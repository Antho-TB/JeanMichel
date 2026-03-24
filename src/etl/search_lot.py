import pandas as pd

df = pd.read_csv('c:/Users/abezille/dev/MyReport/DWH_Nouvelle_Version_Dictionnaire.csv')
hits = df[df['Attribut'].astype(str).str.contains('lot|quantite|livraisonvente', case=False, na=False)]

vente_tables = hits[hits['Table'].astype(str).str.contains('livraison|vente', case=False, na=False)]

# Group by table to see fields
for table, group in vente_tables.groupby('Table'):
    fields = group['Attribut'].drop_duplicates().tolist()
    # Filter only those that are likely relevant to what we seek
    relevant = [f for f in fields if any(k in f.lower() for k in ['lot', 'quantite', 'livraison'])]
    if relevant:
        print(f"Table: {table}")
        for f in relevant:
            print(f"  - {f}")
