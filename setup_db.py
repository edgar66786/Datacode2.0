import sqlite3

conexion = sqlite3.connect('database.db')

# Tabla de alumnos (Punto 4)
conexion.execute('''
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        turno TEXT NOT NULL,
        taller TEXT NOT NULL,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Tabla del Comité Organizador (Punto 2)
conexion.execute('''
    CREATE TABLE IF NOT EXISTS propuestas_comite (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        votos_favor INTEGER DEFAULT 0
    )
''')

# Insertamos propuestas de ejemplo
conexion.execute("INSERT OR IGNORE INTO propuestas_comite (id, titulo, descripcion, votos_favor) VALUES (1, 'Ampliación de horarios en el laboratorio', 'Permitir el acceso al área de cómputo hasta las 20:00 hrs para prácticas libres.', 12)")
conexion.execute("INSERT OR IGNORE INTO propuestas_comite (id, titulo, descripcion, votos_favor) VALUES (2, 'Modificación de fechas del Torneo de Esport', 'Ajustar el inicio de las rondas de eliminación para evitar traslape con los talleres.', 8)")

conexion.commit()
conexion.close()
print("¡Base de datos configurada y tablas creadas con éxito! 🚀")