import sqlite3
from werkzeug.security import generate_password_hash

# Conectar a la base de datos
conn = sqlite3.connect('usuariosdb.db')
cur = conn.cursor()

# Datos del administrador
nombre = "Administrador"
correo = "admin@campofinder.com"
edad = 30
contraseña = "admin123"
direccion = "Soacha, Colombia"
rol = "administrador"

# Verificar si el usuario ya existe
cur.execute("SELECT id FROM usuarios WHERE correo = ?", (correo,))
existing_user = cur.fetchone()

if existing_user:
    print(f"⚠️  El usuario con correo {correo} ya existe en la base de datos.")
    print(f"   ID del usuario: {existing_user[0]}")
else:
    # Hash de la contraseña
    hashed_password = generate_password_hash(contraseña)
    
    # Insertar el usuario administrador
    cur.execute("""
        INSERT INTO usuarios (nombre, correo, edad, contraseña, direccion, rol)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, correo, edad, hashed_password, direccion, rol))
    
    conn.commit()
    user_id = cur.lastrowid
    
    print("✅ Usuario administrador creado exitosamente!")
    print(f"   ID: {user_id}")
    print(f"   Nombre: {nombre}")
    print(f"   Correo: {correo}")
    print(f"   Contraseña: {contraseña}")
    print(f"   Rol: {rol}")

conn.close()
