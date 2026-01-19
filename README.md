# 🤖 Projet Jean-Michel - TB Groupe

Système intelligent de BI "conversationnelle" pour les collaborateurs de TB Groupe, propulsé par l'IA Google Gemini.

---

## 🎯 Résumé du Projet

**Objectif** : Créer un "collègue virtuel" accessible sur **Google Chat** capable d'automatiser les processus métier et de fournir des analyses de données en temps réel en langage naturel.

### 🛡️ Les 3 Piliers de la Solution

1.  **Le Pont (Interface)** 🚦
    *   **Composant** : `gateway/` (Azure Function)
    *   **Rôle** : Point d'accès sécurisé qui réceptionne les messages de Google Chat et les transmet de manière fiable à l'orchestrateur.

2.  **Le Cerveau (IA)** 🧠
    *   **Composant** : `orchestrator/` (Python + LangChain)
    *   **Rôle** : Analyse la demande utilisateur via Gemini, définit la stratégie de réponse et appelle les outils nécessaires pour récupérer la donnée.

3.  **Les Experts (Métier)** 🛠️
    *   **Composant** : Workflows **n8n** (Agents spécialisés)
    *   **Rôle** : Exécutent des tâches précises comme interroger l'ERP Sylob ou la base SQL Server pour remonter la donnée brute à l'IA.

---

## 🏗️ Architecture & Flux

### ➤ Parcours d'une requête
**`Utilisateur`** ➡️ **`Azure Function`** (Sécurité) ➡️ **`Agent Python`** (Raisonnement) ➡️ **`n8n`** (Action) ➡️ **`Données`** (Source)

### ➤ Sécurité
*   **Secrets** : Gestion centralisée via **Azure Key Vault** (`kv-tb-ia-agents-secrets`).
*   **Logs** : Supervision complète via **Application Insights** pour le suivi des performances et des erreurs.

---

## 📁 Structure du Projet

```text
JeanMichel/
├── docs/             # Documentation technique et schémas d'architecture
├── gateway/          # 🚦 Code de la passerelle Azure Function
├── orchestrator/     # 🧠 Code du cerveaux IA (Python/LangChain)
├── tests/            # 🧪 Tests unitaires et d'intégration consolidés
├── azure-pipelines.yml # 🔄 Pipeline CI/CD Azure DevOps
└── README.md         # 📖 Ce document
```

---

## 🚀 Utilisation

### ➤ Configuration Locale
1.  **Cloner le dépôt** :
    ```bash
    git clone <URL_du_repo_JeanMichel>
    cd JeanMichel
    ```
2.  **Variables d'environnement** :
    *   Configurer `gateway/local.settings.json` pour la passerelle.
    *   Configurer `orchestrator/.env` pour l'intelligence (Clé Gemini, Azure Auth).

### ➤ Lancement
*   **Passerelle** : `func start` dans le dossier `gateway/`.
*   **Orchestrateur** : `python main.py` dans le dossier `orchestrator/`.

---

## �️ Stack Technique

*   **IA & LLM** : Google Gemini 2.5 Flash / Pro.
*   **Framework IA** : Python 3.11 + LangChain.
*   **Infrastructure** : Azure Functions, Azure VM (Docker), Azure Key Vault.
*   **Automatisation Métier** : n8n (Low-code workflow).
*   **Canal Client** : Google Chat (Vertex AI SDK).

---

## 🌐 Migration vers la nouvelle architecture Azure TB-Groupe

Pour aligner **Jean-Michel** avec les nouveaux standards de la Landing Zone TB-Groupe, les évolutions suivantes sont à prévoir :

### ➤ Gouvernance & Nommage
*   **Convention de Nommage** : Adopter le format `<Prefix>-shsv-<Feature>-<Env>`.
    *   Exemples : `func-shsv-jeanmichel-gateway-prod`, `kv-shsv-jeanmichel-prod`.
*   **Tags Obligatoires** : Appliquer systématiquement les tags `project: JeanMichel` et `deployment: IaC`.
*   **Région** : Isolation dans la région **North Europe**.

### ➤ Infrastructure (Landing Zone)
*   **Déploiement** : Utilisation du module Terraform `mod-landing-zone` au sein du Management Group `Shared Services`.
*   **Réseau** : Ségrégation stricte via des VNets dédiés par environnement.

### ➤ Services de Données (PostgreSQL)
*   **Instance Partagée** : Migration vers les serveurs flexibles `psql-dtpf-psql-dev` / `prod`.
*   **Accès Privé** : Utilisation de **Self-hosted Runners** pour le CI/CD (accès réseau privé uniquement).
*   **FinOps** : Respect du planning d'arrêt automatique (18h-9h et week-end) pour les instances de DEV.

### ➤ DevOps & Observabilité
*   **GitHub Actions** : Migration vers GitHub Actions avec injection de secrets via tokenisation (`@#{VAR_NAME}#@`).
*   **Logs** : Centralisation forcée vers le workspace `log-platform-logs-prd` via Azure Policy.

---
Anthony, Service Data&ia TB-Groupe 
