# 🚀 Projet Agents-TB - TB Groupe

## 1. Vision et Objectifs

Ce projet a pour but de développer une **équipe d'agents IA spécialisés** 🤖 pour chaque métier de l'entreprise (comptabilité, commerce, supply chain, etc.). L'objectif est d'automatiser les processus, de fournir des informations pertinentes et de créer une solution de **BI "conversationnelle"** pour les utilisateurs finaux.

L'ambition est de créer des agents capables de :
* Comprendre une demande utilisateur en langage naturel.
* Orchestrer des actions complexes en faisant appel à des outils et agents spécialisés.
* Interroger la plateforme de données pour consolider des informations.
* Restituer une synthèse claire et exploitable.

### L'Agent "Jean-Michel" sur Google Chat 💬

Pour intégrer l'IA au cœur des processus de l'entreprise, l'agent orchestrateur prend la forme d'un "collègue virtuel" nommé **Jean-Michel**, accessible directement via l'application **Google Chat**.

L'architecture cible de cette intégration est la suivante :

* Un **Chatbot Google Chat** représente l'interface de "Jean-Michel".
* Il transmet les messages des utilisateurs à une **Azure Function**, agissant comme un pont sécurisé 🌉.
* L'Azure Function invoque l'**agent orchestrateur Python/LangChain**, qui traite la demande.
* La réponse est renvoyée à l'utilisateur dans la conversation Google Chat.

Cette approche rend l'interaction avec notre système d'IA aussi simple et naturelle que de discuter avec un collègue.

---

## 2. Environnement Technique

L'architecture du projet a été validée pour allier robustesse et agilité.

### 2.1. Architecture des Agents IA

* **Agent Orchestrateur ("Cerveau")** 🧠: Développé en **Python** avec **LangChain**, il gère la logique IA. Il est exposé via une API Flask sur un serveur **Gunicorn** sur la VM.
* **Agents Spécialisés ("Experts Métier")** 👷: Développés en **n8n**, ils exécutent des tâches précises (ex: interroger la base de données, appeler une API).
* **Infrastructure de Support** 🛠️:
    * **Calcul** 🖥️: VM Azure `TB-Agents-VM` (Ubuntu) hébergeant n8n via Docker et le service de l'agent Python.
    * **Passerelle** 🚦: Azure Function `AppAgentChat` pour relayer les requêtes de Google Chat vers la VM.
    * **CI/CD** 🔄: Azure DevOps (Projet `TB-IA-Agents` pour le code Python).
    * **Sécurité** 🔒: Azure Key Vault `kv-tb-ia-agents-secrets` pour la gestion centralisée des secrets, avec accès via l'Identité Managée de la VM et de la Function App.
    * **Supervision** 📈: Application Insights `AppInsights-TB-IA-Agents` pour la centralisation des logs.

### 2.2. Plateforme de Données (BI)

* **Cible Stratégique** 🎯: Une pile 100% cloud native sur Azure (ADF, ADLS Gen2, Synapse Analytics, Power BI).
* **Implémentation Actuelle** ✅:
    * **Source** : Base de données ERP Sylob.
    * **Connectivité** : Passerelle de données installée sur `SERVFTP-REPORT`.
    * **Entrepôt** : Base de données `INFOCENTRE` sur un SQL Server local.

---

## 3. Démarrage Rapide / Configuration de l'Environnement

1.  **Prérequis** ✅:
    * Accès à l'abonnement Azure TB Groupe et au projet Azure DevOps `TB-IA-Agents`.
    * Git, Python 3.11+ et Azure CLI installés localement.

2.  **Cloner le projet (Code de l'orchestrateur)** 💾:
    ```bash
    git clone <URL_du_repo_ia-agents-code>
    cd ia-agents-code
    ```

3.  **Configurer l'environnement virtuel Python** 🐍:
    ```bash
    # Créer l'environnement virtuel
    python -m venv .venv

    # Activer l'environnement virtuel
    # Sur Windows (cmd.exe):
    .venv\Scripts\activate
    # Sur Windows (Git Bash) / Linux / macOS:
    source .venv/bin/activate
    ```

    ## Structure du Projet (Code Python)

ia-agents-code/
├── .venv/                     # Environnement virtuel Python (ignoré par Git)
│
├── agents/                    # Code source de tous les agents
│   ├── init.py
│   │
│   ├── common/                # Modules partagés par tous les agents
│   │   ├── init.py
│   │   └── azure_utils.py     # Fonctions pour Key Vault, Application Insights, etc.
│   │
│   └── commerce_agent/        # Agent spécialisé pour le domaine "Commerce"
│       ├── init.py
│       ├── main.py            # Point d'entrée principal de l'agent (avec la boucle d'interaction)
│       └── tools.py           # Définition des "outils" LangChain pour cet agent (ex: appeler n8n)
│
├── notebooks/                 # Notebooks pour l'exploration et le prototypage
│   └── 1-test-n8n-connection.ipynb
│
├── docs/                      # Documentation du projet
│   └── architecture.md
│
├── tests/                     # Tests unitaires et d'intégration
│   ├── init.py
│   ├── test_commerce_agent_tools.py # Tests pour les outils de l'agent commerce
│   └── common/
│       ├── init.py
│       └── test_azure_utils.py      # Tests pour les fonctions utilitaires Azure
│
├── .gitignore                 # Fichier Git pour ignorer les fichiers non désirés
├── azure-pipelines.yml        # Définition du pipeline CI/CD sur Azure DevOps
├── README.md                  # Documentation principale du projet
└── requirements.txt           # Liste des dépendances Python du projet

4.  **Installer les dépendances** 📦:
    ```bash
    python -m pip install -r requirements.txt
    ```

4.  **Exécuter les tests** 🧪:
    Après avoir installé les dépendances, vous pouvez exécuter les tests unitaires et d'intégration avec `pytest` :
    ```bash
    pytest
    ```

5.  **Authentification Azure CLI** 🔑:
    Pour que les scripts locaux puissent accéder aux secrets du Key Vault :
    ```bash
    az login
    az account set --subscription "Abonnement Azure 1"
    ```

6.  **Accéder à n8n** 🌐:
    L'interface de développement des agents spécialisés est accessible via un tunnel SSH sécurisé :
    ```bash
    ssh -L 5678:localhost:5678 azureTBuser@<IP_PUBLIQUE_DE_LA_VM>
    ```
    Accédez ensuite à `http://localhost:5678` dans votre navigateur.

---

## 4. Problème Actuel & Diagnostic en Cours

* **Problème** 🐛: L'agent "Jean-Michel" ne répond pas dans Google Chat, bien que tous les services (Gunicorn, n8n) soient opérationnels sur la VM.
* **Diagnostic** 🧐: L'Azure Function reçoit les requêtes de Google Chat mais ne renvoie aucune réponse. Les logs du "Flux de journaux" de l'Azure Function ne montrent aucune trace de notre code Python.
* **Hypothèse** 🤔: Le worker Python de l'Azure Function ne parvient pas à charger ou à exécuter le script `__init__.py`, ou un problème de journalisation empêche les logs d'atteindre Application Insights, malgré une configuration de `host.json` et de la chaîne de connexion validée.

---

## 5. Documentation Complémentaire

* [Mémo : Création et Débogage d'un Agent n8n](https://dev.azure.com/TB-IA-Agents/TB-IA-Agents/_wiki/wikis/TB-IA-Agents.wiki/1/M%C3%A9mo-Cr%C3%A9ation-et-D%C3%A9bogage-d'un-Agent-n8n-connect%C3%A9-%C3%A0-Azure-SQL)

## Structure du Projet (Code Python)

ia-agents-code/
├── .venv/                   # Environnement virtuel Python (ignoré par Git)
│
├── agents/                  # Code source de tous les agents
│   ├── __init__.py
│   │
│   ├── common/              # Modules partagés par tous les agents
│   │   ├── __init__.py
│   │   └── azure_utils.py   # Fonctions pour Key Vault, Application Insights, etc.
│   │
│   └── commerce_agent/      # Agent spécialisé pour le domaine "Commerce"
│       ├── __init__.py
│       ├── main.py          # Point d'entrée principal de l'agent (avec la boucle d'interaction)
│       └── tools.py         # Définition des "outils" LangChain pour cet agent (ex: appeler n8n)
│
├── notebooks/               # Notebooks pour l'exploration et le prototypage
│   └── 1-test-n8n-connection.ipynb
│
├── docs/                    # Documentation du projet
│   └── architecture.md
│
├── tests/                   # Tests unitaires et d'intégration
│   ├── __init__.py
│   └── test_example.py      # Exemple de test
│
├── .gitignore               # Fichier Git pour ignorer les fichiers non désirés
├── azure-pipelines.yml      # Définition du pipeline CI/CD sur Azure DevOps
├── README.md                # Documentation principale du projet
└── requirements.txt         # Liste des dépendances Python du projet
# 🚀 Projet Agents-TB - TB Groupe

## 1. Vision et Objectifs

Ce projet a pour but de développer une **équipe d'agents IA spécialisés** 🤖 pour chaque métier de l'entreprise (comptabilité, commerce, supply chain, etc.). L'objectif est d'automatiser les processus, de fournir des informations pertinentes et de créer une solution de **BI "conversationnelle"** pour les utilisateurs finaux.

L'ambition est de créer des agents capables de :
* Comprendre une demande utilisateur en langage naturel.
* Orchestrer des actions complexes en faisant appel à des outils et agents spécialisés.
* Interroger la plateforme de données pour consolider des informations.
* Restituer une synthèse claire et exploitable.

### L'Agent "Jean-Michel" sur Google Chat 💬

Pour intégrer l'IA au cœur des processus de l'entreprise, l'agent orchestrateur prend la forme d'un "collègue virtuel" nommé **Jean-Michel**, accessible directement via l'application **Google Chat**.

L'architecture cible de cette intégration est la suivante :

* Un **Chatbot Google Chat** représente l'interface de "Jean-Michel".
* Il transmet les messages des utilisateurs à une **Azure Function**, agissant comme un pont sécurisé 🌉.
* L'Azure Function invoque l'**agent orchestrateur Python/LangChain**, qui traite la demande.
* La réponse est renvoyée à l'utilisateur dans la conversation Google Chat.

Cette approche rend l'interaction avec notre système d'IA aussi simple et naturelle que de discuter avec un collègue.

---

## 2. Environnement Technique

L'architecture du projet a été validée pour allier robustesse et agilité.

### 2.1. Architecture des Agents IA

* **Agent Orchestrateur ("Cerveau")** 🧠: Développé en **Python** avec **LangChain**, il gère la logique IA. Il est exposé via une API Flask sur un serveur **Gunicorn** sur la VM.
* **Agents Spécialisés ("Experts Métier")** 👷: Développés en **n8n**, ils exécutent des tâches précises (ex: interroger la base de données, appeler une API).
* **Infrastructure de Support** 🛠️:
    * **Calcul** 🖥️: VM Azure `TB-Agents-VM` (Ubuntu) hébergeant n8n via Docker et le service de l'agent Python.
    * **Passerelle** 🚦: Azure Function `AppAgentChat` pour relayer les requêtes de Google Chat vers la VM.
    * **CI/CD** 🔄: Azure DevOps (Projet `TB-IA-Agents` pour le code Python).
    * **Sécurité** 🔒: Azure Key Vault `kv-tb-ia-agents-secrets` pour la gestion centralisée des secrets, avec accès via l'Identité Managée de la VM et de la Function App.
    * **Supervision** 📈: Application Insights `AppInsights-TB-IA-Agents` pour la centralisation des logs.

