import os
import requests
import base64

def get_akeneo_token():
    """
    Récupère un Bearer Token auprès de l'API REST Akeneo PIM
    en utilisant les identifiants fournis dans les variables d'environnement.
    """
    base_url = os.getenv("AKENEO_BASE_URL", "http://192.168.102.22")
    client_id = os.getenv("AKENEO_CLIENT_ID")
    secret = os.getenv("AKENEO_SECRET")
    username = os.getenv("AKENEO_USERNAME", "test_5292")
    password = os.getenv("AKENEO_PASSWORD", "VOTRE_MOT_DE_PASSE_AKENEO")

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
