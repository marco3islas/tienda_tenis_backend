from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Configuración de las bases de datos
sqlite_url = "sqlite:///instance/tenis.db"
postgres_url = "postgresql://marco:admin@localhost:5432/tienda_tenis"

sqlite_engine = create_engine(sqlite_url)
postgres_engine = create_engine(postgres_url)

SQLiteSession = sessionmaker(bind=sqlite_engine)
PostgresSession = sessionmaker(bind=postgres_engine)

def migrate_data():
    sqlite_session = SQLiteSession()
    postgres_session = PostgresSession()

    try:
        # Leer datos de SQLite
        productos = sqlite_session.execute(
            text("SELECT id, imagen, titulo, description, precio, tallas FROM productos")
        ).fetchall()

        print(f"📦 Se encontraron {len(productos)} registros en SQLite.")

        # Insertar en PostgreSQL
        for producto in productos:
            print(f"➡️ Insertando: {producto}")
            postgres_session.execute(
                text("""
                    INSERT INTO productos (id, imagen, titulo, "description", precio, tallas) 
                    VALUES (:id, :imagen, :titulo, :description, :precio, :tallas)
                """),
                {
                    "id": producto[0],          
                    "imagen": producto[1],      
                    "titulo": producto[2],      
                    "description": producto[3], 
                    "precio": producto[4],      
                    "tallas": producto[5]       
                }
            )
        
        postgres_session.commit()  # Asegurar que se guarden los cambios
        print("✅ Migración completada con éxito.")

    except Exception as e:
        print(f"❌ Error: {e}")
        postgres_session.rollback()

    finally:
        sqlite_session.close()
        postgres_session.close()

if __name__ == "__main__":
    migrate_data()
