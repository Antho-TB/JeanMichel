from flask import Flask, request, jsonify, g
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from agents.common.azure_utils import get_secret
from agents.commerce_agent.tools import get_client_summary_tool
from dotenv import load_dotenv
import logging
import json
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

def get_agent_executor():
    """
    Initializes and returns the LangChain agent executor.
    Uses the Flask application context (g) to store the agent,
    ensuring it is created only once per request.
    """
    if 'agent_executor' not in g:
        logging.info("Initializing the LangChain agent...")
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            with open('prompt.txt', 'r') as f:
                template = f.read()

            llm = ChatGoogleGenerativeAI(
                model=config.get("llm_model_name", "models/gemini-1.5-flash-latest"),
                google_api_key=get_secret("Google-APIKey")
            )
            tools = [get_client_summary_tool]
            prompt = PromptTemplate.from_template(template)
            agent = create_react_agent(llm, tools, prompt)
            g.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
            logging.info("Agent is ready.")
        except FileNotFoundError as e:
            logging.error(f"Configuration or prompt file not found: {e}", exc_info=True)
            raise
        except Exception as e:
            logging.error(f"Failed to initialize agent: {e}", exc_info=True)
            raise
    return g.agent_executor

@app.route("/", methods=["POST"])
def handle_request():
    """
    Handles incoming requests, executes the query using the agent,
    and returns the response.
    """
    try:
        agent_executor = get_agent_executor()
    except Exception:
        return jsonify({"text": "Error: Agent is not initialized. Check server logs."}), 500

    try:
        request_data = request.get_json()
        user_query = request_data.get('message', {}).get('text')

        if not user_query:
            return jsonify({"text": "I did not receive a question."})

        logging.info(f"Executing query: {user_query}")
        result = agent_executor.invoke({"input": user_query})
        response_text = result.get("output", "I could not find an answer.")

        return jsonify({"text": response_text})
    except Exception as e:
        logging.error(f"Error handling request: {e}", exc_info=True)
        return jsonify({"text": "Sorry, an internal error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))