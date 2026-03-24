import os
import pandas as pd
import warnings
import pathlib

# Ignorer les warnings de pandas concernant les styles Excel
warnings.filterwarnings("ignore", category=UserWarning)

# Configuration des chemins dynamiques
BASE_DIR = pathlib.Path(r"c:\Users\abezille\dev\MyReport\Service_Achat")
OUTPUT_DIR = pathlib.Path(r"c:\Users\abezille\dev\MyReport\DWH_Achats")

def process_base_article(filepath):
    print(f"Traitement de {filepath.name}...")
    try:
        # L'onglet est "Feuil2" d'après l'analyse
        df = pd.read_excel(filepath, sheet_name="Feuil2", skiprows=0)
        output_path = OUTPUT_DIR / "dim_article_logistique.csv"
        df.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig")
        print(f" -> Exporté vers {output_path.name}")
    except Exception as e:
        print(f"Erreur sur {filepath.name}: {e}")

def process_import(filepath):
    print(f"Traitement de {filepath.name}...")
    try:
        # L'onglet "IMPORT 2025" a 3 lignes d'en-tête complexes. 
        # On lit à partir de la ligne 2 (index 1) qui semble contenir les noms de colonnes réels
        # d'après notre échantillon : "Intermédiaire", "Date envoi...", "MEN#"
        df = pd.read_excel(filepath, sheet_name="IMPORT 2025", header=3)
        # Nettoyage rapide des colonnes "Unnamed"
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        output_path = OUTPUT_DIR / "fait_import_suivi.csv"
        df.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig")
        print(f" -> Exporté vers {output_path.name}")
    except Exception as e:
        print(f"Erreur sur {filepath.name}: {e}")

def process_matrice_tb(filepath):
    print(f"Traitement de {filepath.name}...")
    try:
        # L'onglet "Lot-Vrac Produits uniques" a des en-têtes complexes sur 2 lignes
        df_vrac = pd.read_excel(filepath, sheet_name="Lot-Vrac Produits uniques", header=2)
        df_vrac = df_vrac.loc[:, ~df_vrac.columns.str.contains('^Unnamed')]
        output_path_vrac = OUTPUT_DIR / "dim_matrice_vrac.csv"
        df_vrac.to_csv(output_path_vrac, index=False, sep=";", encoding="utf-8-sig")
        print(f" -> (Vrac) Exporté vers {output_path_vrac.name}")
        
    except Exception as e:
        print(f"Erreur sur {filepath.name}: {e}")

def main():
    print("--- Démarrage de l'ETL Achats ---")
    
    # Création du dossier cible si inexistant
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    for file in BASE_DIR.glob("*.xlsx"):
        # Ignorer les modèles de saisie
        if "FOR-ACH-03-12" in file.name:
            print(f"Ignoré (Template) : {file.name}")
            continue
            
        if "Base article dimensions volume" in file.name:
            process_base_article(file)
        elif "IMPORT 2026" in file.name:
            process_import(file)
        elif "Matrice TB Import" in file.name:
            process_matrice_tb(file)
        else:
            print(f"Fichier non reconnu pour l'ETL : {file.name}")
            
    print("--- Fin de l'ETL Achats ---")

if __name__ == "__main__":
    main()
