from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import date
import sys
import os

# Add parent directory to path to import db if relative import fails, 
# but try relative import first if running as package
try:
    from ..db import get_db
except ImportError:
    # Fallback for some execution contexts
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from db import get_db

admin_usuarios = Blueprint('admin_usuarios', __name__, url_prefix='/admin', template_folder='../templates/admin')

@admin_usuarios.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin():
        flash('Acceso denegado', 'danger')
        return redirect(url_for('index'))
    
    db = get_db()
    cur = db.cursor()
    
    # Stats
    cur.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM usuarios WHERE rol='dueño'")
    total_duenos = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM canchas")
    total_canchas = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM reservas")
    total_reservas = cur.fetchone()[0]
    
    # Recent activity (optional, e.g., last 5 reservations)
    cur.execute("""
        SELECT r.id_reserva, u.nombre, c.nombre, r.fecha, r.horario 
        FROM reservas r
        JOIN usuarios u ON r.id_usuario = u.id
        JOIN canchas c ON r.cancha = c.nombre
        ORDER BY r.fecha DESC, r.horario DESC LIMIT 5
    """)
    recent_reservas = cur.fetchall()
    
    return render_template('dashboard_admin.html', 
                           total_usuarios=total_usuarios,
                           total_duenos=total_duenos,
                           total_canchas=total_canchas,
                           total_reservas=total_reservas,
                           recent_reservas=recent_reservas)

@admin_usuarios.route('/usuarios')
@login_required
def listar_usuarios():
    if not current_user.is_admin():
        flash('Acceso denegado', 'danger')
        return redirect(url_for('index'))
    
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, nombre, correo, edad, rol FROM usuarios")
    usuarios = cur.fetchall()
    
    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            'id': usuario[0],
            'nombre': usuario[1],
            'correo': usuario[2],
            'edad': usuario[3],
            'rol': usuario[4]
        })
    
    return render_template('usuarios.html', usuarios=usuarios_list)

@admin_usuarios.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    if not current_user.is_admin():
        flash('Acceso denegado', 'danger')
        return redirect(url_for('index'))
    
    db = get_db()
    cur = db.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        edad = request.form['edad']
        rol = request.form['rol']
        nueva_contraseña = request.form.get('nueva_contraseña')
        
        if nueva_contraseña:
            hashed_password = generate_password_hash(nueva_contraseña)
            cur.execute("""
                UPDATE usuarios 
                SET nombre=?, correo=?, edad=?, rol=?, contraseña=? 
                WHERE id=?
            """, (nombre, correo, edad, rol, hashed_password, id))
        else:
            cur.execute("""
                UPDATE usuarios 
                SET nombre=?, correo=?, edad=?, rol=? 
                WHERE id=?
            """, (nombre, correo, edad, rol, id))
            
        db.commit()
        flash('Usuario actualizado exitosamente', 'success')
        return redirect(url_for('admin_usuarios.listar_usuarios'))
    
    cur.execute("SELECT id, nombre, correo, edad, rol FROM usuarios WHERE id=?", (id,))
    usuario = cur.fetchone()
    
    if usuario:
        usuario_data = {
            'id': usuario[0],
            'nombre': usuario[1],
            'correo': usuario[2],
            'edad': usuario[3],
            'rol': usuario[4]
        }
        return render_template('editar_usuario.html', usuario=usuario_data)
    
    flash('Usuario no encontrado', 'error')
    return redirect(url_for('admin_usuarios.listar_usuarios'))

@admin_usuarios.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    if not current_user.is_admin():
        flash('Acceso denegado', 'danger')
        return redirect(url_for('index'))

    db = get_db()
    cur = db.cursor()
    # Primero eliminar registros relacionados
    cur.execute("DELETE FROM reservas WHERE id_usuario=?", (id,))
    cur.execute("DELETE FROM favoritos WHERE id_usuario=?", (id,))
    # Finalmente eliminar el usuario
    cur.execute("DELETE FROM usuarios WHERE id=?", (id,))
    db.commit()
    
    flash('Usuario eliminado exitosamente', 'success')
    return redirect(url_for('admin_usuarios.listar_usuarios'))

# --- Rutas para Canchas (Admin) ---
@admin_usuarios.route('/canchas')
@login_required
def listar_canchas():
    if not current_user.is_admin():
        flash('Acceso denegado', 'danger')
        return redirect(url_for('index'))
    
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT c.id_cancha, c.nombre, c.precio, c.direccion, c.imagen_url, u.nombre as dueno
        FROM canchas c
        LEFT JOIN usuarios u ON c.usuario_id = u.id
    """)
    canchas_raw = cur.fetchall()
    
    # Convert to dict for easier template access
    canchas = []
    for cancha in canchas_raw:
        canchas.append({
            'id_cancha': cancha[0],
            'nombre': cancha[1],
            'precio': cancha[2],
            'direccion': cancha[3],
            'imagen_url': cancha[4],
            'dueno': cancha[5]
        })
    
    return render_template('admin_canchas.html', canchas=canchas)

@admin_usuarios.route('/canchas/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cancha(id):
    if not current_user.is_admin():
        flash('Acceso denegado', 'danger')
        return redirect(url_for('index'))
    
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM reservas WHERE cancha = (SELECT nombre FROM canchas WHERE id_cancha=?)", (id,))
    cur.execute("DELETE FROM favoritos WHERE cancha = (SELECT nombre FROM canchas WHERE id_cancha=?)", (id,))
    cur.execute("DELETE FROM canchas WHERE id_cancha=?", (id,))
    db.commit()
    
    flash('Cancha eliminada exitosamente', 'success')
    return redirect(url_for('admin_usuarios.listar_canchas'))

# --- Rutas para Reservas (Admin) ---
@admin_usuarios.route('/reservas')
@login_required
def listar_reservas():
    if not current_user.is_admin():
        flash('Acceso denegado', 'danger')
        return redirect(url_for('index'))
    
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT r.id_reserva, r.cancha, r.fecha, r.horario, u.nombre as usuario
        FROM reservas r
        JOIN usuarios u ON r.id_usuario = u.id
        ORDER BY r.fecha DESC, r.horario DESC
    """)
    reservas = cur.fetchall()
    
    # Convertir las reservas a diccionarios para facilitar el acceso en el template
    reservas_procesadas = []
    for reserva in reservas:
        reservas_procesadas.append({
            'id_reserva': reserva[0],
            'cancha': reserva[1],
            'fecha': reserva[2],  # Mantener como viene de la BD (puede ser string o date)
            'horario': reserva[3],
            'usuario': reserva[4],
            'estado': 'activa'  # Por defecto todas son activas ya que no hay columna estado en la BD
        })
    
    # Pasar today como objeto date para comparación
    today = date.today()
    
    return render_template('admin_reservas.html', reservas=reservas_procesadas, today=today)