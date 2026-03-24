import pandas as pd

try:
    df = pd.read_csv(r"c:\Users\abezille\dev\MyReport\DWH_Nouvelle_Version_Dictionnaire.csv", encoding="utf-8")
    tables_uniques = df['Table'].unique()
    tables_article = [t for t in tables_uniques if pd.notna(t) and 'article' in t.lower()]
    print("Tables contenant 'article':")
    for t in tables_article:
        print(f" - {t}")
except Exception as e:
    print(f"Erreur pandas: {e}")
