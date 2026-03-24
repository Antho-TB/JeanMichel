import logging
import azure.functions as func
import os
import requests
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('>>> Requête reçue par la fonction GoogleChatWebhook.')

    try:
        backend_agent_url = os.environ.get("BACKEND_AGENT_URL")
        if not backend_agent_url:
            logging.error("!!! ERREUR FATALE: La variable d'environnement BACKEND_AGENT_URL n'est pas configurée.")
            return func.HttpResponse(
                body=json.dumps({'text': 'Erreur: Le service est momentanément indisponible.'}),
                status_code=200,
                headers={'Content-Type': 'application/json'}
            )

        req_body = req.get_body()
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(url=backend_agent_url, data=req_body, headers=headers, timeout=25)
            response.raise_for_status() 

            return func.HttpResponse(
                body=response.content,
                status_code=response.status_code,
                headers={'Content-Type': 'application/json'}
            )

        except requests.exceptions.ReadTimeout:
            logging.error(f"!!! Timeout lors de l'appel au backend agent : {backend_agent_url}")
            return func.HttpResponse(
                body=json.dumps({'text': "Désolé, je prends un peu plus de temps pour répondre. Veuillez patienter quelques instants, je vous écris dès que j'ai trouvé."}),
                status_code=200,
                headers={'Content-Type': 'application/json'}
            )

        except requests.exceptions.RequestException as req_err:
            logging.error(f"!!! Erreur de connexion au backend agent : {req_err}")
            return func.HttpResponse(
                body=json.dumps({'text': 'Erreur: Le service est momentanément indisponible.'}),
                status_code=200,
                headers={'Content-Type': 'application/json'}
            )

    except Exception as e:
        logging.error(f"!!! UNE EXCEPTION NON GÉRÉE EST SURVENUE : {e}", exc_info=True)
        return func.HttpResponse(
            body=json.dumps({'text': 'Une erreur inattendue est survenue.'}),
            status_code=200,
            headers={'Content-Type': 'application/json'}
        )