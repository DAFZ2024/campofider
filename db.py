"""
Módulo de conexión a la base de datos
Soporta SQLite (desarrollo) y PostgreSQL (producción) con compatibilidad de sintaxis
"""
import sqlite3
from flask import g
from config import DB_CONFIG

# Importar psycopg2 solo si estamos en producción
if DB_CONFIG['type'] == 'postgresql':
    import psycopg2
    import psycopg2.extras

class UnifiedCursor:
    """
    Cursor unificado que traduce la sintaxis de SQLite (?) a PostgreSQL (%s)
    y asegura que los resultados sean accesibles tanto por índice como por nombre.
    """
    def __init__(self, original_cursor, db_type):
        self.cursor = original_cursor
        self.db_type = db_type

    def execute(self, query, params=None):
        # Traducir placeholder ? a %s si es PostgreSQL
        if self.db_type == 'postgresql' and '?' in query:
            query = query.replace('?', '%s')
        
        try:
            if params:
                return self.cursor.execute(query, params)
            else:
                return self.cursor.execute(query)
        except Exception as e:
            print(f"❌ Error SQL: {e}")
            print(f"   Query: {query}")
            raise e

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()
    
    def close(self):
        self.cursor.close()
    
    @property
    def lastrowid(self):
        return self.cursor.lastrowid
    
    @property
    def rowcount(self):
        return self.cursor.rowcount
    
    @property
    def description(self):
        return self.cursor.description
        
    def __getattr__(self, name):
        return getattr(self.cursor, name)

class ConnectionWrapper:
    """Wrapper para la conexión que devuelve nuestro cursor unificado"""
    def __init__(self, conn, db_type):
        self.conn = conn
        self.db_type = db_type
    
    def cursor(self):
        return UnifiedCursor(self.conn.cursor(), self.db_type)
    
    def commit(self):
        self.conn.commit()
    
    def rollback(self):
        self.conn.rollback()
    
    def close(self):
        self.conn.close()

def get_db():
    """Obtiene la conexión a la base de datos"""
    db = getattr(g, '_database', None)
    
    if db is None:
        if DB_CONFIG['type'] == 'postgresql':
            # Conexión PostgreSQL
            # Usamos DictCursor para permitir acceso por nombre, pero también soporta índices
            real_conn = psycopg2.connect(
                DB_CONFIG['url'],
                cursor_factory=psycopg2.extras.DictCursor
            )
            db = g._database = ConnectionWrapper(real_conn, 'postgresql')
        else:
            # Conexión SQLite
            real_conn = sqlite3.connect(DB_CONFIG['database'])
            real_conn.row_factory = sqlite3.Row
            db = g._database = ConnectionWrapper(real_conn, 'sqlite')
    
    return db

def close_connection(exception=None):
    """Cierra la conexión a la base de datos al finalizar la petición"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    """Helper function para ejecutar queries (usa el wrapper automáticamente)"""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute(query, params)
        
        result = None
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        
        if commit:
            db.commit()
            # Intentar obtener ID insertado de manera compatible
            if DB_CONFIG['type'] == 'sqlite':
                result = cursor.lastrowid
            else:
                # En PG, lastrowid no siempre funciona igual, pero rowcount sí
                result = cursor.rowcount
        
        return result
    
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
