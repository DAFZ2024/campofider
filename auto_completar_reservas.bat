@echo off
REM Script para ejecutar automáticamente la actualización de estados de reservas
REM Puedes programar este script con el Programador de Tareas de Windows

echo ========================================
echo Actualizando estados de reservas
echo ========================================
echo.

cd /d "c:\Users\du28f\Downloads\campofinder\campo finder\campo finder"

python marcar_completadas.py

echo.
echo ========================================
echo Proceso finalizado
echo ========================================
