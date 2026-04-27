import os
import base64
import requests
import json
import logging
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'orchestrator')))
from agents.common.azure_utils import get_secret

def get_akeneo_token():
    """
    Récupère un token d'accès Akeneo (OAuth2 Password Grant)
    en utilisant les identifiants stockés dans Azure Key Vault.
    """
    base_url = get_secret("AKENEO-BASE-URL")
    client_id = get_secret("AKENEO-CLIENT-ID")
    secret = get_secret("AKENEO-SECRET")
    username = get_secret("AKENEO-USERNAME")
    password = get_secret("AKENEO-PASSWORD")

    if not client_id or not secret:
        raise ValueError("AKENEO_CLIENT_ID ou AKENEO_SECRET manquant.")

    # Akeneo exige une authentification Basic avec le Client ID et le Secret encodés en base64
    credentials = f"{client_id}:{secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    url = f"{base_url}/api/oauth/v1/token"
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "grant_type": "password",
        "username": username,
        "password": password
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Erreur connexion Akeneo : {response.status_code} - {response.text}")

def test_akeneo_connection():
    """ Fonction de test pour valider la récupération du token """
    try:
        token = get_akeneo_token()
        print("✅ Connexion Akeneo réussie. Token obtenu.")
        return token
    except Exception as e:
        print(f"❌ Échec de connexion Akeneo : {e}")
        return None

if __name__ == "__main__":
    test_akeneo_connection()
