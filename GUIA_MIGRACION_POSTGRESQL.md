# 🚀 Guía Completa de Migración a PostgreSQL en Railway

## 📋 Resumen del Proceso

Esta guía te llevará paso a paso para migrar tu aplicación de SQLite a PostgreSQL en Railway. **NO necesitas escribir SQL manualmente** - todo se hace automáticamente con scripts Python.

---

## ✅ Paso 1: Preparación Local (Ya completado)

Los siguientes archivos ya fueron creados:

- ✅ `config.py` - Detecta automáticamente si usar SQLite o PostgreSQL
- ✅ `db.py` - Conexión a base de datos compatible con ambos
- ✅ `init_db_postgres.py` - Crea las tablas automáticamente en PostgreSQL
- ✅ `Procfile` - Configuración para Railway
- ✅ `railway.json` - Ejecuta el script de creación automáticamente

---

## 🌐 Paso 2: Crear Cuenta en Railway

1. Ve a [railway.app](https://railway.app)
2. Haz clic en **"Start a New Project"**
3. Inicia sesión con GitHub (recomendado)

---

## 🗄️ Paso 3: Crear Base de Datos PostgreSQL en Railway

### 3.1 Crear el Proyecto
1. En Railway, haz clic en **"New Project"**
2. Selecciona **"Provision PostgreSQL"**
3. Railway creará una base de datos PostgreSQL vacía automáticamente

### 3.2 Obtener las Credenciales
1. Haz clic en tu base de datos PostgreSQL
2. Ve a la pestaña **"Variables"**
3. Verás la variable `DATABASE_URL` - **NO necesitas copiarla manualmente**

---

## 📦 Paso 4: Subir tu Código a GitHub

### 4.1 Inicializar Git (si no lo has hecho)
```bash
git init
git add .
git commit -m "Migración a PostgreSQL preparada"
```

### 4.2 Crear Repositorio en GitHub
1. Ve a [github.com](https://github.com)
2. Crea un nuevo repositorio (por ejemplo: `campofinder`)
3. **NO inicialices con README**

### 4.3 Subir el código
```bash
git remote add origin https://github.com/TU_USUARIO/campofinder.git
git branch -M main
git push -u origin main
```

---

## 🚀 Paso 5: Desplegar en Railway

### 5.1 Conectar GitHub
1. En Railway, haz clic en **"New"** → **"GitHub Repo"**
2. Autoriza Railway a acceder a tus repositorios
3. Selecciona tu repositorio `campofinder`

### 5.2 Conectar la Base de Datos
1. En tu proyecto Railway, verás dos servicios:
   - Tu aplicación web
   - La base de datos PostgreSQL
2. Haz clic en tu aplicación web
3. Ve a **"Variables"**
4. Haz clic en **"Reference"** → Selecciona tu PostgreSQL
5. Railway agregará automáticamente `DATABASE_URL`

### 5.3 Agregar Variables de Entorno
En la sección de Variables, agrega:
```
SECRET_KEY=tu-clave-secreta-super-segura-aqui
RAILWAY_ENVIRONMENT=production
```

---

## 🎯 Paso 6: El Deploy Automático

Cuando hagas push a GitHub, Railway automáticamente:

1. ✅ Detecta que es una app Python
2. ✅ Instala las dependencias de `requirements.txt`
3. ✅ **Ejecuta `init_db_postgres.py`** (crea todas las tablas)
4. ✅ Inicia la aplicación con Gunicorn

### Ver el Progreso
1. En Railway, haz clic en tu aplicación
2. Ve a **"Deployments"**
3. Verás los logs en tiempo real

Deberías ver algo como:
```
🚀 Inicializando base de datos PostgreSQL...
🔗 Conectado a PostgreSQL
📋 Creando tablas...
✅ Esquema de base de datos creado exitosamente!
📊 Tablas creadas:
   ✓ usuarios: 0 registros
   ✓ canchas: 0 registros
   ✓ favoritos: 0 registros
   ✓ horarios_canchas: 0 registros
   ✓ reservas: 0 registros
```

---

## 🔧 Paso 7: Verificar que Funciona

### 7.1 Obtener la URL
1. En Railway, haz clic en tu aplicación
2. Ve a **"Settings"**
3. En **"Domains"**, haz clic en **"Generate Domain"**
4. Railway te dará una URL como: `https://tu-app.up.railway.app`

### 7.2 Probar la Aplicación
1. Abre la URL en tu navegador
2. Intenta registrarte como usuario
3. Verifica que puedes iniciar sesión

---

## 📊 Paso 8: Migrar Datos Existentes (Opcional)

Si quieres migrar los datos de tu SQLite local a PostgreSQL:

### 8.1 Exportar datos de SQLite
```bash
python export_data.py
```

Este script creará un archivo `data_export.json` con todos tus datos.

### 8.2 Importar a PostgreSQL
```bash
# Configurar DATABASE_URL localmente
set DATABASE_URL=postgresql://usuario:password@host:puerto/database

# Importar datos
python import_data.py
```

---

## 🎉 ¡Listo!

Tu aplicación ahora está corriendo en Railway con PostgreSQL. Los beneficios:

- ✅ **Escalable**: PostgreSQL maneja múltiples usuarios simultáneos
- ✅ **Automático**: Las tablas se crean solas en cada deploy
- ✅ **Gratis**: Railway ofrece $5 de crédito mensual gratis
- ✅ **Sin SQL manual**: Todo se maneja con Python

---

## 🔄 Desarrollo Local

Para seguir desarrollando localmente:

1. Tu app seguirá usando SQLite automáticamente
2. Cuando hagas push a GitHub, Railway usará PostgreSQL
3. **No necesitas cambiar nada en tu código**

---

## 🆘 Solución de Problemas

### Error: "DATABASE_URL not configured"
- Verifica que conectaste la base de datos PostgreSQL a tu app en Railway
- Ve a Variables y confirma que `DATABASE_URL` existe

### Error: "relation does not exist"
- Las tablas no se crearon correctamente
- Revisa los logs del deploy en Railway
- Asegúrate que `init_db_postgres.py` se ejecutó

### Error al conectar
- Verifica que `psycopg2-binary` está en `requirements.txt`
- Revisa que `config.py` está importado correctamente en `app.py`

---

## 📞 Próximos Pasos

1. ✅ Crear cuenta en Railway
2. ✅ Crear base de datos PostgreSQL
3. ✅ Subir código a GitHub
4. ✅ Conectar Railway con GitHub
5. ✅ Ver cómo se crean las tablas automáticamente
6. ✅ ¡Disfrutar tu app en producción!

---

**¿Necesitas ayuda?** Revisa los logs en Railway o consulta la documentación.
