# 🔌 Guía Rápida: Probar Conexión PostgreSQL Local

## 📋 Pasos para Probar la Conexión

### 1️⃣ Crear archivo .env con tus credenciales

1. **Copia el archivo de ejemplo:**
   ```bash
   copy .env.example .env
   ```

2. **Edita el archivo `.env`** y reemplaza con tus datos de Railway:
   - Ve a Railway.app
   - Click en tu base de datos PostgreSQL
   - Ve a "Variables" o "Connect"
   - Copia el valor de `DATABASE_URL`
   - Pégalo en `.env`

3. **Tu archivo `.env` debe verse así:**
   ```env
   DATABASE_URL=postgresql://postgres:TU_PASSWORD@containers-us-west-XXX.railway.app:XXXX/railway
   SECRET_KEY=dev-secret-key-for-testing
   RAILWAY_ENVIRONMENT=production
   ```

   ⚠️ **IMPORTANTE:** Descomenta la línea `RAILWAY_ENVIRONMENT=production`

---

### 2️⃣ Instalar dependencias (si no lo has hecho)

```bash
pip install python-dotenv psycopg2-binary
```

O instala todas las dependencias:
```bash
pip install -r requirements.txt
```

---

### 3️⃣ Ejecutar el test de conexión

```bash
python test_connection.py
```

---

## ✅ Resultado Esperado

Si todo está bien, verás:

```
🚀 Test de Conexión PostgreSQL - Railway
============================================================

🔍 Probando conexión a PostgreSQL de Railway...
============================================================
✓ URL convertida al formato correcto
📡 Conectando a: ...@containers-us-west-XXX.railway.app:XXXX/railway

⏳ Conectando...
✅ ¡Conexión exitosa!
📊 PostgreSQL Version: PostgreSQL 15.X

⚠️  No hay tablas creadas todavía
💡 Ejecuta: python init_db_postgres.py

============================================================
✅ ¡TODO FUNCIONA CORRECTAMENTE!
💡 Ahora puedes ejecutar init_db_postgres.py para crear las tablas
```

---

## 4️⃣ Crear las tablas en PostgreSQL

Una vez que la conexión funcione, ejecuta:

```bash
python init_db_postgres.py
```

Esto creará automáticamente todas las tablas en tu base de datos de Railway.

---

## ❌ Solución de Problemas

### Error: "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "DATABASE_URL not found"
- Verifica que creaste el archivo `.env`
- Verifica que copiaste correctamente la URL de Railway
- Asegúrate de estar en el directorio correcto

### Error: "connection refused" o "timeout"
- Verifica que la URL de Railway sea correcta
- Verifica tu conexión a internet
- Verifica que la base de datos esté activa en Railway

---

## 🎯 Siguiente Paso

Una vez que veas "✅ ¡TODO FUNCIONA CORRECTAMENTE!", ejecuta:

```bash
python init_db_postgres.py
```

Para crear todas las tablas automáticamente en PostgreSQL.
