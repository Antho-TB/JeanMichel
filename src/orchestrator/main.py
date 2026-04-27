"""
[ARCHITECTURE] Agent Orchestrator Gateway (JeanMichel)

Rôle global :
Ce script est le coeur battant de "JeanMichel", notre architecture multi-agents.
Il expose un webhook HTTP (Flask) permettant à des clients externes (comme Google Chat)
d'interagir avec notre Agent IA. Il charge la configuration, initialise l'Agent Executor (LangChain)
et route les requêtes en langage naturel vers le bon outil métier.

Stratégie métier (Agentique & Caching contextuel) :
Plutôt que de ré-instancier l'agent (et ses outils) à chaque requête HTTP (ce qui ralentirait 
les temps de réponse), on utilise l'objet `g` de Flask. Cela permet de cacher le graphe d'exécution
LangChain dans le contexte de l'application. On injecte de manière dynamique la clé API Gemini
depuis Azure Key Vault pour garantir un Zero Trust absolu (Doctrine NUBO).
"""

from flask import Flask, request, jsonify, g
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from agents.common.azure_utils import get_secret
from agents.commerce_agent.tools import get_client_summary_tool
import logging
import json
import os

# Logging visuel et structuré pour la prod
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
app = Flask(__name__)

def get_agent_executor() -> AgentExecutor:
    """
    Initialise et retourne le moteur d'exécution de l'agent LangChain.
    
    Stratégie :
    C'est un Singleton pattern adapté à Flask. On vérifie si l'agent est déjà en mémoire (`g`).
    S'il ne l'est pas, on construit le graphe : Modèle (Gemini Flash) + Tools (Outils métier) + Prompt.
    On utilise le modèle `gemini-1.5-flash-latest` pour maximiser la vitesse de réponse 
    sur les interactions conversationnelles classiques.
    """
    if 'agent_executor' not in g:
        logging.info("Initialisation du graphe cognitif LangChain...")
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            with open('prompt.txt', 'r', encoding='utf-8') as f:
                template = f.read()

            # Instanciation du LLM avec secret injecté depuis Key Vault (0 dotenv)
            llm = ChatGoogleGenerativeAI(
                model=config.get("llm_model_name", "models/gemini-1.5-flash-latest"),
                google_api_key=get_secret("Google-APIKey")
            )
            
            tools = [get_client_summary_tool]
            prompt = PromptTemplate.from_template(template)
            
            # Création de l'agent raisonneur (ReAct : Reason + Act)
            agent = create_react_agent(llm, tools, prompt)
            
            # Paramétrage strict : verbose pour le debug, handle_parsing_errors pour ne pas crasher 
            # si le LLM hallucine un format de réponse hors contrat.
            g.agent_executor = AgentExecutor(
                agent=agent, 
                tools=tools, 
                verbose=True, 
                handle_parsing_errors=True
            )
            logging.info("[SUCCÈS] Agent cognitif prêt à recevoir des instructions.")
            
        except FileNotFoundError as e:
            logging.error(f"[ERREUR] Fichier de configuration ou de prompt introuvable : {e}", exc_info=True)
            raise
        except Exception as e:
            logging.error(f"[ERREUR] Échec de l'initialisation de l'Agent : {e}", exc_info=True)
            raise
            
    return g.agent_executor

@app.route("/", methods=["POST"])
def handle_request():
    """
    Point d'entrée (Webhook) principal pour interagir avec JeanMichel.
    
    Stratégie :
    Extrait le payload (ex: format Google Chat), interroge l'Agent, et wrap la 
    réponse dans le JSON attendu par l'appelant. Un fallback sécurisé est mis en 
    place (Status 500) pour ne jamais exposer la stack trace technique à l'utilisateur.
    """
    try:
        agent_executor = get_agent_executor()
    except Exception:
        return jsonify({"text": "Oups, une erreur système m'empêche de démarrer mon cerveau. Vérifiez les logs serveurs."}), 500

    try:
        request_data = request.get_json()
        user_query = request_data.get('message', {}).get('text')

        if not user_query:
            logging.warning("Requête reçue sans question.")
            return jsonify({"text": "Je n'ai pas reçu de question. Que puis-je faire pour vous ?"})

        logging.info(f"Traitement de la requête métier : {user_query}")
        result = agent_executor.invoke({"input": user_query})
        response_text = result.get("output", "Je n'ai pas trouvé de réponse pertinente.")

        return jsonify({"text": response_text})
        
    except Exception as e:
        logging.error(f"[ERREUR] Crash durant l'exécution de la requête : {e}", exc_info=True)
        return jsonify({"text": "Désolé, mes circuits ont surchauffé (Erreur interne)."}), 500

if __name__ == '__main__':
    # Résolution dynamique du port (Google Cloud Run / Azure Container Apps)
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)