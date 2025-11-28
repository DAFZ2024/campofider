-- SQLite3 Database Schema
-- Converted from MySQL export
-- Database: usuariosdb

-- --------------------------------------------------------
-- Table: usuarios
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    edad INTEGER NOT NULL,
    contraseña TEXT NOT NULL,
    direccion TEXT DEFAULT NULL,
    rol TEXT NOT NULL DEFAULT 'usuario'
);

-- --------------------------------------------------------
-- Table: administradores
-- --------------------------------------------------------
-- (La tabla 'administradores' ha sido eliminada. Ahora la relación con propietarios se maneja vía 'usuarios' y 'usuario_id' en 'canchas')

-- --------------------------------------------------------
-- Table: canchas
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS canchas (
    id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio TEXT DEFAULT NULL,
    descripcion TEXT DEFAULT NULL,
    imagen_url TEXT DEFAULT NULL,
    tiempo_uso INTEGER DEFAULT 0,
    cronometro_inicio DATETIME DEFAULT NULL,
    direccion TEXT DEFAULT NULL,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- --------------------------------------------------------
-- Table: favoritos
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS favoritos (
    id_favorito INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    cancha TEXT NOT NULL,
    fecha_agregado DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- --------------------------------------------------------
-- Table: horarios_canchas
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS horarios_canchas (
    id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cancha INTEGER NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    disponible INTEGER DEFAULT 1,
    FOREIGN KEY (id_cancha) REFERENCES canchas(id_cancha)
);

-- --------------------------------------------------------
-- Table: reservas
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS reservas (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    cancha TEXT NOT NULL,
    horario TEXT NOT NULL,
    fecha DATE NOT NULL,
    numero TEXT,
    mensaje TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

-- --------------------------------------------------------
-- Insert data into usuarios
-- --------------------------------------------------------

INSERT INTO usuarios (id, nombre, correo, edad, contraseña, rol) VALUES
(45, 'Andres Escobar', 'andres123@gmail.com', 25, 'scrypt:32768:8:1$jBAMrbdl7cnmoGpQ$3ac545daf0c2a24596eacbf26f8e4f05e0d0182552c28daa9a92b4d65c42e910402ab92f7d538eac2a6b11d4cf253b8f06f56c58440e20d8ca7969a948983ef0', 'administrador'),
(102, 'Administrador Mendoza', 'mendoza@campofinder.com', 30, 'mendoza123', 'administrador'),
(103, 'Administrador Bombonera', 'bombonera@campofinder.com', 30, 'bombonera123', 'administrador'),
(104, 'Administrador Cúpula', 'cupula@campofinder.com', 30, 'cupula123', 'administrador'),
(105, 'Administrador Arenosa', 'arenosa@campofinder.com', 30, 'arenosa123', 'administrador'),
(108, 'Administrador Surxoacha', 'surxoacha@campofinder.com', 30, 'surxoacha123', 'administrador'),
(109, 'Administrador Punto30', 'punto30@campofinder.com', 30, 'punto30123', 'administrador'),
(110, 'Administrador Primos', 'primos@campofinder.com', 30, 'primos123', 'administrador'),
(111, 'Administrador Parque', 'parque@campofinder.com', 30, 'parque123', 'administrador'),
(115, 'Jorge Escobar', 'gesgondres10@gmail.com', 25, 'scrypt:32768:8:1$eg6napE27IaazIDC$f39852ba088d0f76ee734e3d0e10868e66fa647b5a869dcfed2158c6a6a18aaed3b57576447d0ad66921bba3edfa26aa29b119d6517d914bd961086c02a25542', 'administrador'),
(116, 'Jorge Escobar', 'jesgondres10@gmail.com', 25, 'scrypt:32768:8:1$Gr8z4Vihrc7I6u4n$68b4dd2577e8238ecb67353223228a479310a8d9bcc7ed3335a31f859e018a76d97d78b1f926d47b244b21b199e5f5823cb136e3d9104e09c0c170cbb57303fc', 'jugador');

-- --------------------------------------------------------
-- Insert data into administradores
-- --------------------------------------------------------
-- Los inserts de la tabla 'administradores' han sido removidos porque la tabla ya no existe.

-- --------------------------------------------------------
-- Insert data into canchas
-- --------------------------------------------------------

INSERT INTO canchas (id_cancha, nombre, precio, descripcion, imagen_url, tiempo_uso, cronometro_inicio, usuario_id) VALUES
(13, 'Cancha de Administrador Mendoza', '120000', 'Disfruta del deporte rey en una amplia cancha de césped natural. Ubicada en la zona residencial de La Mendoza en Soacha, ofrece un espacio abierto con vistas a las montañas. Es el lugar perfecto para partidos de fútbol 11 o entrenamientos de gran formato. ¡El ambiente perfecto para sentirte como un profesional!', 'static/imagenes/La_mendoza.png', 0, NULL, 102),
(15, 'Cancha la Cúpula', '85000', 'Una robusta cancha cubierta en el sector de Soacha, conocida por su amplia cúpula que garantiza un juego sin interrupciones por lluvia. Su grama sintética está diseñada para resistir y ofrecer un pique de balón constante. Además, cuenta con una tarima y área de cafetería para tus espectadores.', 'static/imagenes/lacupula.png', 0, NULL, 104),
(16, 'Cancha la Arenosa', '80000', 'Ubicado en las afueras de Soacha, La Arenosa ofrece amplias zonas verdes y una cancha sintética de gran tamaño. Es un espacio perfecto para escuelas de formación deportiva y partidos de fin de semana en un ambiente limpio y despejado. ¡Ideal para toda la familia', 'static/imagenes/larenosa.png', 0, NULL, 105),
(19, 'Cancha Teatro De Los Sueños', '120000', 'Nuestra cancha Blue 6 te ofrece un espacio cubierto con grama sintética de calidad y un diseño moderno de color azul. Ubicada estratégicamente en Soacha, es ideal para partidos rápidos y llenos de adrenalina, garantizando la diversión sin importar el clima. ¡Con arcos profesionales y excelente mantenimiento!', 'static/imagenes/cancha2.png', 0, NULL, 108),
(20, 'Cancha de Punto30', '100000', 'Una cancha sintética bien mantenida en Soacha que pone la experiencia del jugador primero. Disfruta de un excelente ambiente nocturno con buena iluminación y una zona de banca cómoda para rotar a tus compañeros. ¡Reserva aquí el mejor partido de la semana!', 'static/imagenes/punto30.png', 0, NULL, 109),
(21, 'Cancha Don Balon', '90000', 'Experimenta el fútbol 5 bajo techo en Don Balón, una de las mejores canchas del sector de Soacha. Disfruta de grama sintética de última generación, iluminación LED superior y un área de descanso con vista a la cancha. Perfecta para torneos nocturnos y entrenamientos de alto nivel.', 'static/imagenes/donbalon.png', 0, NULL, 110),
(22, 'Cancha Indoor Naranja', '100000', 'Esta cancha cubierta se destaca en Soacha por su enfoque en la seguridad, con postes y paredes acolchadas en un vibrante color naranja. Ofrece una superficie sintética de calidad y un amplio techo para jugar cómodamente. ¡Perfecta para partidos en cualquier clima, con la máxima protección!', 'static/imagenes/parquecolor.png', 0, NULL, 111),
(27, 'Cancha La Bombonera ', '90000', 'Una auténtica cancha de barrio ubicada en el corazón de Soacha. Ideal para armar el partido de la semana con tus amigos. Ofrece una experiencia de juego al aire libre, sintiendo la energía de la comunidad local. ¡Reserva tu horario y juega como en casa!', 'static/canchas_uploads/Cancha_La_Bombonera__115.png', 0, NULL, 115);

-- --------------------------------------------------------
-- Trigger: registrar_admin
-- SQLite trigger to auto-create admin and cancha when a new admin user is registered
-- --------------------------------------------------------

CREATE TRIGGER IF NOT EXISTS registrar_admin 
AFTER INSERT ON usuarios
FOR EACH ROW
WHEN NEW.rol = 'administrador'
BEGIN
    -- Insert into administradores table
    INSERT INTO administradores (usuario_id) VALUES (NEW.id);
    
    -- Insert into canchas table with default image based on name
    INSERT INTO canchas (nombre, imagen_url, usuario_id)
    VALUES (
        'Cancha de ' || NEW.nombre,
        CASE
            WHEN NEW.nombre LIKE '%Mendoza%'   THEN 'static/imagenes/La_mendoza.png'
            WHEN NEW.nombre LIKE '%Bombonera%' THEN 'static/imagenes/labomonera.png'
            WHEN NEW.nombre LIKE '%Cúpula%'    THEN 'static/imagenes/lacupula.png'
            WHEN NEW.nombre LIKE '%Arenosa%'   THEN 'static/imagenes/larenosa.png'
            WHEN NEW.nombre LIKE '%Judá%'      THEN 'static/imagenes/leondejuda.png'
            WHEN NEW.nombre LIKE '%Last Time%' THEN 'static/imagenes/cancha1.png'
            WHEN NEW.nombre LIKE '%Surxoacha%' THEN 'static/imagenes/cancha2.png'
            WHEN NEW.nombre LIKE '%Punto30%'   THEN 'static/imagenes/punto30.png'
            WHEN NEW.nombre LIKE '%Primos%'    THEN 'static/imagenes/donbalon.png'
            WHEN NEW.nombre LIKE '%Parque%'    THEN 'static/imagenes/parquecolor.png'
            ELSE 'static/imagenes/default.png'
        END,
        NEW.id
    );
END;
