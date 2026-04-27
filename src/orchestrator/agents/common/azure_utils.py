import os
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError

class _SecretClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            key_vault_name = os.environ.get("KEY_VAULT_NAME", "kv-tb-ia-agents-secrets")
            
            kv_uri = f"https://{key_vault_name}.vault.azure.net"
            credential = DefaultAzureCredential()
            cls._instance = SecretClient(vault_url=kv_uri, credential=credential)
        return cls._instance

def get_secret(secret_name: str) -> str:
    """Retrieves a secret from Azure Key Vault using Managed Identity."""
    try:
        client = _SecretClientSingleton()
        retrieved_secret = client.get_secret(secret_name)
        return retrieved_secret.value
    except ResourceNotFoundError:
        logging.error(f"Secret '{secret_name}' not found in the Key Vault.")
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        logging.error(f"Failed to retrieve secret '{secret_name}': {e}", exc_info=True)
        raise