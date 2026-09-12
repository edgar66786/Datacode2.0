DATA CODE 2.0 — Plataforma Oficial UAdeO
Universidad Autónoma de Occidente (UAdeO) — Unidad Regional Guamúchil

Evento / Reto Oficial: DATA CODE 2.0 (2026)

1. Descripción
La plataforma web DATA CODE 2.0 es una solución digital integral desarrollada para cubrir las necesidades operativas, académicas y recreativas del congreso tecnológico institucional. El sistema centraliza la interacción entre los alumnos, el comité organizador y el jurado calificador mediante flujos transaccionales seguros, bases de datos relacionales y una interfaz moderna basada en la identidad visual institucional (guinda y dorado).

Módulos principales del sistema:

Portal de Acceso y Registro de Alumnos: Validación estricta de matrículas de 8 dígitos, contraseñas seguras, selección de unidad regional y turnos.

Panel de Estudiante (Dashboard): Visualización en tiempo real del estatus, taller asignado, torneo de Esports inscrito y acceso a credencial digital.

Gestión de Talleres: Catálogo interactivo con control estricto de cupos y aforo disponible.

Liga de Esports: Inscripción a torneos presenciales y en red con generación automática de folios de pago únicos (FOLIO-UAADEO-XXXXXX).

Comité y Buzón Estudiantil: Espacio participativo para proponer dinámicas y emitir votos únicos por alumno.

Dictamen Técnico: Módulo analítico de formato operativo (Hackathon vs Buildathon).

Panel de Administración: Acceso restringido para docentes y jueces para auditar registros, gestionar ganadores, configurar la rúbrica y exportar reportes directos en formato CSV.

2. Requisitos
Para la correcta ejecución del sistema en el entorno local o en un servidor de producción (como un VPS Linux con Gunicorn y Nginx):

Python (versión 3.8 o superior).

Administrador de paquetes pip.

3. Dependencias
El proyecto está optimizado con un diseño modular que requiere únicamente el microframework principal y librerías nativas del lenguaje:

Flask (para el control de enrutamiento y sesiones web).

SQLite3 (para la gestión de base de datos relacional mediante filas tipo diccionario).

4. Instalación
Clona el repositorio oficial en tu equipo local:

Bash
git clone https://github.com/TU_USUARIO/datacode-uadeo.git
Accede al directorio del proyecto:

Bash
cd datacode-uadeo
Instala la dependencia principal ejecutando:

Bash
pip install Flask
5. Configuración
La base de datos (database.db) se configura y despliega de manera automática en el primer arranque, creando las tablas e insertando los datos iniciales por defecto si se encuentra vacía.

El sistema implementa una llave secreta de sesión prediseñada en el script principal y maneja un diseño eco-sustentable libre de papel.

6. Ejecución
Inicia el servidor local de desarrollo ejecutando el archivo principal:

Bash
python app.py
Una vez iniciado el servidor, abre tu navegador web de preferencia e ingresa a la siguiente dirección:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

7. Credenciales de Demostración
Panel de Administración (Jueces / Docentes):

Dirígete a la sección de inicio de sesión y despliega el acceso exclusivo de administración.

Contraseña maestra: uadeo2026

Portal de Alumnos:

Puedes registrar una cuenta nueva desde la pestaña de Registro utilizando una matrícula válida de 8 dígitos (ejemplo: 21012345) y una contraseña segura de al menos 6 caracteres.

 Seguridad y Privacidad
El código fuente y el repositorio se entregan libres de credenciales reales, llaves de API, tokens de acceso o contraseñas de producción, cumpliendo estrictamente con las normativas de seguridad técnica y protección de datos exigidas en la rúbrica oficial de evaluación.
