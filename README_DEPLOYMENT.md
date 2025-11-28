# 🏟️ CampoFinder - Sistema de Reservas de Canchas

Sistema web para la gestión y reserva de canchas deportivas, desarrollado con Flask y PostgreSQL.

## 🚀 Características

- ✅ **Registro y autenticación** de usuarios (Jugadores, Dueños, Administradores)
- ✅ **Gestión de canchas** (CRUD completo para dueños)
- ✅ **Sistema de reservas** con calendario
- ✅ **Favoritos** para guardar canchas preferidas
- ✅ **Dashboard personalizado** según el rol del usuario
- ✅ **Diseño moderno** con Tailwind CSS
- ✅ **Base de datos** SQLite (desarrollo) y PostgreSQL (producción)

## 📋 Requisitos

- Python 3.8+
- PostgreSQL (solo para producción)
- Node.js (para Tailwind CSS)

## 🛠️ Instalación Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/campofinder.git
cd campofinder
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Inicializar base de datos SQLite
```bash
python init_db.py
```

### 5. Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🌐 Despliegue en Railway (Producción)

### Preparación
1. Asegúrate de tener una cuenta en [Railway](https://railway.app)
2. Sube tu código a GitHub

### Pasos de Despliegue

1. **Crear proyecto en Railway**
   - Ve a Railway.app
   - Click en "New Project"
   - Selecciona "Provision PostgreSQL"

2. **Conectar repositorio**
   - Click en "New" → "GitHub Repo"
   - Selecciona tu repositorio

3. **Conectar base de datos**
   - En tu servicio web, ve a "Variables"
   - Click en "Reference" → Selecciona PostgreSQL
   - Esto agregará automáticamente `DATABASE_URL`

4. **Agregar variables de entorno**
   ```
   SECRET_KEY=tu-clave-secreta-super-segura
   RAILWAY_ENVIRONMENT=production
   ```

5. **Deploy automático**
   - Railway detectará automáticamente que es una app Flask
   - Ejecutará `init_db_postgres.py` para crear las tablas
   - Iniciará la aplicación con Gunicorn

### Verificar el Deploy
- Ve a "Deployments" para ver los logs
- Genera un dominio en "Settings" → "Domains"
- Accede a tu aplicación en la URL generada

## 📁 Estructura del Proyecto

```
campofinder/
├── admin/                  # Módulo de administración
│   └── admin_usuarios.py
├── static/                 # Archivos estáticos
│   ├── imagenes/          # Imágenes de canchas
│   └── canchas_uploads/   # Uploads de usuarios
├── templates/             # Plantillas HTML
├── app.py                 # Aplicación principal
├── config.py              # Configuración (SQLite/PostgreSQL)
├── db.py                  # Conexión a base de datos
├── init_db.py             # Inicializar SQLite (desarrollo)
├── init_db_postgres.py    # Inicializar PostgreSQL (producción)
├── export_data.py         # Exportar datos de SQLite
├── import_data.py         # Importar datos a PostgreSQL
├── requirements.txt       # Dependencias Python
├── Procfile               # Configuración Railway
└── railway.json           # Configuración Railway
```

## 🔄 Migración de Datos (Opcional)

Si quieres migrar datos existentes de SQLite a PostgreSQL:

### 1. Exportar datos de SQLite
```bash
python export_data.py
```

### 2. Importar a PostgreSQL
```bash
# Configurar DATABASE_URL
set DATABASE_URL=postgresql://usuario:password@host:puerto/database

# Importar
python import_data.py
```

## 👥 Roles de Usuario

### Jugador
- Explorar canchas disponibles
- Hacer reservas
- Gestionar favoritos
- Ver historial de reservas

### Dueño
- Gestionar sus propias canchas
- Ver reservas de sus canchas
- Estadísticas de ingresos

### Administrador
- Gestionar todos los usuarios
- Gestionar todas las canchas
- Ver todas las reservas

## 🔐 Seguridad

- Contraseñas hasheadas con Werkzeug
- Protección CSRF con Flask
- Variables de entorno para datos sensibles
- Validación de formularios

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask, Flask-Login
- **Base de Datos**: SQLite (dev), PostgreSQL (prod)
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Deploy**: Railway, Gunicorn
- **Control de Versiones**: Git, GitHub

## 📝 Variables de Entorno

### Desarrollo (Opcional)
```
SECRET_KEY=dev-secret-key
```

### Producción (Requeridas)
```
DATABASE_URL=postgresql://...  # Automática en Railway
SECRET_KEY=tu-clave-secreta
RAILWAY_ENVIRONMENT=production
```

## 🐛 Solución de Problemas

### Error: "DATABASE_URL not configured"
- Verifica que conectaste la base de datos PostgreSQL en Railway
- Revisa las variables de entorno

### Error: "relation does not exist"
- Las tablas no se crearon correctamente
- Revisa los logs del deploy
- Asegúrate que `init_db_postgres.py` se ejecutó

### Error al conectar
- Verifica que `psycopg2-binary` está en `requirements.txt`
- Revisa que `config.py` está importado en `app.py`

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado por [Tu Nombre]

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si tienes alguna pregunta o problema, por favor abre un issue en GitHub.

---

**¡Gracias por usar CampoFinder!** ⚽🏟️
