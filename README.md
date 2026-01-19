# 🤖 Projet Jean-Michel - TB Groupe

Ce dépôt regroupe l'ensemble des composants de l'agent intelligent **Jean-Michel**.

## 🏗️ Architecture

Le projet est divisé en deux composants principaux :

1. **`gateway/`** : Une Azure Function qui sert de point d'entrée sécurisé pour les messages provenant de **Google Chat**. Elle relaie les requêtes vers l'orchestrateur.
2. **`orchestrator/`** : Le "cerveau" de l'agent, développé avec **Python** et **LangChain**. Il utilise le modèle **Gemini** pour raisonner et appeler des outils métier (souvent via des agents **n8n**).

## 📁 Structure du Projet

- `gateway/` : Code de la passerelle Azure Function.
- `orchestrator/` : Code source de l'intelligence et des agents spécialisés.
- `docs/` : Documentation technique et schémas d'architecture.
- `tests/` : Tests unitaires et d'intégration consolidés.

## 🚀 Démarrage Rapide

### Configuration
1. Clonez ce dépôt.
2. Configurez vos variables d'environnement dans `gateway/local.settings.json` et `orchestrator/.env`.
3. Installez les dépendances pour chaque composant (voir les README locaux).

### Déploiement
Le déploiement est géré par Azure DevOps (voir `azure-pipelines.yml`).

---
*Projet développé pour TB Groupe.*
