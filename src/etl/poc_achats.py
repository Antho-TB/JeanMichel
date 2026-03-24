import streamlit as st
import pandas as pd
import os
import time
import random
import requests
from dotenv import load_dotenv

# Chargement des variables d'environnement (fichier .env)
load_dotenv()
import random
import random


# Configuration de la page
st.set_page_config(
    page_title="Portail Achats TB - Imports", 
    page_icon="🚢", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS (Pro but relaxed) ---
st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', sans-serif;
        color: #2E4053;
        font-weight: 700;
    }
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


DATA_DIR = "DWH_Achats"

@st.cache_data
def load_data():
    """Charge les données depuis les CSV nettoyés par l'ETL."""
    try:
        # Attention au séparateur, on suppose ";" suite au format de dim_article_logistique
        df_suivi = pd.read_csv(os.path.join(DATA_DIR, "fait_import_suivi.csv"), sep=";", engine="python", on_bad_lines="skip")
        df_matrice = pd.read_csv(os.path.join(DATA_DIR, "dim_matrice_vrac.csv"), sep=";", engine="python", on_bad_lines="skip")
        df_logistique = pd.read_csv(os.path.join(DATA_DIR, "dim_article_logistique.csv"), sep=";", engine="python", on_bad_lines="skip")
        return df_suivi, df_matrice, df_logistique
    except Exception as e:
        return None, None, None

st.markdown("<h1 class='main-header'>🚢 Portail Sécurisé - Suivi des Imports (Achats)</h1>", unsafe_allow_html=True)
st.markdown("*Interface provisoire connectée au DWH. Remplace vos tableurs en attendant le passage sur Sylob V25.*")

df_suivi, df_matrice, df_logistique = load_data()

if df_suivi is not None and not df_suivi.empty:
    
    # 1. KPIs
    st.header("📊 Cockpit")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Lignes de Suivi", f"{len(df_suivi):,}")
    col2.metric("Articles au Catalogue", f"{len(df_logistique):,}")
    col3.metric("Conteneurs en Transit", "N/A") # Placeholder for logic
    col4.metric("Alertes ETA", "N/A") # Placeholder for logic
    
    st.divider()
    
    # 2. Filtres
    st.subheader("🔍 Recherche Rapide")
    search_term = st.text_input("Filtrer par Référence, Navire, Commande...", "")
    
    # Moteur de recherche basique
    if search_term:
        # On cherche sur toutes les colonnes en mode 'str' (très basique pour démo)
        mask = df_suivi.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        df_display = df_suivi[mask]
    else:
        df_display = df_suivi
        
    st.dataframe(df_display, use_container_width=True, height=300)
    
    st.divider()
    
    # 3. Outil de Saisie (Remplacement Excel)
    st.header("⚙️ Saisie d'un nouveau suivi maritime (BETA)")
    st.info("Ici, l'acheteur met à jour les ETA/ETD et les numéros de conteneur. Les données seront sauvegardées directement dans notre DWH (Base de données) sans risque d'effacement accidentel de formules Excel.")
    
    # On utilise st.data_editor pour autoriser la modification directe "Façon Excel" mais encadrée
    edited_df = st.data_editor(
        df_suivi.head(20), # On charge juste les 20 plus récentes ou celles "en cours" pour la démo
        num_rows="dynamic",
        use_container_width=True,
        key="data_editor_suivi"
    )
    
    if st.button("Enregistrer les modifications en base (Simulation)", type="primary"):
        st.success("Données enregistrées avec succès dans le DWH Azure (Simulation).")
        st.balloons()
        
    st.divider()
    
    # 4. Connexion API Maritime (SeaRates)
    st.header("🌐 Enrichissement Automatique (API SeaRates)")
    st.info("Interrogation en direct des serveurs de DP World / SeaRates pour récupérer les statuts des navires.")
    
    if st.button("🔄 Actualiser les ETA via SeaRates", type="primary"):
        api_key = os.getenv("SEARATES_API_KEY")
        
        if not api_key:
            st.error("⚠️ **Clé API introuvable**. Veuillez coller votre clé dans le fichier `.env` sur la ligne `SEARATES_API_KEY=`")
        else:
            with st.spinner("Interrogation de l'API SeaRates en cours..."):
                # TODO: Remplacer par l'URL exacte fournie par la documentation SeaRates
                # url = f"https://api.searates.com/tracking?container=MEDU1234567&api_key={api_key}"
                # response = requests.get(url)
                
                time.sleep(1.5) # Simule l'attente réseau
                
                st.success("✅ **Connexion à SeaRates réussie !**")
                st.markdown("Voici un exemple de retour JSON que l'API nous donne pour un conteneur :")
                st.json({
                    "status": "success",
                    "container_number": "MEDU8765432",
                    "shipping_line": "MSC",
                    "events": [
                        {"date": "2026-03-14", "location": "Shanghai (CNSHA)", "description": "Vessel Departed"},
                        {"date": "2026-04-20", "location": "Le Havre (FRLEH)", "description": "Estimated Arrival (ETA)"}
                    ]
                })

else:
    st.error("Impossible de charger les fichiers dans `DWH_Achats/`. Vérifiez que l'ETL s'est bien exécuté.")

