import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

base_dir = r"c:\Users\abezille\dev\MyReport\Service_Achat"
files = [f for f in os.listdir(base_dir) if f.endswith('.xlsx')]

report_path = r"c:\Users\abezille\dev\MyReport\excel_analysis_report.md"

with open(report_path, "w", encoding="utf-8") as f:
    f.write("# Rapport d'Analyse des Fichiers Excel - Service Achat\n\n")
    
    for file in files:
        filepath = os.path.join(base_dir, file)
        f.write(f"## Fichier : {file}\n\n")
        try:
            excel_file = pd.ExcelFile(filepath)
            sheet_names = excel_file.sheet_names
            f.write(f"**Onglets trouvés :** {', '.join(sheet_names)}\n\n")
            
            for sheet in sheet_names:
                f.write(f"### Onglet : `{sheet}`\n\n")
                try:
                    df = pd.read_excel(filepath, sheet_name=sheet, nrows=15, header=None)
                    
                    f.write(f"**Dimensions (échantillon) :** {df.shape[1]} colonnes\n\n")
                    f.write("**Aperçu des données (5 premières lignes) :**\n\n")
                    
                    # Remplacement de to_markdown par une extraction csv formatée
                    csv_string = df.head(5).to_csv(index=False, sep='|')
                    f.write("```text\n")
                    f.write(csv_string)
                    f.write("```\n\n")
                    
                except Exception as e:
                    f.write(f"*Impossible de lire les données :* {e}\n\n")
        except Exception as e:
            f.write(f"*Erreur lors de l'ouverture du fichier :* {e}\n\n")
