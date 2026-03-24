import os
import requests
import json
from langchain.tools import tool

N8N_COMMERCE_AGENT_URL = os.environ.get("N8N_COMMERCE_AGENT_URL")

@tool
def get_client_summary_tool(client_name: str) -> str:
    """Indispensable pour obtenir le résumé d'un client à partir de son code. Utilise cet outil chaque fois que l'utilisateur demande des informations sur un client spécifique en fournissant un code client. L'entrée doit être le code client sous forme de chaîne de caractères."""
    if not N8N_COMMERCE_AGENT_URL:
        return "Error: The client summary service is not configured."

    headers = {"Content-Type": "application/json"}
    payload = {"clientCode": client_name}

    try:
        response = requests.post(N8N_COMMERCE_AGENT_URL, json=payload, headers=headers)
        response.raise_for_status()
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        return "Error: Could not connect to the client summary service."