from sqlalchemy import create_engine
from faker import Faker
import polars as pl
import random

SOURCE_CONN_STR = 'postgresql://user_source:password_source@source_db:5432/ecommerce_db'

fake = Faker()

# 1. SIMULACIÓN: GENERADOR DE DATOS (SOURCE) ---
def generate_source_data(engine, num_users=100, num_orders=500):
    print("--- Generando datos simulados en Source DB ---")
    
    # Crear tablas si no existen
    with engine.connect() as conn:
        conn.exec_driver_sql("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                country VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                amount DECIMAL(10, 2),
                status VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    
    # Generar Usuarios falsos
    users_data = []
    for _ in range(num_users):
        users_data.append({
            'name': fake.name(),
            'email': fake.email(),
            'country': fake.country()
        })
    
    # Writing to DB
    pl.DataFrame(users_data).write_database(
        table_name='users',
        connection=engine,
        if_table_exists='append'
    )

    # Generar Órdenes falsas
    orders_data = []
    for _ in range(num_orders):
        orders_data.append({
            'user_id': random.randint(1, num_users),
            'amount': round(random.uniform(10.0, 500.0), 2),
            'status': random.choice(['completed', 'pending', 'cancelled', 'refunded'])
        })
    
    pl.DataFrame(orders_data).write_database(
        table_name='orders',
        connection=engine,
        if_table_exists='append'
    )
    
    print("Datos generados exitosamente.")


if __name__ == '__main__':
    source_engine = create_engine(SOURCE_CONN_STR)
    # Solo generamos datos si las tablas no existen o están vacías (simplificado)
    try:
        generate_source_data(source_engine)
    except Exception as e:
        print(f"Nota: {e}")