from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from db import get_db, close_connection
from admin.admin_usuarios import admin_usuarios
from config import SECRET_KEY, DEBUG

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'canchas_uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Asegurar que el directorio de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

# Registrar Blueprint de administrador
app.register_blueprint(admin_usuarios)

# Cerrar la conexión a la base de datos al finalizar cada petición
@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)

# Modelo de Usuario
class Usuario(UserMixin):
    def __init__(self, id, nombre, correo, edad, contraseña, direccion, rol):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.edad = edad
        self.contraseña = contraseña
        self.direccion = direccion
        self.rol = rol

    def is_admin(self):
        return self.rol == 'administrador'

    def is_owner(self):
        return self.rol == 'dueño'

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, nombre, correo, edad, contraseña, direccion, rol FROM usuarios WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if user:
        return Usuario(user[0], user[1], user[2], user[3], user[4], user[5], user[6])
    return None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ---------------------- REGISTRO ----------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            correo = request.form['correo']
            edad = request.form['edad']
            contraseña = request.form['contraseña']
            direccion = request.form.get('direccion')
            rol = request.form.get('rol', 'usuario')
            if isinstance(rol, str):
                rol = rol.strip().lower()
            allowed_roles = {'usuario', 'dueño'}
            if rol not in allowed_roles:
                rol = 'usuario'

            if len(contraseña) < 6:
                flash('La contraseña debe tener al menos 6 caracteres', 'error')
                return render_template('register.html')
            
            if int(edad) < 18:
                flash('Debes ser mayor de 18 años para registrarte', 'error')
                return render_template('register.html')

            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT id FROM usuarios WHERE correo = ?", (correo,))
            user_exists = cur.fetchone()
            
            if user_exists:
                flash('Este correo ya está registrado', 'error')
                return render_template('register.html')

            hashed = generate_password_hash(contraseña)

            cur.execute("""
                INSERT INTO usuarios (nombre, correo, edad, contraseña, direccion, rol)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, correo, edad, hashed, direccion, rol))
            
            db.commit()
            user_id = cur.lastrowid

            new_user = Usuario(id=user_id, nombre=nombre, correo=correo, edad=edad, contraseña=hashed, direccion=direccion, rol=rol)
            login_user(new_user)
            
            flash(f'¡Bienvenido {nombre}! Te has registrado exitosamente como {rol}', 'success')

            if rol == 'administrador':
                return redirect(url_for('dashboard_admin'))
            elif rol == 'dueño':
                return redirect(url_for('dashboard_dueño'))
            else:
                return redirect(url_for('dashboard_usuario'))

        except Exception as e:
            get_db().rollback()
            print(f"Error en registro: {str(e)}") 
            flash('Error al procesar el registro. Por favor, intenta de nuevo.', 'error')
            return render_template('register.html')

    return render_template('register.html')

# ---------------------- LOGIN ----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.rol == 'administrador':
            return redirect(url_for('dashboard_admin'))
        if current_user.rol == 'dueño':
            return redirect(url_for('dashboard_dueño'))
        return redirect(url_for('dashboard_usuario'))

    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id, nombre, correo, edad, contraseña, direccion, rol FROM usuarios WHERE correo=?", (correo,))
        user = cur.fetchone()

        if user and check_password_hash(user[4], contraseña):
            usuario = Usuario(user[0], user[1], user[2], user[3], user[4], user[5], user[6])
            login_user(usuario)
            flash(f'¡Bienvenido {usuario.nombre}!', 'success')
            if usuario.rol == 'administrador':
                return redirect(url_for('dashboard_admin'))
            if usuario.rol == 'dueño':
                return redirect(url_for('dashboard_dueño'))
            return redirect(url_for('dashboard_usuario'))
        else:
            flash('Credenciales inválidas. Por favor, verifica tu correo y contraseña.', 'error')

    return render_template('login.html')

# ---------------------- RUTAS PÚBLICAS ----------------------

@app.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    favoritas = []
    if current_user.is_authenticated:
        cur.execute("""
            SELECT c.nombre, c.descripcion, c.imagen_url
            FROM favoritos f
            JOIN canchas c ON f.cancha = c.nombre
            WHERE f.id_usuario = ?
        """, (current_user.id,))
        favoritas_db = cur.fetchall()
        for c in favoritas_db:
            favoritas.append({
                'nombre': c[0],
                'descripcion': c[1],
                'imagen': c[2].split(',')[0] if c[2] else None
            })
    cur.execute("SELECT nombre, descripcion, imagen_url, precio FROM canchas WHERE usuario_id IS NOT NULL")
    canchas_db = cur.fetchall()
    canchas = []
    for c in canchas_db:
        img_path = c[2].split(',')[0] if c[2] else 'imagenes/cancha1.png'
        if img_path.startswith('static/'):
            img_path = img_path.replace('static/', '', 1)
        canchas.append((c[0], c[1], img_path, c[3]))
    return render_template('home.html', canchas=canchas, favoritas=favoritas)

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# ---------------------- DASHBOARD DUEÑO ----------------------
@app.route('/dashboard_dueño')
@login_required
def dashboard_dueño():
    if not current_user.is_owner():
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    db = get_db()
    cur = db.cursor()
    
    # Obtener canchas del dueño
    cur.execute("""
        SELECT id_cancha, nombre, precio, descripcion, imagen_url, direccion
        FROM canchas
        WHERE usuario_id = ?
        ORDER BY id_cancha DESC
    """, (current_user.id,))
    canchas = cur.fetchall()
    
    # Contar total de canchas
    total_canchas = len(canchas)
    
    # Contar reservas totales
    cur.execute("""
        SELECT COUNT(*) 
        FROM reservas r
        JOIN canchas c ON r.cancha = c.nombre
        WHERE c.usuario_id = ?
    """, (current_user.id,))
    total_reservas = cur.fetchone()[0]
    
    # Obtener reservas recientes
    cur.execute("""
        SELECT r.id_reserva, r.cancha, r.fecha, r.horario, r.numero, r.mensaje,
               u.nombre as usuario_nombre, u.correo as usuario_correo
        FROM reservas r
        JOIN canchas c ON r.cancha = c.nombre
        JOIN usuarios u ON r.id_usuario = u.id
        WHERE c.usuario_id = ?
        ORDER BY r.fecha DESC, r.horario DESC
        LIMIT 5
    """, (current_user.id,))
    reservas_recientes = cur.fetchall()
    
    return render_template('dueño_canchas.html', 
                         canchas=canchas,
                         total_canchas=total_canchas,
                         total_reservas=total_reservas,
                         reservas_recientes=reservas_recientes)

@app.route('/dueño/canchas/agregar', methods=['GET', 'POST'])
@login_required
def dueno_agregar_cancha():
    if not current_user.is_owner():
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            precio = request.form['precio']
            descripcion = request.form['descripcion']
            direccion = request.form.get('direccion', '')
            
            imagen_url = ''
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{nombre.replace(' ', '_')}_{current_user.id}.{filename.rsplit('.', 1)[1].lower()}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    imagen_url = f"static/canchas_uploads/{filename}"
            
            db = get_db()
            cur = db.cursor()
            cur.execute("""
                INSERT INTO canchas (nombre, precio, descripcion, imagen_url, direccion, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, precio, descripcion, imagen_url, direccion, current_user.id))
            db.commit()
            
            flash(f'Cancha "{nombre}" agregada exitosamente', 'success')
            return redirect(url_for('dashboard_dueño'))
            
        except Exception as e:
            get_db().rollback()
            print(f"Error al agregar cancha: {str(e)}")
            flash('Error al agregar la cancha. Por favor, intenta de nuevo.', 'error')
    
    return render_template('dueño_agregar_cancha.html')

@app.route('/dueño/canchas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def dueno_editar_cancha(id):
    if not current_user.is_owner():
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    db = get_db()
    cur = db.cursor()
    
    cur.execute("SELECT * FROM canchas WHERE id_cancha = ? AND usuario_id = ?", (id, current_user.id))
    cancha = cur.fetchone()
    
    if not cancha:
        flash('Cancha no encontrada o no tienes permiso para editarla', 'error')
        return redirect(url_for('dashboard_dueño'))
    
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            precio = request.form['precio']
            descripcion = request.form['descripcion']
            direccion = request.form.get('direccion', '')
            
            imagen_url = cancha['imagen_url']
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{nombre.replace(' ', '_')}_{current_user.id}.{filename.rsplit('.', 1)[1].lower()}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    imagen_url = f"static/canchas_uploads/{filename}"
            
            cur.execute("""
                UPDATE canchas 
                SET nombre = ?, precio = ?, descripcion = ?, imagen_url = ?, direccion = ?
                WHERE id_cancha = ? AND usuario_id = ?
            """, (nombre, precio, descripcion, imagen_url, direccion, id, current_user.id))
            db.commit()
            
            flash(f'Cancha "{nombre}" actualizada exitosamente', 'success')
            return redirect(url_for('dashboard_dueño'))
            
        except Exception as e:
            get_db().rollback()
            print(f"Error al editar cancha: {str(e)}")
            flash('Error al editar la cancha. Por favor, intenta de nuevo.', 'error')
    
    return render_template('dueño_editar_cancha.html', cancha=cancha)

@app.route('/dueño/canchas/eliminar/<int:id>', methods=['POST'])
@login_required
def dueno_eliminar_cancha(id):
    if not current_user.is_owner():
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    db = get_db()
    cur = db.cursor()
    
    cur.execute("SELECT nombre FROM canchas WHERE id_cancha = ? AND usuario_id = ?", (id, current_user.id))
    cancha = cur.fetchone()
    
    if not cancha:
        flash('Cancha no encontrada o no tienes permiso para eliminarla', 'error')
        return redirect(url_for('dashboard_dueño'))
    
    try:
        cur.execute("DELETE FROM canchas WHERE id_cancha = ? AND usuario_id = ?", (id, current_user.id))
        db.commit()
        flash(f'Cancha "{cancha[0]}" eliminada exitosamente', 'success')
    except Exception as e:
        get_db().rollback()
        print(f"Error al eliminar cancha: {str(e)}")
        flash('Error al eliminar la cancha', 'error')
    
    return redirect(url_for('dashboard_dueño'))

@app.route('/dueño/reservas')
@login_required
def dueno_reservas():
    if not current_user.is_owner():
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT r.id_reserva, r.cancha, r.fecha, r.horario, r.numero, r.mensaje,
               u.nombre as usuario_nombre, u.correo as usuario_correo
        FROM reservas r
        JOIN canchas c ON r.cancha = c.nombre
        JOIN usuarios u ON r.id_usuario = u.id
        WHERE c.usuario_id = ?
        ORDER BY r.fecha DESC, r.horario DESC
    """, (current_user.id,))
    reservas = cur.fetchall()
    
    return render_template('dueño_reservas.html', reservas=reservas)

@app.route('/perfil_dueño', methods=['GET', 'POST'])
@login_required
def perfil_dueño():
    if not current_user.is_owner():
        flash('Acceso denegado', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            correo = request.form['correo']
            edad = request.form['edad']
            direccion = request.form.get('direccion', '')
            nueva_contraseña = request.form.get('nueva_contraseña')
            
            db = get_db()
            cur = db.cursor()
            
            if nueva_contraseña and len(nueva_contraseña) >= 6:
                hashed = generate_password_hash(nueva_contraseña)
                cur.execute("""
                    UPDATE usuarios 
                    SET nombre = ?, correo = ?, edad = ?, direccion = ?, contraseña = ?
                    WHERE id = ?
                """, (nombre, correo, edad, direccion, hashed, current_user.id))
            else:
                cur.execute("""
                    UPDATE usuarios 
                    SET nombre = ?, correo = ?, edad = ?, direccion = ?
                    WHERE id = ?
                """, (nombre, correo, edad, direccion, current_user.id))
            
            db.commit()
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('perfil_dueño'))
            
        except Exception as e:
            get_db().rollback()
            print(f"Error al actualizar perfil: {str(e)}")
            flash('Error al actualizar el perfil', 'error')
    
    return render_template('perfil_dueño.html')

# ---------------------- DASHBOARD USUARIO ----------------------

@app.route('/dashboard_usuario')
@login_required
def dashboard_usuario():
    db = get_db()
    cur = db.cursor()
    
    cur.execute("SELECT COUNT(*) FROM reservas WHERE id_usuario = ?", (current_user.id,))
    total_reservas = cur.fetchone()[0]
    
    cur.execute("""
        SELECT COUNT(*) FROM reservas 
        WHERE id_usuario = ? AND fecha >= date('now')
    """, (current_user.id,))
    proximas_reservas = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM favoritos WHERE id_usuario = ?", (current_user.id,))
    total_favoritos = cur.fetchone()[0]
    
    cur.execute("""
        SELECT r.id_reserva, r.cancha, r.fecha, r.horario, c.precio, c.imagen_url
        FROM reservas r
        JOIN canchas c ON r.cancha = c.nombre
        WHERE r.id_usuario = ? AND r.fecha >= date('now')
        ORDER BY r.fecha ASC, r.horario ASC
        LIMIT 3
    """, (current_user.id,))
    proximas_reservas_list = cur.fetchall()
    
    cur.execute("""
        SELECT DISTINCT c.id_cancha, c.nombre, c.precio, c.imagen_url, c.descripcion, c.direccion
        FROM canchas c
        WHERE c.usuario_id IS NOT NULL
        ORDER BY c.id_cancha DESC
        LIMIT 6
    """)
    canchas_recomendadas = cur.fetchall()
    
    return render_template('dashboard_usuario.html',
                         total_reservas=total_reservas,
                         proximas_reservas=proximas_reservas,
                         total_favoritos=total_favoritos,
                         proximas_reservas_list=proximas_reservas_list,
                         canchas_recomendadas=canchas_recomendadas)

@app.route('/usuario/explorar')
@login_required
def usuario_explorar():
    db = get_db()
    cur = db.cursor()
    
    cur.execute("""
        SELECT c.id_cancha, c.nombre, c.precio, c.descripcion, c.imagen_url, c.direccion,
               EXISTS(SELECT 1 FROM favoritos f WHERE f.cancha = c.nombre AND f.id_usuario = ?) as es_favorito
        FROM canchas c
        WHERE c.usuario_id IS NOT NULL
        ORDER BY c.id_cancha DESC
    """, (current_user.id,))
    canchas = cur.fetchall()
    
    return render_template('usuario_explorar.html', canchas=canchas)

@app.route('/usuario/reservar/<int:id_cancha>', methods=['GET', 'POST'])
@login_required
def usuario_reservar(id_cancha):
    db = get_db()
    cur = db.cursor()
    
    cur.execute("""
        SELECT id_cancha, nombre, precio, descripcion, imagen_url, direccion
        FROM canchas
        WHERE id_cancha = ?
    """, (id_cancha,))
    cancha = cur.fetchone()
    
    if not cancha:
        flash('Cancha no encontrada', 'error')
        return redirect(url_for('usuario_explorar'))
    
    if request.method == 'POST':
        try:
            fecha = request.form['fecha']
            horario = request.form['horario']
            numero = request.form.get('numero', '')
            mensaje = request.form.get('mensaje', '')
            
            fecha_reserva = datetime.strptime(fecha, '%Y-%m-%d').date()
            if fecha_reserva < datetime.now().date():
                flash('No puedes reservar en una fecha pasada', 'error')
                return render_template('usuario_reservar.html', cancha=cancha)
            
            cur.execute("""
                INSERT INTO reservas (id_usuario, cancha, fecha, horario, numero, mensaje)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (current_user.id, cancha['nombre'], fecha, horario, numero, mensaje))
            db.commit()
            
            flash(f'¡Reserva confirmada para {cancha["nombre"]} el {fecha} a las {horario}!', 'success')
            return redirect(url_for('usuario_mis_reservas'))
            
        except Exception as e:
            get_db().rollback()
            print(f"Error al crear reserva: {str(e)}")
            flash('Error al procesar la reserva. Por favor, intenta de nuevo.', 'error')
    
    return render_template('usuario_reservar.html', cancha=cancha)

@app.route('/usuario/mis-reservas')
@login_required
def usuario_mis_reservas():
    db = get_db()
    cur = db.cursor()
    
    cur.execute("""
        SELECT r.id_reserva, r.cancha, r.fecha, r.horario, r.numero, r.mensaje,
               c.precio, c.imagen_url, c.direccion,
               CASE 
                   WHEN r.fecha < date('now') THEN 'Completada'
                   WHEN r.fecha = date('now') THEN 'Hoy'
                   ELSE 'Próxima'
               END as estado
        FROM reservas r
        JOIN canchas c ON r.cancha = c.nombre
        WHERE r.id_usuario = ?
        ORDER BY r.fecha DESC, r.horario DESC
    """, (current_user.id,))
    reservas = cur.fetchall()
    
    return render_template('usuario_reservas.html', reservas=reservas)

@app.route('/usuario/cancelar-reserva/<int:id>', methods=['POST'])
@login_required
def usuario_cancelar_reserva(id):
    db = get_db()
    cur = db.cursor()
    
    cur.execute("""
        SELECT id_reserva, cancha, fecha 
        FROM reservas 
        WHERE id_reserva = ? AND id_usuario = ? AND fecha >= date('now')
    """, (id, current_user.id))
    reserva = cur.fetchone()
    
    if not reserva:
        flash('Reserva no encontrada o no se puede cancelar', 'error')
        return redirect(url_for('usuario_mis_reservas'))
    
    try:
        cur.execute("DELETE FROM reservas WHERE id_reserva = ? AND id_usuario = ?", (id, current_user.id))
        db.commit()
        flash(f'Reserva para {reserva["cancha"]} cancelada exitosamente', 'success')
    except Exception as e:
        get_db().rollback()
        print(f"Error al cancelar reserva: {str(e)}")
        flash('Error al cancelar la reserva', 'error')
    
    return redirect(url_for('usuario_mis_reservas'))

@app.route('/usuario/favoritos')
@login_required
def usuario_favoritos():
    db = get_db()
    cur = db.cursor()
    
    cur.execute("""
        SELECT c.id_cancha, c.nombre, c.precio, c.descripcion, c.imagen_url, c.direccion
        FROM favoritos f
        JOIN canchas c ON f.cancha = c.nombre
        WHERE f.id_usuario = ?
        ORDER BY f.fecha_agregado DESC
    """, (current_user.id,))
    favoritos = cur.fetchall()
    
    return render_template('usuario_favoritos.html', favoritos=favoritos)

@app.route('/usuario/favoritos/agregar/<int:id_cancha>', methods=['POST'])
@login_required
def usuario_agregar_favorito(id_cancha):
    db = get_db()
    cur = db.cursor()
    
    cur.execute("SELECT nombre FROM canchas WHERE id_cancha = ?", (id_cancha,))
    cancha = cur.fetchone()
    
    if not cancha:
        return jsonify({'success': False, 'message': 'Cancha no encontrada'}), 404
    
    try:
        cur.execute("""
            SELECT id_favorito FROM favoritos 
            WHERE id_usuario = ? AND cancha = ?
        """, (current_user.id, cancha['nombre']))
        
        if cur.fetchone():
            return jsonify({'success': False, 'message': 'Ya está en favoritos'}), 400
        
        cur.execute("""
            INSERT INTO favoritos (id_usuario, cancha)
            VALUES (?, ?)
        """, (current_user.id, cancha['nombre']))
        db.commit()
        
        return jsonify({'success': True, 'message': 'Agregado a favoritos'})
    except Exception as e:
        get_db().rollback()
        print(f"Error al agregar favorito: {str(e)}")
        return jsonify({'success': False, 'message': 'Error al agregar'}), 500

@app.route('/usuario/favoritos/eliminar/<int:id_cancha>', methods=['POST'])
@login_required
def usuario_eliminar_favorito(id_cancha):
    db = get_db()
    cur = db.cursor()
    
    cur.execute("SELECT nombre FROM canchas WHERE id_cancha = ?", (id_cancha,))
    cancha = cur.fetchone()
    
    if not cancha:
        return jsonify({'success': False, 'message': 'Cancha no encontrada'}), 404
    
    try:
        cur.execute("""
            DELETE FROM favoritos 
            WHERE id_usuario = ? AND cancha = ?
        """, (current_user.id, cancha['nombre']))
        db.commit()
        
        flash('Eliminado de favoritos', 'success')
        return jsonify({'success': True, 'message': 'Eliminado de favoritos'})
    except Exception as e:
        get_db().rollback()
        print(f"Error al eliminar favorito: {str(e)}")
        return jsonify({'success': False, 'message': 'Error al eliminar'}), 500

@app.route('/perfil_usuario', methods=['GET', 'POST'])
@login_required
def perfil_usuario():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            correo = request.form['correo']
            edad = request.form['edad']
            direccion = request.form.get('direccion', '')
            nueva_contraseña = request.form.get('nueva_contraseña')
            
            db = get_db()
            cur = db.cursor()
            
            if nueva_contraseña and len(nueva_contraseña) >= 6:
                hashed = generate_password_hash(nueva_contraseña)
                cur.execute("""
                    UPDATE usuarios 
                    SET nombre = ?, correo = ?, edad = ?, direccion = ?, contraseña = ?
                    WHERE id = ?
                """, (nombre, correo, edad, direccion, hashed, current_user.id))
            else:
                cur.execute("""
                    UPDATE usuarios 
                    SET nombre = ?, correo = ?, edad = ?, direccion = ?
                    WHERE id = ?
                """, (nombre, correo, edad, direccion, current_user.id))
            
            db.commit()
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('perfil_usuario'))
            
        except Exception as e:
            get_db().rollback()
            print(f"Error al actualizar perfil: {str(e)}")
            flash('Error al actualizar el perfil', 'error')
    
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM reservas WHERE id_usuario = ?", (current_user.id,))
    total_reservas = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(DISTINCT cancha) FROM reservas WHERE id_usuario = ?", (current_user.id,))
    canchas_visitadas = cur.fetchone()[0]
    
    return render_template('perfil_usuario.html', 
                         total_reservas=total_reservas,
                         canchas_visitadas=canchas_visitadas)

# ---------------------- OTRAS RUTAS ----------------------

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión.", "success")
    return redirect(url_for('login'))

@app.route('/reset_contrasena')
def reset_contrasena():
    return render_template('reset_contrasena.html')

# API para verificar disponibilidad
@app.route('/api/disponibilidad/<int:id_cancha>/<fecha>')
@login_required
def check_availability(id_cancha, fecha):
    try:
        db = get_db()
        cur = db.cursor()
        
        # Obtener reservas activas para esa cancha y fecha
        cur.execute("""
            SELECT horario 
            FROM reservas 
            WHERE id_cancha = ? 
            AND fecha = ? 
            AND estado != 'cancelada'
        """, (id_cancha, fecha))
        
        reservas = cur.fetchall()
        horarios_ocupados = [r[0] for r in reservas]
        
        return jsonify({
            'success': True,
            'horarios_ocupados': horarios_ocupados
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
