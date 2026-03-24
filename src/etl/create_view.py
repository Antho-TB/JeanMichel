import psycopg2
import sys

def create_view():
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
        conn.autocommit = True
        cur = conn.cursor()
        
        create_view_sql = """
        CREATE OR REPLACE VIEW tarrerias.vue_monitoring_etl AS
        WITH last_global_run AS (
            SELECT etl_start_date, total_size_pretty, total_etl_execution_time
            FROM tarrerias._etl_history
            ORDER BY etl_start_date DESC
            LIMIT 1
        ),
        entity_logs AS (
            SELECT * FROM (
                SELECT 
                    'Générale de Découpage' as entite,
                    status as statut,
                    start_etl_date as date_lancement_global,
                    end_dwh_date as date_fin_traitement
                FROM "TARRERIAS_GENERALE_DE_DECOUPAGE_log".log_bdd_execution
                ORDER BY start_etl_date DESC LIMIT 1
            ) a
            
            UNION ALL
            
            SELECT * FROM (
                SELECT 
                    'SE' as entite,
                    status as statut,
                    start_etl_date as date_lancement_global,
                    end_dwh_date as date_fin_traitement
                FROM "TARRERIAS_SE_TARRERIAS_BONJEAN_log".log_bdd_execution
                ORDER BY start_etl_date DESC LIMIT 1
            ) b
            
            UNION ALL
            
            SELECT * FROM (
                SELECT 
                    'Cie' as entite,
                    status as statut,
                    start_etl_date as date_lancement_global,
                    end_dwh_date as date_fin_traitement
                FROM "TARRERIAS_TARRERIAS_BONJEAN_ET_CIE_log".log_bdd_execution
                ORDER BY start_etl_date DESC LIMIT 1
            ) c
        )
        SELECT 
            e.entite AS "Entité",
            g.etl_start_date AS "Date_Lancement_ETL",
            e.date_fin_traitement AS "Fin_Traitement_Entité",
            e.statut AS "Statut_Traitement",
            g.total_size_pretty AS "Volumétrie_Globale"
        FROM last_global_run g
        LEFT JOIN entity_logs e ON e.date_lancement_global = g.etl_start_date;
        """
        
        print("Creating view...")
        cur.execute(create_view_sql)
        print("View 'tarrerias.vue_monitoring_etl' created successfully!")
        
        # Test the view
        cur.execute('SELECT * FROM tarrerias.vue_monitoring_etl')
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        print(f"\nTest query headers: {cols}")
        for r in rows:
            print(r)
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    create_view()
