"""
Script para marcar automáticamente las reservas como completadas
cuando su fecha y hora ya han pasado.
Soporta tanto SQLite (desarrollo) como PostgreSQL (producción)
"""
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def marcar_completadas():
    """Marca las reservas pendientes como completadas si su fecha/hora ya pasó"""
    
    database_url = os.getenv('DATABASE_URL')
    
    # Determinar si usar PostgreSQL o SQLite
    usar_postgres = database_url and database_url.strip()
    
    if usar_postgres:
        # Usar PostgreSQL
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        database_url = database_url.strip()
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        try:
            conn = psycopg2.connect(database_url)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            print("🔗 Conectado a PostgreSQL")
        except Exception as e:
            print(f"❌ Error al conectar a PostgreSQL: {e}")
            return False
    else:
        # Usar SQLite
        import sqlite3
        
        db_path = os.path.join(os.path.dirname(__file__), 'usuariosdb.db')
        if not os.path.exists(db_path):
            print(f"❌ Base de datos SQLite no encontrada: {db_path}")
            return False
        
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            print("🔗 Conectado a SQLite")
        except Exception as e:
            print(f"❌ Error al conectar a SQLite: {e}")
            return False
    
    try:
        # Obtener fecha y hora actual
        ahora = datetime.now()
        fecha_actual = ahora.date()
        hora_actual = ahora.time()
        
        print(f"📅 Fecha/Hora actual: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Buscar reservas pendientes cuya fecha ya pasó
        if usar_postgres:
            cursor.execute("""
                SELECT id_reserva, cancha, fecha, horario, estado
                FROM reservas
                WHERE estado = 'pendiente' 
                AND fecha < %s
            """, (fecha_actual,))
        else:
            cursor.execute("""
                SELECT id_reserva, cancha, fecha, horario, estado
                FROM reservas
                WHERE estado = 'pendiente' 
                AND fecha < date('now')
            """)
        
        reservas_pasadas = cursor.fetchall()
        
        if not reservas_pasadas:
            print("✅ No hay reservas pendientes para marcar como completadas")
            cursor.close()
            conn.close()
            return True
        
        print(f"🔄 Encontradas {len(reservas_pasadas)} reservas para actualizar:")
        
        # Actualizar cada reserva
        ids_actualizados = []
        for reserva in reservas_pasadas:
            id_reserva = reserva['id_reserva'] if usar_postgres else reserva[0]
            cancha = reserva['cancha'] if usar_postgres else reserva[1]
            fecha = reserva['fecha'] if usar_postgres else reserva[2]
            horario = reserva['horario'] if usar_postgres else reserva[3]
            
            print(f"  • ID {id_reserva}: {cancha} - {fecha} {horario}")
            ids_actualizados.append(id_reserva)
        
        # Actualizar todas las reservas en una sola consulta
        if usar_postgres:
            cursor.execute("""
                UPDATE reservas 
                SET estado = 'completada'
                WHERE estado = 'pendiente' 
                AND fecha < %s
            """, (fecha_actual,))
        else:
            cursor.execute("""
                UPDATE reservas 
                SET estado = 'completada'
                WHERE estado = 'pendiente' 
                AND fecha < date('now')
            """)
        
        conn.commit()
        
        print(f"✅ {len(ids_actualizados)} reservas marcadas como completadas")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar reservas: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando actualización de estados de reservas...")
    print("-" * 60)
    
    if marcar_completadas():
        print("\n✅ Proceso completado exitosamente")
        sys.exit(0)
    else:
        print("\n❌ Proceso completado con errores")
        sys.exit(1)
