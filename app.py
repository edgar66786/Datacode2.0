from flask import Flask, render_template, request, redirect, url_for, session, Response
import sqlite3
import random
import string
import csv

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'clave_secreta_uadeo_2026'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            turno TEXT NOT NULL,
            unidad_regional TEXT DEFAULT 'Guamúchil',
            taller TEXT DEFAULT 'Pendiente de Asignación',
            torneo TEXT DEFAULT 'Sin torneo inscrito'
        )
    ''')

    try:
        conn.execute("ALTER TABLE alumnos ADD COLUMN unidad_regional TEXT DEFAULT 'Guamúchil'")
    except sqlite3.OperationalError:
        pass

    try:
        conn.execute("ALTER TABLE alumnos ADD COLUMN torneo TEXT DEFAULT 'Sin torneo inscrito'")
    except sqlite3.OperationalError:
        pass

    conn.execute('''
        CREATE TABLE IF NOT EXISTS propuestas_comite (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            votos_favor INTEGER DEFAULT 0
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS votos_propuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT NOT NULL,
            propuesta_id INTEGER NOT NULL,
            UNIQUE(matricula, propuesta_id)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS votos_formato (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT UNIQUE NOT NULL,
            formato TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS talleres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            cupo TEXT NOT NULL,
            limite_cupo INTEGER DEFAULT 30,
            icono TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            requisitos TEXT NOT NULL,
            lugar TEXT DEFAULT 'Laboratorio de Cómputo',
            fecha TEXT DEFAULT '26 de Mayo, 2026',
            horario TEXT DEFAULT '09:00 AM - 11:00 AM',
            responsable TEXT DEFAULT 'Ing. Asignado'
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS cronograma (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            horario TEXT NOT NULL,
            actividad TEXT NOT NULL,
            lugar TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS torneos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            modalidad TEXT NOT NULL,
            costo TEXT DEFAULT 'Gratis ($0)',
            descripcion TEXT NOT NULL,
            requisitos TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS inscripciones_torneos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            torneo_nombre TEXT NOT NULL,
            equipo TEXT NOT NULL,
            capitan_nombre TEXT NOT NULL,
            matricula TEXT NOT NULL,
            carrera TEXT NOT NULL,
            modalidad TEXT NOT NULL,
            costo TEXT NOT NULL,
            folio_pago TEXT UNIQUE NOT NULL,
            estado_pago TEXT DEFAULT 'Validando Comprobante',
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS rubrica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            criterio TEXT NOT NULL,
            porcentaje TEXT NOT NULL,
            descripcion TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS ganadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            puesto TEXT NOT NULL,
            equipo_participante TEXT NOT NULL,
            integrantes TEXT NOT NULL
        )
    ''')
    
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM propuestas_comite')
    if cursor.fetchone()[0] == 0:
        conn.execute("INSERT INTO propuestas_comite (titulo, descripcion, votos_favor) VALUES ('Torneo de Free Fire en escuadras', 'Competencia general por equipos en el laboratorio de cómputo.', 12)")
        conn.execute("INSERT INTO propuestas_comite (titulo, descripcion, votos_favor) VALUES ('Taller avanzado de Python y Flask', 'Introducción práctica al desarrollo web backend.', 8)")
        conn.commit()

    cursor.execute('SELECT COUNT(*) FROM rubrica')
    if cursor.fetchone()[0] == 0:
        conn.execute("INSERT INTO rubrica (criterio, porcentaje, descripcion) VALUES ('Arquitectura y Código Limpio', '30%', 'Estructura modular, aplicación de patrones y buenas prácticas de desarrollo.')")
        conn.execute("INSERT INTO rubrica (criterio, porcentaje, descripcion) VALUES ('Innovación y Viabilidad Ecológica', '30%', 'Enfoque hacia la sostenibilidad o resolución de problemas reales del entorno.')")
        conn.execute("INSERT INTO rubrica (criterio, porcentaje, descripcion) VALUES ('Base de Datos y Seguridad', '20%', 'Normalización de tablas en SQLite, consultas seguras y control de aforos.')")
        conn.execute("INSERT INTO rubrica (criterio, porcentaje, descripcion) VALUES ('Defensa y Presentación (Pitch)', '20%', 'Claridad técnica en la exposición y funcionamiento en vivo del sistema.')")
        conn.commit()

    cursor.execute('SELECT COUNT(*) FROM talleres')
    if cursor.fetchone()[0] == 0:
        conn.execute("INSERT INTO talleres (titulo, cupo, limite_cupo, icono, descripcion, requisitos, lugar, fecha, horario, responsable) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     ('Arquitectura de Software y Clean Code', 'Cupo: 30 Alumnos', 30, 'bi-box-seam', 'Descubre cómo estructurar proyectos robustos. Abordaremos el modelo MVC, APIs RESTful y principios SOLID.', 'Laptop personal con IDE y lógica de POO.', 'Laboratorio de Cómputo 1', '26 de Mayo, 2026', '09:00 AM - 11:00 AM', 'Dr. Carlos Mendoza'))
        conn.execute("INSERT INTO talleres (titulo, cupo, limite_cupo, icono, descripcion, requisitos, lugar, fecha, horario, responsable) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     ('Desarrollo de Apps con Inteligencia Artificial y APIs', 'Cupo: 25 Alumnos', 25, 'bi-cpu-fill', 'Aprende a integrar modelos de lenguaje y APIs de IA generativa en aplicaciones web modernas usando Python.', 'Conocimientos básicos de programación y Python.', 'Laboratorio de Cómputo 2', '26 de Mayo, 2026', '11:30 AM - 01:30 PM', 'Dra. Sofía Valenzuela'))
        conn.execute("INSERT INTO talleres (titulo, cupo, limite_cupo, icono, descripcion, requisitos, lugar, fecha, horario, responsable) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     ('Fundamentos de Ciberseguridad y Hacking Ético', 'Cupo: 25 Alumnos', 25, 'bi-shield-lock-fill', 'Introducción a la seguridad en redes, pruebas de penetración básicas y mitigación de vulnerabilidades web.', 'Interés en redes y sistemas operativos.', 'Laboratorio de Redes', '26 de Mayo, 2026', '03:00 PM - 05:00 PM', 'Mtro. Alejandro Rivas'))
        conn.commit()

    cursor.execute('SELECT COUNT(*) FROM cronograma')
    if cursor.fetchone()[0] == 0:
        conn.execute("INSERT INTO cronograma (horario, actividad, lugar, tipo) VALUES ('08:30 AM - 09:00 AM', 'Registro oficial y entrega de gafetes digitales', 'Vestíbulo Principal', 'general')")
        conn.commit()

    cursor.execute('SELECT COUNT(*) FROM torneos')
    if cursor.fetchone()[0] == 0:
        conn.execute("INSERT INTO torneos (nombre, tipo, modalidad, costo, descripcion, requisitos) VALUES (?, ?, ?, ?, ?, ?)",
                     ('Super Smash Bros. Ultimate', 'Consola | 1 vs 1 (Individual)', 'Gratis', 'Sin costo ($0)', 'Modalidad 1vs1 con eliminación directa. 3 Vidas, 7 Minutos.', 'Ser alumno activo de la UAdeO y traer control propio.'))
        conn.execute("INSERT INTO torneos (nombre, tipo, modalidad, costo, descripcion, requisitos) VALUES (?, ?, ?, ?, ?, ?)",
                     ('EA Sports FC 26', 'Consola | 1 vs 1 (Individual)', 'Con costo', '$50 MXN por inscripción', 'Torneo relámpago con partidos de 6 minutos por mitad.', 'Matrícula vigente en la institución y pago previo.'))
        conn.execute("INSERT INTO torneos (nombre, tipo, modalidad, costo, descripcion, requisitos) VALUES (?, ?, ?, ?, ?, ?)",
                     ('Valorant (PC)', 'PC | Escuadras (5 vs 5)', 'Gratis', 'Sin costo ($0)', 'Competencia por equipos con fase de baneo de mapas.', 'Roster de 5 titulares con cuenta nivel 20+.'))
        conn.commit()

    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    try:
        ganadores = conn.execute('SELECT * FROM ganadores').fetchall()
    except sqlite3.OperationalError:
        ganadores = []
    
    matricula = session.get('matricula_alumno')
    alumno = None
    if matricula:
        alumno = conn.execute('SELECT * FROM alumnos WHERE matricula = ?', (matricula,)).fetchone()
        
    conn.close()
    return render_template('index.html', ganadores=ganadores, alumno=alumno)

@app.route('/inicio')
def inicio_publico():
    conn = get_db_connection()
    try:
        ganadores = conn.execute('SELECT * FROM ganadores').fetchall()
    except sqlite3.OperationalError:
        ganadores = []
    conn.close()
    return render_template('index.html', ganadores=ganadores, alumno=None)

@app.route('/dashboard', methods=['GET'])
def mi_dashboard():
    matricula = session.get('matricula_alumno')
    if not matricula:
        return redirect(url_for('inscripcion', mensaje="Por favor inicia sesión para ver tu panel."))
    return redirect(url_for('dashboard', matricula=matricula))

@app.route('/talleres')
def vista_talleres():
    conn = get_db_connection()
    talleres_bd = conn.execute('SELECT * FROM talleres').fetchall()
    conn.close()
    return render_template('talleres.html', talleres=talleres_bd)

@app.route('/torneos')
def vista_torneos():
    conn = get_db_connection()
    torneos_bd = conn.execute('SELECT * FROM torneos').fetchall()
    conn.close()
    return render_template('torneos.html', torneos=torneos_bd)

@app.route('/inscripcion', methods=['GET', 'POST'])
def inscripcion():
    mensaje = request.args.get('mensaje')
    return render_template('inscripcion.html', mensaje=mensaje)

@app.route('/registrar_alumno', methods=['POST'])
def registrar_alumno():
    nombre = request.form.get('nombre')
    matricula = request.form.get('matricula').strip()
    contrasena = request.form.get('contrasena')
    turno = request.form.get('turno')
    unidad_regional = request.form.get('unidad_regional', 'Guamúchil')
    
    if len(contrasena) < 6:
        return redirect(url_for('inscripcion', mensaje="La contraseña debe tener al menos 6 caracteres."))
        
    if not matricula.isdigit() or len(matricula) != 8:
        return redirect(url_for('inscripcion', mensaje="La matrícula debe contener exactamente 8 números."))

    taller_por_defecto = "Pendiente de Asignación"
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO alumnos (nombre, matricula, contrasena, turno, unidad_regional, taller) VALUES (?, ?, ?, ?, ?, ?)',
                     (nombre, matricula, contrasena, turno, unidad_regional, taller_por_defecto))
        conn.commit()
        conn.close()
        session['matricula_alumno'] = matricula
        return redirect(url_for('dashboard', matricula=matricula))
    except sqlite3.IntegrityError:
        conn.close()
        return redirect(url_for('inscripcion', mensaje="La matrícula ya está registrada."))

@app.route('/login_alumno', methods=['POST'])
def login_alumno():
    matricula = request.form.get('matricula').strip()
    contrasena = request.form.get('contrasena')
    
    if not matricula.isdigit() or len(matricula) != 8 or len(contrasena) < 6:
        return redirect(url_for('inscripcion', mensaje="Matrícula (8 dígitos) o contraseña inválidos."))
    
    conn = get_db_connection()
    alumno = conn.execute('SELECT * FROM alumnos WHERE matricula = ? AND contrasena = ?', (matricula, contrasena)).fetchone()
    conn.close()
    
    if alumno:
        session['matricula_alumno'] = matricula
        return redirect(url_for('dashboard', matricula=matricula))
    else:
        return redirect(url_for('inscripcion', mensaje="Matrícula o contraseña incorrectas."))

@app.route('/login_admin', methods=['POST'])
def login_admin():
    password_admin = request.form.get('password_admin')
    if password_admin == 'uadeo2026':
        session['admin_logged'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('inscripcion', mensaje="Contraseña de Administrador incorrecta."))

@app.route('/dashboard/<matricula>', methods=['GET'])
def dashboard(matricula):
    session['matricula_alumno'] = matricula
    conn = get_db_connection()
    alumno = conn.execute('SELECT * FROM alumnos WHERE matricula = ?', (matricula,)).fetchone()
    
    if alumno is None:
        conn.close()
        return redirect(url_for('inscripcion'))

    talleres_raw = conn.execute('SELECT * FROM talleres').fetchall()
    talleres = []
    for t in talleres_raw:
        inscritos_query = conn.execute('SELECT COUNT(*) FROM alumnos WHERE taller = ?', (t['titulo'],)).fetchone()
        inscritos = inscritos_query[0] if inscritos_query else 0
        limite = t['limite_cupo'] if 'limite_cupo' in t and t['limite_cupo'] is not None else 30
        
        taller_dict = {
            'id': t['id'],
            'titulo': t['titulo'],
            'cupo': t['cupo'],
            'limite_cupo': limite,
            'descripcion': t['descripcion'],
            'requisitos': t['requisitos'],
            'lugar': t['lugar'],
            'fecha': t['fecha'],
            'horario': t['horario'],
            'responsable': t['responsable'],
            'inscritos': inscritos,
            'lugares_disponibles': limite - inscritos
        }
        talleres.append(taller_dict)
        
    conn.close()
    return render_template('dashboard.html', alumno=alumno, talleres=talleres)

@app.route('/gafete/<matricula>', methods=['GET'])
def gafete(matricula):
    conn = get_db_connection()
    alumno = conn.execute('SELECT * FROM alumnos WHERE matricula = ?', (matricula,)).fetchone()
    conn.close()
    if alumno is None:
        return redirect(url_for('inscripcion'))
    return render_template('gafete.html', alumno=alumno)

@app.route('/torneo', methods=['GET'])
def torneo():
    conn = get_db_connection()
    torneos = conn.execute('SELECT * FROM torneos').fetchall()
    conn.close()
    return render_template('torneo.html', torneos=torneos)

@app.route('/comite', methods=['GET'])
def comite():
    matricula = session.get('matricula_alumno')
    conn = get_db_connection()
    
    propuestas = conn.execute('SELECT * FROM propuestas_comite').fetchall()
    
    votos_usuario = []
    if matricula:
        res = conn.execute('SELECT propuesta_id FROM votos_propuestas WHERE matricula = ?', (matricula,)).fetchall()
        votos_usuario = [row['propuesta_id'] for row in res]
        
    alumno = None
    if matricula:
        alumno = conn.execute('SELECT * FROM alumnos WHERE matricula = ?', (matricula,)).fetchone()
        
    conn.close()
    
    return render_template('comite.html', propuestas=propuestas, votos_usuario=votos_usuario, alumno=alumno)

@app.route('/comite/eleccion', methods=['GET'])
def eleccion_comite():
    matricula = session.get('matricula_alumno')
    if not matricula:
        return redirect(url_for('inscripcion', mensaje="Por favor inicia sesión para participar."))
    
    conn = get_db_connection()
    voto_actual = conn.execute('SELECT formato FROM votos_formato WHERE matricula = ?', (matricula,)).fetchone()
    conn.close()
    
    ya_voto = voto_actual['formato'] if voto_actual else None
    return render_template('eleccion_formato.html', ya_voto=ya_voto)

@app.route('/procesar_voto', methods=['POST'])
def procesar_voto():
    tipo_formato = request.form.get('tipo_formato')
    matricula = session.get('matricula_alumno')
    
    if not matricula:
        return redirect(url_for('inscripcion'))
        
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO votos_formato (matricula, formato) VALUES (?, ?)', (matricula, tipo_formato))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()
        
    return redirect(url_for('eleccion_comite'))

@app.route('/votar/<int:propuesta_id>', methods=('POST',))
def votar(propuesta_id):
    matricula = session.get('matricula_alumno')
    if not matricula:
        return redirect(url_for('inscripcion', mensaje="Inicia sesión para poder votar."))
        
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO votos_propuestas (matricula, propuesta_id) VALUES (?, ?)', (matricula, propuesta_id))
        conn.execute('UPDATE propuestas_comite SET votos_favor = votos_favor + 1 WHERE id = ?', (propuesta_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()
        
    return redirect(url_for('comite'))

@app.route('/propuesta/nueva', methods=('POST',))
def nueva_propuesta():
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    if titulo:
        conn = get_db_connection()
        conn.execute('INSERT INTO propuestas_comite (titulo, descripcion, votos_favor) VALUES (?, ?, ?)', (titulo, descripcion, 0))
        conn.commit()
        conn.close()
    return redirect(url_for('comite'))

@app.route('/rubrica', methods=['GET'])
def vista_rubrica():
    conn = get_db_connection()
    criterios = conn.execute('SELECT * FROM rubrica').fetchall()
    conn.close()
    return render_template('rubrica_alumno.html', criterios=criterios)

@app.route('/ganadores', methods=['GET'])
def vista_ganadores():
    conn = get_db_connection()
    ganadores = conn.execute('SELECT * FROM ganadores').fetchall()
    conn.close()
    return render_template('ganadores.html', ganadores=ganadores)

@app.route('/cronograma', methods=['GET'])
def cronograma():
    conn = get_db_connection()
    actividades = conn.execute('SELECT * FROM cronograma').fetchall()
    conn.close()
    return render_template('cronograma.html', actividades=actividades)

@app.route('/procesar_torneo', methods=['POST'])
def procesar_torneo():
    juego = request.form.get('juego')
    equipo = request.form.get('equipo', 'Individual')
    modalidad = request.form.get('modalidad', 'Gratis')
    costo = request.form.get('costo', 'Sin costo ($0)')
    
    matricula = session.get('matricula_alumno')
    
    if not matricula:
        return redirect(url_for('inscripcion', mensaje="Por favor inicia sesión para inscribirte al torneo."))

    conn = get_db_connection()
    alumno = conn.execute('SELECT * FROM alumnos WHERE matricula = ?', (matricula,)).fetchone()
    
    if not alumno:
        conn.close()
        return redirect(url_for('inscripcion'))

    capitan_nombre = alumno['nombre']
    carrera = alumno['unidad_regional']

    folio_pago = "FOLIO-UAADEO-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    estado_inicial = 'Aprobado (Sin Costo)' if modalidad == 'Gratis' else 'Pendiente de Pago'
    
    try:
        conn.execute('''
            INSERT INTO inscripciones_torneos (torneo_nombre, equipo, capitan_nombre, matricula, carrera, modalidad, costo, folio_pago, estado_pago)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (juego, equipo, capitan_nombre, matricula, carrera, modalidad, costo, folio_pago, estado_inicial))
        
        estatus_alumno = juego if modalidad == 'Gratis' else f"{juego} (Pago Pendiente)"
        conn.execute('UPDATE alumnos SET torneo = ? WHERE matricula = ?', (estatus_alumno, matricula))
        conn.commit()
    except Exception as e:
        print("Error al registrar torneo:", e)
    finally:
        conn.close()
        
    return redirect(url_for('comprobante_pago', folio=folio_pago))

@app.route('/comprobante/<folio>', methods=['GET'])
def comprobante_pago(folio):
    conn = get_db_connection()
    inscripcion = conn.execute('SELECT * FROM inscripciones_torneos WHERE folio_pago = ?', (folio,)).fetchone()
    conn.close()
    
    if not inscripcion:
        return redirect(url_for('torneo'))
        
    return render_template('comprobante.html', inscripcion=inscripcion)

@app.route('/detalle_juego/<juego>', methods=['GET'])
def detalle_juego(juego):
    conn = get_db_connection()
    torneo_db = conn.execute('SELECT * FROM torneos WHERE lower(nombre) LIKE ?', (f"%{juego}%",)).fetchone()
    conn.close()

    torneos_info = {
        'smash': {
            'nombre': 'Super Smash Bros. Ultimate',
            'tipo': 'Consola | 1 vs 1 (Individual)',
            'modalidad': 'Gratis',
            'costo': 'Sin costo ($0)',
            'reglas': ['Modalidad: 1vs1 con eliminación directa.', 'Configuración: 3 Vidas, 7 Minutos por partida (BO3).', 'Escenarios legales con Hazards APAGADOS.'],
            'requisitos': ['Ser alumno activo de la UAdeO.', 'Presentarse con control propio de Nintendo Switch o Gamecube.'],
            'requiere_roster': False
        },
        'fc26': {
            'nombre': 'EA Sports FC 26',
            'tipo': 'Consola | 1 vs 1 (Individual)',
            'modalidad': 'Con costo',
            'costo': '$50 MXN por inscripción',
            'reglas': ['Torneo relámpago con partidos de 6 minutos por mitad.', 'Uso obligatorio de Defensa Táctica y clima despejado.'],
            'requisitos': ['Matrícula vigente en la institución.', 'Comprobante de aportación institucional.'],
            'requiere_roster': False
        },
        'valorant': {
            'nombre': 'Valorant (PC)',
            'tipo': 'PC | Escuadras (5 vs 5)',
            'modalidad': 'Gratis',
            'costo': 'Sin costo ($0)',
            'reglas': ['Competencia por equipos con fase de baneo de mapas.', 'Partidas personalizadas en servidor LATAM oficial.'],
            'requisitos': ['Roster obligatorio de 5 titulares con cuenta nivel 20+.', 'Traer audífonos con micrófono propio.'],
            'requiere_roster': True
        },
        'mariokart': {
            'nombre': 'Mario Kart 8 Deluxe',
            'tipo': 'Consola | Todos contra Todos',
            'modalidad': 'Gratis',
            'costo': 'Sin costo ($0)',
            'reglas': ['Sistema de puntuación a 4 carreras en cilindrada de 150cc.', 'Prohibido el uso de volante inteligente y aceleración automática.'],
            'requisitos': ['Estar inscrito formalmente en la Unidad Regional.', 'Registro previo en plataforma.'],
            'requiere_roster': False
        }
    }
    
    datos = torneos_info.get(juego, {
        'nombre': 'Torneo Oficial Lince',
        'tipo': 'Competencia Universitaria',
        'modalidad': 'Gratis',
        'costo': 'Sin costo ($0)',
        'reglas': ['Acatar el reglamento general de la UAdeO.'],
        'requisitos': ['Credencial escolar vigente.'],
        'requiere_roster': False
    })
    
    if torneo_db:
        datos['nombre'] = torneo_db['nombre']
        datos['tipo'] = torneo_db['tipo']
        datos['modalidad'] = torneo_db['modalidad']
        datos['costo'] = torneo_db['costo']
        if '5' in torneo_db['tipo'].lower() or 'escuadras' in torneo_db['tipo'].lower():
            datos['requiere_roster'] = True

    return render_template('detalle_juego.html', datos=datos)

@app.route('/inscribir_taller/<int:taller_id>', methods=['POST'])
def inscribir_taller(taller_id):
    matricula = request.form.get('matricula')
    conn = get_db_connection()
    taller = conn.execute('SELECT * FROM talleres WHERE id = ?', (taller_id,)).fetchone()
    
    if taller and matricula:
        inscritos = conn.execute('SELECT COUNT(*) FROM alumnos WHERE taller = ?', (taller['titulo'],)).fetchone()[0]
        limite = taller['limite_cupo'] if 'limite_cupo' in taller and taller['limite_cupo'] is not None else 30
        
        if inscritos < limite:
            conn.execute('UPDATE alumnos SET taller = ? WHERE matricula = ?', (taller['titulo'], matricula))
            conn.commit()
            
    conn.close()
    return redirect(url_for('dashboard', matricula=matricula))

# --- PANEL DE ADMINISTRACIÓN ---
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged'):
        return redirect(url_for('inscripcion'))
        
    conn = get_db_connection()
    if request.method == 'POST':
        tipo_accion = request.form.get('tipo_accion')
        
        if tipo_accion == 'crear_torneo':
            nombre = request.form.get('nombre_torneo')
            tipo = request.form.get('tipo_torneo')
            modalidad = request.form.get('modalidad')
            costo = request.form.get('costo')
            descripcion = request.form.get('desc_torneo')
            requisitos = request.form.get('req_torneo')
            if nombre and modalidad:
                conn.execute('INSERT INTO torneos (nombre, tipo, modalidad, costo, descripcion, requisitos) VALUES (?, ?, ?, ?, ?, ?)',
                             (nombre, tipo, modalidad, costo, descripcion, requisitos))
                conn.commit()
                
        elif tipo_accion == 'eliminar_propuesta':
            prop_id = request.form.get('propuesta_id')
            conn.execute('DELETE FROM propuestas_comite WHERE id = ?', (prop_id,))
            conn.execute('DELETE FROM votos_propuestas WHERE propuesta_id = ?', (prop_id,))
            conn.commit()
            
        elif tipo_accion == 'reiniciar_votos_formato':
            conn.execute('DELETE FROM votos_formato')
            conn.commit()

    alumnos = conn.execute('SELECT * FROM alumnos').fetchall()
    talleres = conn.execute('SELECT * FROM talleres').fetchall()
    propuestas = conn.execute('SELECT * FROM propuestas_comite').fetchall()
    cronograma = conn.execute('SELECT * FROM cronograma').fetchall()
    torneos = conn.execute('SELECT * FROM torneos').fetchall()
    rubrica = conn.execute('SELECT * FROM rubrica').fetchall()
    ganadores = conn.execute('SELECT * FROM ganadores').fetchall()
    inscripciones_torneos = conn.execute('SELECT * FROM inscripciones_torneos').fetchall()
    
    votos_hackathon = conn.execute("SELECT COUNT(*) FROM votos_formato WHERE formato = 'hackathon'").fetchone()[0]
    votos_buildathon = conn.execute("SELECT COUNT(*) FROM votos_formato WHERE formato = 'buildathon'").fetchone()[0]

    conn.close()
    
    return render_template('admin_comite.html', alumnos=alumnos, talleres=talleres, propuestas=propuestas, 
                           cronograma=cronograma, torneos=torneos, rubrica=rubrica, ganadores=ganadores, inscripciones_torneos=inscripciones_torneos,
                           votos_hackathon=votos_hackathon, votos_buildathon=votos_buildathon)

@app.route('/admin/rubrica/crear', methods=['POST'])
def admin_crear_rubrica():
    if not session.get('admin_logged'):
        return redirect(url_for('inscripcion'))
    criterio = request.form.get('criterio')
    porcentaje = request.form.get('porcentaje')
    descripcion = request.form.get('descripcion')
    if criterio and porcentaje:
        conn = get_db_connection()
        conn.execute('INSERT INTO rubrica (criterio, porcentaje, descripcion) VALUES (?, ?, ?)', (criterio, porcentaje, descripcion))
        conn.commit()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/rubrica/eliminar/<int:id>', methods=['POST'])
def admin_eliminar_rubrica(id):
    if not session.get('admin_logged'):
        return redirect(url_for('inscripcion'))
    conn = get_db_connection()
    conn.execute('DELETE FROM rubrica WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/ganador/crear', methods=['POST'])
def admin_crear_ganador():
    if not session.get('admin_logged'):
        return redirect(url_for('inscripcion'))
    categoria = request.form.get('categoria')
    puesto = request.form.get('puesto')
    equipo = request.form.get('equipo')
    integrantes = request.form.get('integrantes')
    
    if categoria and equipo:
        conn = get_db_connection()
        conn.execute('INSERT INTO ganadores (categoria, puesto, equipo_participante, integrantes) VALUES (?, ?, ?, ?)',
                     (categoria, puesto, equipo, integrantes))
        conn.commit()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/ganador/eliminar/<int:id>', methods=['POST'])
def admin_eliminar_ganador(id):
    if not session.get('admin_logged'):
        return redirect(url_for('inscripcion'))
    conn = get_db_connection()
    conn.execute('DELETE FROM ganadores WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/torneo/editar/<int:id>', methods=['POST'])
def admin_editar_torneo(id):
    if not session.get('admin_logged'):
        return redirect(url_for('inscripcion'))
    nombre = request.form.get('nombre')
    modalidad = request.form.get('modalidad')
    costo = request.form.get('costo')
    if nombre:
        conn = get_db_connection()
        conn.execute('UPDATE torneos SET nombre = ?, modalidad = ?, costo = ? WHERE id = ?', (nombre, modalidad, costo, id))
        conn.commit()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/torneo/eliminar/<int:id>', methods=['POST'])
def admin_eliminar_torneo(id):
    if not session.get('admin_logged'):
        return redirect(url_for('inscripcion'))
    conn = get_db_connection()
    conn.execute('DELETE FROM torneos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/torneo/validar_pago/<int:inscripcion_id>', methods=['POST'])
def admin_validar_pago(inscripcion_id):
    if not session.get('admin_logged'):
        return redirect(url_for('inscripcion'))
        
    nuevo_estado = request.form.get('estado_pago')
    
    conn = get_db_connection()
    inscripcion = conn.execute('SELECT * FROM inscripciones_torneos WHERE id = ?', (inscripcion_id,)).fetchone()
    
    if inscripcion:
        matricula = inscripcion['matricula']
        torneo_nombre = inscripcion['torneo_nombre']
        
        conn.execute('UPDATE inscripciones_torneos SET estado_pago = ? WHERE id = ?', (nuevo_estado, inscripcion_id))
        
        if nuevo_estado == 'Aprobado (Pagado)':
            estatus_alumno = torneo_nombre
        else:
            estatus_alumno = f"{torneo_nombre} (Pago {nuevo_estado})"
            
        conn.execute('UPDATE alumnos SET torneo = ? WHERE matricula = ?', (estatus_alumno, matricula))
        conn.commit()
        
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/exportar/alumnos', methods=['GET'])
def exportar_alumnos():
    if not session.get('admin_logged'):
        return redirect(url_for('inscripcion'))
    
    conn = get_db_connection()
    alumnos = conn.execute('SELECT matricula, nombre, turno, unidad_regional, taller, torneo FROM alumnos').fetchall()
    conn.close()
    
    def generate():
        yield 'Matricula,Nombre,Turno,Unidad Regional,Taller Asignado,Torneo Inscrito\n'
        for a in alumnos:
            yield f"{a['matricula']},\"{a['nombre']}\",{a['turno']},{a['unidad_regional']},\"{a['taller']}\",\"{a['torneo']}\"\n"
            
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=reporte_alumnos_uadeo.csv"})

@app.route('/admin/exportar/torneos', methods=['GET'])
def exportar_torneos():
    if not session.get('admin_logged'):
        return redirect(url_for('inscripcion'))
    
    conn = get_db_connection()
    inscripciones = conn.execute('SELECT folio_pago, torneo_nombre, equipo, capitan_nombre, matricula, modalidad, costo, estado_pago FROM inscripciones_torneos').fetchall()
    conn.close()
    
    def generate():
        yield 'Folio,Torneo,Equipo,Capitán,Matrícula,Modalidad,Costo,Estatus Pago\n'
        for i in inscripciones:
            yield f"{i['folio_pago']},\"{i['torneo_nombre']}\",\"{i['equipo']}\",\"{i['capitan_nombre']}\",{i['matricula']},{i['modalidad']},{i['costo']},\"{i['estado_pago']}\"\n"
            
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=reporte_torneos_esports.csv"})

@app.route('/admin/logout', methods=['GET'])
def admin_logout():
    session.pop('admin_logged', None)
    return redirect(url_for('inscripcion'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)