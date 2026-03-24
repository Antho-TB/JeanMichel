import logging
import os
from azure.identity import DefaultAzureCredential 
from azure.keyvault.secrets import SecretClient 
from azure.monitor.opentelemetry import configure_azure_monitor 

# --- Configuration initiale du Logger TRÈS VERBEUSE pour le DÉBOGAGE LOCAL ---
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# Mettez le niveau à DEBUG pour tout voir au début
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, handlers=[logging.StreamHandler()]) 
logger = logging.getLogger(__name__)
logger.info("Logger configuré pour la console en mode DEBUG (local).")


# --- Constantes pour Key Vault et Application Insights ---
KEY_VAULT_NAME = "kv-tb-ia-agents-secrets" 
KV_URI = f"https://{KEY_VAULT_NAME}.vault.azure.net"
APP_INSIGHTS_SECRET_NAME = "AppInsightsConnectionString-TB-IA-Agents"

# --- Fonction pour récupérer un secret depuis Key Vault ---
def get_secret_from_key_vault(secret_name: str) -> str | None:
    logger.debug(f"Début de get_secret_from_key_vault pour le secret : {secret_name}")
    try:
        # DefaultAzureCredential essaiera plusieurs méthodes d'authentification,
        # y compris l'identité managée de la VM ou les identifiants Azure CLI locaux.
        credential = DefaultAzureCredential()
        logger.debug("DefaultAzureCredential instancié.")
        client = SecretClient(vault_url=KV_URI, credential=credential)
        logger.debug(f"SecretClient instancié pour KV_URI: {KV_URI}")
        retrieved_secret = client.get_secret(secret_name)
        logger.info(f"Secret '{secret_name}' récupéré avec succès depuis Key Vault.")
        return retrieved_secret.value
    except Exception as e:
        logger.error(f"Erreur DANS get_secret_from_key_vault lors de la récupération du secret '{secret_name}': {e}", exc_info=True)
        return None

# --- Initialisation d'Azure Monitor pour la journalisation centralisée ---
def initialize_azure_monitor_logging():
    logger.info("Tentative d'initialisation de la journalisation Azure Monitor...")
    connection_string = get_secret_from_key_vault(APP_INSIGHTS_SECRET_NAME)

    if connection_string:
        logger.info("Chaîne de connexion AppInsights récupérée, tentative de configuration d'Azure Monitor.")
        try:
            configure_azure_monitor(
                connection_string=connection_string,
                # Vous pouvez désactiver la collecte de traces et de métriques si vous ne voulez que les logs :
                # disable_tracing=True,
                # disable_metrics=True,
            )
            # Le logger global est maintenant configuré pour envoyer vers Azure Monitor
            logger.info("Journalisation Azure Monitor configurée avec succès.")
        except Exception as e:
            logger.error(f"Erreur DANS initialize_azure_monitor_logging lors de la configuration d'Azure Monitor : {e}", exc_info=True)
    else:
        logger.warning("Chaîne de connexion Application Insights NON TROUVÉE. La journalisation Azure Monitor n'est PAS activée.")

# --- Logique principale de l'agent ---
def run_pipeline_monitor_agent():
    logger.info("L'agent de surveillance des pipelines démarre (simulation locale).")
    # TODO: Implémentez ici la logique de surveillance des pipelines Fabric.
    logger.info("L'agent de surveillance des pipelines a terminé son cycle (simulation locale).")


if __name__ == "__main__":
    logger.info(f"Démarrage du script principal de l'agent ({__file__}) en local.")
    
    initialize_azure_monitor_logging() # Appel de l'initialisation
    
    run_pipeline_monitor_agent()
    
    logger.info("Script principal de l'agent terminé (local).")