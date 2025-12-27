from sqlalchemy import create_engine
import polars as pl
import datetime

SOURCE_CONN_STR = 'postgresql://user_source:password_source@source_db:5432/ecommerce_db'
DW_CONN_STR = 'postgresql://user_dw:password_dw@warehouse_db:5432/analytics_dw'

def run_etl():
    print("\n--- Iniciando ETL ---")
    
    # Conexiones
    source_engine = create_engine(SOURCE_CONN_STR)
    dw_engine = create_engine(DW_CONN_STR)
    
    # Paso A: EXTRACT
    print("1. Extrayendo datos...")
    query = """
        SELECT o.id as order_id, o.user_id, o.amount, o.status, o.created_at,
               u.country, u.name as user_name
        FROM orders o
        JOIN users u ON o.user_id = u.id
    """
    df = pl.read_database(query, source_engine)
    
    # Paso B: TRANSFORM
    # Regla de negocio: Solo nos interesan las ventas completadas para análisis
    # Regla de negocio: Queremos estandarizar los países a mayúsculas
    print("2. Transformando datos...")
    
    # Filtrar
    df_transformed = df[df['status'] == 'completed'].copy()
    
    # Transformar strings
    df_transformed['country'] = df_transformed['country'].str.upper()
    
    # Crear una columna de auditoría
    df_transformed['etl_loaded_at'] = datetime.now()

    # Agregación: Vamos a calcular un flag de "Venta VIP" si supera los 300
    df_transformed['is_vip_order'] = df_transformed['amount'] > 300

    # Paso C: LOAD
    print(f"3. Cargando {len(df_transformed)} registros al Data Warehouse...")
    
    # En un escenario real, usaríamos 'append' o estrategias de upsert.
    # Para este ejercicio, 'replace' crea la tabla de nuevo cada vez.
    df_transformed.write_database('fact_sales', dw_engine, if_table_exists='replace')
    
    print("--- ETL Finalizado con Éxito ---")


if __name__ == '__main__':
    run_etl()