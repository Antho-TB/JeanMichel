import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

base_dir = r"c:\Users\abezille\dev\MyReport\Service_Achat"
files = [f for f in os.listdir(base_dir) if f.endswith('.xlsx')]

print("=== Analyze Excel Files ===")
for file in files:
    filepath = os.path.join(base_dir, file)
    print(f"\n--- {file} ---")
    try:
        excel_file = pd.ExcelFile(filepath)
        sheet_names = excel_file.sheet_names
        print(f"Sheets: {sheet_names}")
        for sheet in sheet_names:
            try:
                # Read just enough to get columns and row count estimation
                df = pd.read_excel(filepath, sheet_name=sheet, nrows=5)
                # Count total rows roughly by reading only a specific column or using shape without data if possible.
                # Since getting exact count can be slow, I'll just output the columns
                print(f"  Sheet: '{sheet}'")
                print(f"    Columns ({len(df.columns)}): {list(df.columns)}")
            except Exception as e:
                print(f"    Could not read sheet '{sheet}': {e}")
    except Exception as e:
        print(f"Error opening {file}: {e}")
