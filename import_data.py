"""
Script opcional para importar datos desde JSON a PostgreSQL
Ejecuta esto DESPUÉS de crear el esquema con init_db_postgres.py
"""
import os
import json
import psycopg2
from psycopg2 import sql

def import_data_to_postgres():
    """Importa datos desde data_export.json a PostgreSQL"""
    
    # Verificar que existe el archivo de datos
    if not os.path.exists('data_export.json'):
        print("❌ Error: No se encontró 'data_export.json'")
        print("💡 Primero ejecuta export_data.py para exportar los datos")
        return False
    
    # Obtener URL de la base de datos
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ Error: DATABASE_URL no está configurada")
        print("💡 Configura la variable de entorno DATABASE_URL")
        print("   Ejemplo: set DATABASE_URL=postgresql://user:pass@host:port/db")
        return False
    
    # Convertir formato si es necesario
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        # Leer datos del JSON
        with open('data_export.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Conectar a PostgreSQL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("📥 Importando datos a PostgreSQL...")
        print("-" * 60)
        
        # Orden de importación (respetando foreign keys)
        import_order = ['usuarios', 'canchas', 'favoritos', 'horarios_canchas', 'reservas']
        
        for table in import_order:
            if table not in data or not data[table]:
                print(f"   ⚠️  {table}: Sin datos para importar")
                continue
            
            records = data[table]
            
            if not records:
                continue
            
            # Obtener columnas del primer registro
            columns = list(records[0].keys())
            
            # Crear query de inserción
            placeholders = ', '.join(['%s'] * len(columns))
            columns_str = ', '.join(columns)
            
            insert_query = f"""
                INSERT INTO {table} ({columns_str})
                VALUES ({placeholders})
                ON CONFLICT DO NOTHING
            """
            
            # Insertar registros
            inserted = 0
            for record in records:
                try:
                    values = [record[col] for col in columns]
                    cursor.execute(insert_query, values)
                    inserted += 1
                except Exception as e:
                    print(f"      ⚠️  Error en registro: {e}")
                    continue
            
            conn.commit()
            print(f"   ✓ {table}: {inserted}/{len(records)} registros importados")
        
        # Actualizar secuencias (para que los IDs autoincrementales continúen correctamente)
        print("\n🔄 Actualizando secuencias...")
        
        sequences = {
            'usuarios': 'usuarios_id_seq',
            'canchas': 'canchas_id_cancha_seq',
            'favoritos': 'favoritos_id_favorito_seq',
            'horarios_canchas': 'horarios_canchas_id_horario_seq',
            'reservas': 'reservas_id_reserva_seq'
        }
        
        for table, sequence in sequences.items():
            try:
                cursor.execute(f"""
                    SELECT setval('{sequence}', 
                        COALESCE((SELECT MAX(id) FROM {table}), 1), 
                        true
                    )
                """)
                print(f"   ✓ Secuencia actualizada: {sequence}")
            except:
                # Intentar con nombre de columna diferente
                try:
                    id_column = 'id_cancha' if table == 'canchas' else \
                               'id_favorito' if table == 'favoritos' else \
                               'id_horario' if table == 'horarios_canchas' else \
                               'id_reserva' if table == 'reservas' else 'id'
                    
                    cursor.execute(f"""
                        SELECT setval('{sequence}', 
                            COALESCE((SELECT MAX({id_column}) FROM {table}), 1), 
                            true
                        )
                    """)
                    print(f"   ✓ Secuencia actualizada: {sequence}")
                except Exception as e:
                    print(f"   ⚠️  No se pudo actualizar {sequence}: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ ¡Datos importados exitosamente!")
        print("💡 Tu base de datos PostgreSQL ahora tiene todos los datos")
        return True
        
    except Exception as e:
        print(f"❌ Error al importar datos: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Importando datos a PostgreSQL...")
    print("=" * 60)
    
    if import_data_to_postgres():
        print("\n✅ ¡Migración completada!")
    else:
        print("\n❌ La migración falló")
