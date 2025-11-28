@echo off
echo ========================================
echo   Campo Finder - Iniciando Proyecto
echo ========================================
echo.

REM Verificar si existe la base de datos
if not exist usuariosdb.db (
    echo [INFO] Base de datos no encontrada. Inicializando...
    python init_db.py
    echo.
)

REM Iniciar Tailwind en segundo plano
echo [INFO] Iniciando Tailwind CSS en modo watch...
start "Tailwind CSS" cmd /k npm run dev

REM Esperar 2 segundos
timeout /t 2 /nobreak >nul

REM Iniciar Flask
echo [INFO] Iniciando servidor Flask...
echo.
echo ========================================
echo   Servidor corriendo en:
echo   http://localhost:5000
echo ========================================
echo.
python app.py

pause
