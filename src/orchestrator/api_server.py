"""
[ARCHITECTURE] Microservice API Asynchrone (JeanMichel)

Rôle global :
Cette brique expose un point d'accès API (Endpoint `/ask`) qui permet à n'importe quel script
externe de l'infrastructure de solliciter le "cerveau" de JeanMichel via une requête HTTP POST.

Stratégie métier (Security & Découplage) :
L'API est sécurisée par un Bearer Token basique (injecté via Azure Key Vault). 
Le but est d'empêcher un appel involontaire ou malveillant. 
Le design est volontairement léger pour que cet exécutable puisse être déployé
comme un microservice indépendant de l'Orchestrateur lourd.
"""

from flask import Flask, request, jsonify
from agents.common.azure_utils import get_secret
import logging

# Optionnel selon l'implémentation choisie par l'orchestrateur
try:
    from main import get_agent_response
except ImportError:
    # Fallback propre au cas où le routage diffère
    get_agent_response = None

# --- Initialisation de l'application ---
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
app = Flask(__name__)

# Injection sécurisée de la clé API pour l'authentification M2M (Machine to Machine)
API_KEY = get_secret("AGENT-API-KEY")

@app.route('/ask', methods=['POST'])
def ask_agent():
    """
    Traite les requêtes entrantes pour interroger l'Agent IA.
    
    Stratégie :
    1. Validation du contrat d'interface (Token présent et valide).
    2. Extraction du payload ('query').
    3. Délégation du raisonnement à la fonction métier (`get_agent_response`).
    4. Renvoi du résultat ou Fallback avec code HTTP approprié.
    """
    # 1. Sécurité (Authentication)
    auth_header = request.headers.get('Authorization')
    if not auth_header or ' ' not in auth_header or auth_header.split(" ")[1] != API_KEY:
        logging.warning("[ALERTE] Tentative d'accès API avec un jeton invalide ou manquant.")
        return jsonify({"error": "Accès non autorisé. Clé API invalide."}), 401

    # 2. Exécution Métier
    logging.info("[INFO] Authentification M2M réussie. Réception du payload...")
    try:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({"error": "Payload invalide. Le champ 'query' est requis."}), 400
        
        user_query = data['query']
        logging.info(f"[INFO] Traitement de la question : {user_query}")
        
        # Délégation de la complexité au graphe LangChain (JeanMichel)
        if get_agent_response:
            agent_response = get_agent_response(user_query)
        else:
            # Mode "mock" ou fallback si la fonction n'est pas importable dans ce contexte d'exécution
            agent_response = "Erreur de liaison interne avec l'Orchestrateur principal."
            
        return jsonify({"response": agent_response})

    except Exception as e:
        # On loggue l'erreur complexe, mais on renvoie un message bateau pour la sécurité (pas de stack trace fuyante)
        logging.error(f"[ERREUR] Échec du traitement de la requête /ask : {e}", exc_info=True)
        return jsonify({"error": "Erreur interne du serveur lors de la réflexion de l'Agent."}), 500

if __name__ == '__main__':
    logging.info("[INFO] Démarrage du Microservice API JeanMichel sur le port 5000...")
    app.run(host='0.0.0.0', port=5000)
