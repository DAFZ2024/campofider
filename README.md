# 🏟️ Campo Finder - Sistema de Reservas de Canchas Deportivas

Sistema web para gestionar reservas de canchas deportivas en Soacha, Colombia.

## 🚀 Cómo Ejecutar el Proyecto

### Requisitos Previos
- Python 3.8+
- Node.js 14+ y npm

### 1️⃣ Instalación de Dependencias Python

```bash
# Instalar Flask y dependencias
pip install flask flask-login werkzeug
```

### 2️⃣ Inicializar la Base de Datos (Solo primera vez)

```bash
python init_db.py
```

Esto creará `usuariosdb.db` con todas las tablas y datos iniciales.

### 3️⃣ Instalar Dependencias de Tailwind (Solo primera vez)

```bash
npm install
```

### 4️⃣ Ejecutar el Proyecto

Necesitas **2 terminales abiertas**:

#### Terminal 1 - Tailwind CSS (modo watch)
```bash
npm run dev
```
Este comando observa cambios en tus archivos HTML y regenera el CSS automáticamente.

#### Terminal 2 - Servidor Flask
```bash
python app.py
```

### 5️⃣ Abrir en el Navegador

Abre tu navegador en: **http://localhost:5000**

## 📁 Estructura del Proyecto

```
campo finder/
├── app.py                  # Aplicación Flask principal
├── init_db.py             # Script de inicialización de BD
├── usuariosdb.db          # Base de datos SQLite3
├── usuariosdb.sql         # Schema SQL
├── package.json           # Configuración npm
├── tailwind.config.js     # Configuración Tailwind
├── templates/             # Templates HTML
│   ├── base.html         # Template base con Tailwind
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── catalogo.html
│   └── ...
├── static/
│   └── css/
│       ├── input.css     # Estilos Tailwind personalizados
│       └── output.css    # CSS compilado (generado auto)
└── admin/                # Módulo de administración
```

## 👥 Usuarios de Prueba

### Administradores
- **Email:** mendoza@campofinder.com | **Contraseña:** mendoza123
- **Email:** cupula@campofinder.com | **Contraseña:** cupula123
- **Email:** arenosa@campofinder.com | **Contraseña:** arenosa123

### Jugador
- **Email:** jesgondres10@gmail.com | **Contraseña:** (ver en BD)

## 🎨 Desarrollo con Tailwind CSS

### Comandos Disponibles

```bash
# Modo desarrollo (con watch)
npm run dev

# Compilar para producción
npm run build
```

### Usar Tailwind en Templates

```html
{% extends "base.html" %}

{% block title %}Mi Página{% endblock %}

{% block content %}
    <div class="container mx-auto">
        <h1 class="text-3xl font-bold text-primary-600">Título</h1>
        <button class="btn-primary">Reservar</button>
    </div>
{% endblock %}
```

### Componentes Personalizados

- `btn-primary` - Botón verde principal
- `btn-secondary` - Botón gris secundario
- `card` - Tarjeta básica
- `cancha-card` - Tarjeta de cancha con hover
- `input-field` - Campo de entrada estilizado

## 🔧 Tecnologías Utilizadas

- **Backend:** Flask (Python)
- **Base de Datos:** SQLite3
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Autenticación:** Flask-Login
- **Seguridad:** Werkzeug (hash de contraseñas)

## 📝 Funcionalidades

### Para Usuarios (Jugadores)
- ✅ Registro e inicio de sesión
- ✅ Ver catálogo de canchas
- ✅ Reservar canchas por horario
- ✅ Ver mis reservas
- ✅ Guardar canchas favoritas

### Para Administradores
- ✅ Registrar nuevas canchas
- ✅ Ver reservas de sus canchas
- ✅ Bloquear/liberar horarios
- ✅ Gestionar disponibilidad

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install flask flask-login werkzeug
```

### Error: "npm: command not found"
Instala Node.js desde: https://nodejs.org/

### La base de datos no existe
```bash
python init_db.py
```

### Los estilos no se aplican
```bash
# Regenerar CSS
npm run build
```

## 📚 Documentación Adicional

- `TAILWIND_GUIDE.md` - Guía completa de Tailwind CSS
- `TAILWIND_README.md` - Inicio rápido con Tailwind

## 📧 Contacto

Para más información: info@campofinder.com
