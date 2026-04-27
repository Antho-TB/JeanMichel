"""
[ARCHITECTURE] Gestionnaire de Secrets Cloud (JeanMichel)

Rôle global :
Ce module est le garant de la sécurité MLOps (Doctrine NUBO). Il centralise et abstrait 
l'accès aux secrets (clés d'API, credentials DB) stockés dans Azure Key Vault. 
Il est appelé par tous les autres agents et outils du projet JeanMichel lorsqu'ils 
ont besoin de s'authentifier auprès de services externes.

Stratégie métier (Singleton & IAM) :
- L'instanciation du client Key Vault (`SecretClient`) coûte cher en millisecondes et en réseau.
  La stratégie du "Singleton" (`_SecretClientSingleton`) garantit que l'application ne négocie 
  l'authentification Azure IAM (`DefaultAzureCredential`) qu'une seule fois au démarrage.
- `DefaultAzureCredential` est utilisé car il permet aux développeurs de tester en local 
  (via `az login`) sans friction, tout en basculant magiquement sur la "Managed Identity" 
  quand le code tourne en production sur les serveurs Microsoft. Zéro mot de passe sur le disque.
"""

import os
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError

class _SecretClientSingleton:
    """
    Singleton garantissant l'unicité de la connexion au Key Vault Azure.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logging.info("[INFO] Première connexion à l'Azure Key Vault demandée. Négociation IAM...")
            # Fallback en dur sur le KeyVault du projet pour éviter de dépendre de l'OS
            key_vault_name = os.environ.get("KEY_VAULT_NAME", "kv-tb-ia-agents-secrets")
            
            kv_uri = f"https://{key_vault_name}.vault.azure.net"
            credential = DefaultAzureCredential()
            cls._instance = SecretClient(vault_url=kv_uri, credential=credential)
        return cls._instance

def get_secret(secret_name: str) -> str:
    """
    Récupère la valeur d'un secret stocké dans le coffre-fort Azure.
    
    Stratégie :
    Fait appel au Singleton pour éviter la latence. Capture les erreurs spécifiques (ex: 404 Not Found)
    pour fournir un log explicite à l'équipe Infra avant de faire planter l'agent.
    
    Args:
        secret_name (str): Le nom exact du secret (ex: 'Google-APIKey').
        
    Returns:
        str: La valeur en clair du secret.
    """
    try:
        client = _SecretClientSingleton()
        retrieved_secret = client.get_secret(secret_name)
        return retrieved_secret.value
        
    except ResourceNotFoundError:
        # Erreur classique si un nom a été mal tapé ou si Terraform n'a pas encore provisionné le secret
        logging.error(f"[ALERTE NUBO] Le secret '{secret_name}' n'existe pas dans le Key Vault.")
        raise ValueError(f"Secret '{secret_name}' introuvable.")
        
    except Exception as e:
        # Erreurs réseau, VPN IPSec tombé, ou problème de droits IAM (RBAC)
        logging.error(f"[ERREUR FATALE] Échec de la récupération du secret '{secret_name}' : {e}", exc_info=True)
        raise