from flask import Flask, request, jsonify
from agents.common.azure_utils import get_secret
import requests
import os
# On importe notre fonction depuis le fichier main.py
from main import get_agent_response

# --- Initialisation de l'application ---
app = Flask(__name__)
API_KEY = get_secret("AGENT-API-KEY")

# --- Point d'entrée de l'API (/ask) ---
@app.route('/ask', methods=['POST'])
def ask_agent():
    # 1. Sécurité
    auth_header = request.headers.get('Authorization')
    if not auth_header or ' ' not in auth_header or auth_header.split(" ")[1] != API_KEY:
        return jsonify({"error": "Clé API invalide ou manquante."}), 401

    # 2. Exécution
    print("Authentification réussie. Traitement de la requête...")
    try:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({"error": "Le champ 'query' est manquant."}), 400
        
        user_query = data['query']
        
        # Appel de la fonction de notre agent
        agent_response = get_agent_response(user_query)
        
        return jsonify({"response": agent_response})

    except Exception as e:
        print(f"[ERREUR] : {e}")
        return jsonify({"error": "Erreur interne du serveur."}), 500

# --- Lancement du serveur ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
WJyy*q6f9X$G5T8%!h@7
