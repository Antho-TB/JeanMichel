# 🚀 Projet Agent "Jean-Michel" - TB Groupe

## 1. Vision et Objectifs

Ce projet a pour but de développer un **agent IA spécialisé** 🤖 nommé "Jean-Michel". L'objectif est d'automatiser les processus, de fournir des informations pertinentes et de créer une solution de **BI "conversationnelle"** pour les collaborateurs de TB Groupe.

L'ambition est de créer un agent capable de :
* Comprendre une demande utilisateur en langage naturel.
* Choisir l'outil le plus pertinent pour répondre à la demande (ex: interroger une base de données).
* Exécuter l'outil et analyser le résultat.
* Restituer une synthèse claire et exploitable à l'utilisateur.

Pour intégrer l'IA au cœur des processus de l'entreprise, Jean-Michel est accessible directement via l'application **Google Chat**, comme un collègue virtuel.

---

## 2. Architecture Technique

L'architecture a été entièrement repensée autour d'une pile technologique low-code, robuste et agile, centralisée sur n8n.

### 2.1. Flux de Communication

L'interaction avec Jean-Michel suit le parcours suivant :

**`Utilisateur sur Google Chat`** ➡️ **`Azure Function`** (Passerelle sécurisée) ➡️ **`Webhook n8n`** ➡️ **`Agent n8n`** (Cerveau) ➡️ **`Outils`** (ex: Requête SQL) ➡️ **`API Google Chat`** (Réponse)

### 2.2. Composants de l'Infrastructure

* **Cerveau de l'Agent 🧠** : Un workflow **n8n** hébergé sur une VM Azure. Il utilise le nœud **"AI Agent"** qui orchestre la conversation, le raisonnement (via le LLM **Gemini**) et l'appel aux outils connectés.
* **Compétences Métier (Outils) 🛠️** : Les capacités de l'agent (interroger la base de données, etc.) sont implémentées en tant que **nœuds natifs n8n** (ex: Microsoft SQL) et directement connectées à l'Agent.
* **Infrastructure de Support** :
    * **Calcul** 🖥️ : VM Azure **`TB-Agents-VM`** (Ubuntu) hébergeant l'instance n8n via Docker.
    * **Passerelle** 🚦 : Azure Function **`AppAgentChat`** qui reçoit les requêtes de Google Chat et les transmet de manière fiable au webhook n8n.
    * **CI/CD** 🔄 : **Azure DevOps** (Projet `TB-IA-Agents`) assure le déploiement continu de l'Azure Function via le pipeline `google-chat-function`.
    * **Sécurité** 🔒 : **Azure Key Vault** (`kv-tb-ia-agents-secrets`) pour la gestion centralisée de tous les secrets.

---

## 3. Plateforme de Données (Cible BI)

Le projet s'appuie sur la nouvelle plateforme de données en cours de modernisation sur Azure.
* **ETL/Orchestration** : Azure Data Factory (ADF).
* **Data Warehouse (Infocentre)** : Azure SQL Database (`bitb-2025`).
* **BI & Visualisation** : Power BI.

---

## 4. Environnement de Développement et Accès

### 4.1. Prérequis

* Accès à l'abonnement Azure TB Groupe et au projet Azure DevOps `TB-IA-Agents`.
* Git, Python 3.9+ et Azure Functions Core Tools installés localement.
* Accès SSH à la VM `TB-Agents-VM`.

### 4.2. Configuration de la passerelle (`google-chat-function`)

1.  **Cloner le projet** :
    ```bash
    git clone <URL_du_repo_google-chat-function>
    cd google-chat-function
    ```
2.  **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configurer pour le local** :
    Créez un fichier `local.settings.json` à la racine et renseignez l'URL de votre webhook n8n de test dans la variable `BACKEND_AGENT_URL`.

### 4.3. Accéder à n8n

L'interface de développement de l'agent est accessible via son URL publique ou un tunnel SSH.

* **URL Publique** : `http://20.39.233.78:5679/`
* **Tunnel SSH (Exemple)** :
    ```bash
    ssh -L 5678:localhost:5679 azureTBuser@20.39.233.78
    ```
    Accédez ensuite à `http://localhost:5678` dans votre navigateur.

### 4.4. Gestion des Accès Google Cloud

L'agent utilise des services Google Cloud (Vertex AI pour Gemini, API Google Chat).
* **Projet dédié** : Toutes les ressources sont centralisées dans le projet Google Cloud **`JeanMichel`**.
* **Authentification** : L'authentification est gérée par un **Compte de Service** (`jean-michel-220925@...`). La clé JSON de ce compte est stockée de manière sécurisée en tant que "Credential" de type "Google Service Account" dans n8n.
* **CLI** : L'outil `gcloud` est installé sur la VM pour la gestion et les tests.