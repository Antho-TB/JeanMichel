import psycopg2
import pandas as pd
import json

def investigate():
    env_vars = {}
    with open('c:\\Users\\abezille\\dev\\MyReport\\.env', 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                env_vars[k] = v

    try:
        conn = psycopg2.connect(
            host=env_vars['DB_HOST'],
            port=env_vars['DB_PORT'],
            dbname=env_vars['DB_NAME'],
            user=env_vars['DB_USER'],
            password=env_vars['DB_PASSWORD']
        )
        cur = conn.cursor()
        
        # 1. Investigate log_bdd_execution in the 3 log schemas
        log_schemas = [
            '"TARRERIAS_GENERALE_DE_DECOUPAGE_log"',
            '"TARRERIAS_SE_TARRERIAS_BONJEAN_log"',
            '"TARRERIAS_TARRERIAS_BONJEAN_ET_CIE_log"'
        ]
        
        print("--- LOG_BDD_EXECUTION ---")
        for schema in log_schemas:
            try:
                cur.execute(f"SELECT * FROM {schema}.log_bdd_execution ORDER BY start_etl_date DESC LIMIT 1;")
                row = cur.fetchone()
                if row:
                    cols = [desc[0] for desc in cur.description]
                    res = dict(zip(cols, row))
                    # formatting dates
                    for k,v in res.items():
                        if pd.api.types.is_datetime64_any_dtype(pd.Series([v])) or hasattr(v, 'isoformat'):
                            res[k] = str(v)
                    print(f"\n{schema}:")
                    print(json.dumps(res, indent=2))
            except Exception as e:
                conn.rollback()
                print(f"Error reading {schema}: {e}")

        # 2. Check the global _etl_history table
        print("\n--- _ETL_HISTORY ---")
        try:
            cur.execute("SELECT * FROM tarrerias._etl_history ORDER BY etl_start_date DESC LIMIT 1;")
            row = cur.fetchone()
            if row:
                cols = [desc[0] for desc in cur.description]
                res = dict(zip(cols, row))
                for k,v in res.items():
                    if hasattr(v, 'isoformat'):
                        res[k] = str(v)
                print(json.dumps(res, indent=2))
        except Exception as e:
            conn.rollback()
            print(f"Error reading tarrerias._etl_history: {e}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    investigate()
