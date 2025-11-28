"""
Configuración de la base de datos
Soporta SQLite (desarrollo) y PostgreSQL (producción)
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (si existe)
load_dotenv()

# Detectar si estamos en producción (Railway) o desarrollo
IS_PRODUCTION = os.getenv('RAILWAY_ENVIRONMENT') is not None

if IS_PRODUCTION:
    # Configuración PostgreSQL para Railway
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Railway proporciona la URL en formato postgres://
    # pero psycopg2 necesita postgresql://
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    DB_CONFIG = {
        'type': 'postgresql',
        'url': DATABASE_URL
    }
else:
    # Configuración SQLite para desarrollo local
    DB_CONFIG = {
        'type': 'sqlite',
        'database': 'usuariosdb.db'
    }

# Configuración de la aplicación Flask
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = not IS_PRODUCTION
