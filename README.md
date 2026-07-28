# PLAREN — Plataforma de Revisión Normativa

> Aplicación web desarrollada para el **Consejo para Prevenir, Atender y Erradicar la Discriminación en el Estado de Guanajuato (COPRAEDEG)**.  
> Permite a los integrantes del Consejo revisar, analizar y opinar sobre el marco normativo estatal de forma estructurada y colaborativa.

---

## 🚀 Descripción

**PLAREN** es una herramienta interactiva construida con [Streamlit](https://streamlit.io) que facilita la revisión normativa del Consejo. Los usuarios autenticados pueden:

- Navegar el catálogo normativo organizado por **capítulos**, **secciones**, **artículos** y **fracciones**.
- Consultar resúmenes de cada disposición legal.
- Registrar **opiniones técnicas** con clasificación de impacto:
  - 💰 **Presupuestal** — ¿requiere esfuerzo presupuestal?
  - ⚖️ **Jurídico** — ¿implica modificar o trastocar otras leyes?
  - 🫂 **Social** — ¿afecta a grupos prioritarios o vulnerables?

Toda la información se almacena de manera persistente en una base de datos MySQL.

---

## 🏗️ Arquitectura

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│  Python Backend  │────▶│   MySQL Server  │
│   (app.py)      │     │  (database.py)   │     │  (RDS / Local)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Archivos principales

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Interfaz de usuario, lógica de navegación, formularios de opinión y autenticación. |
| `database.py` | Capa de acceso a datos: conexión SQLAlchemy, consultas al catálogo y persistencia de opiniones. |

---

## ⚙️ Requisitos

- Python 3.10+
- MySQL 8.0+ (o MariaDB 10.6+)
- Dependencias de Python:

```text
streamlit>=1.40
sqlalchemy>=2.0
pandas>=2.0
pymysql>=1.1
```

---

## 🛠️ Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/taquitoo3000/plaren.git
cd plaren
```

2. **Crear entorno virtual**

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate    # Windows
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar credenciales de base de datos**

Crear el archivo `.streamlit/secrets.toml`:

```toml
[connections.mysql]
dialect = "mysql"
driver = "pymysql"
host = "tu_servidor.mysql.database.azure.com"
port = 3306
database = "copraedeg_db"
username = "tu_usuario"
password = "tu_contraseña"
```

> También se admiten las claves `DB_USER`, `DB_PASS`, `DB_SERVER`, `DB_PORT` y `DB_NAME` como alternativa.

5. **Ejecutar la aplicación**

```bash
streamlit run app.py
```

La app estará disponible en `http://localhost:8501`.

---

## 🗄️ Esquema de Base de Datos

### Tablas esperadas

| Tabla | Propósito |
|-------|-----------|
| `copraedeg_ley` | Catálogo normativo con capítulos, secciones, artículos, fracciones y resúmenes. |
| `copraedeg_leyes_congreso` | Listado de leyes vigentes del estado para referencia jurídica. |
| `copraedeg_opiniones` | Registro de opiniones emitidas por los integrantes del Consejo. |

### Estructura de `copraedeg_opiniones`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INT (PK, AI) | Identificador único de la opinión. |
| `ley_id` | INT (FK) | Referencia al artículo/fracción del catálogo. |
| `respuesta` | TEXT | Texto de la opinión técnica. |
| `impacto_presupuestal` | TINYINT | `1` si requiere esfuerzo presupuestal. |
| `impacto_juridico` | VARCHAR | Leyes afectadas, separadas por `\|`. |
| `impacto_social` | VARCHAR | Grupos vulnerables afectados, separados por `\|`. |
| `user` | VARCHAR | Nombre del integrante que emitió la opinión. |
| `fecha` | DATETIME | Fecha de registro (por defecto `NOW()`). |

---

## 👥 Integrantes del Consejo (usuarios)

La aplicación cuenta con un sistema de autenticación basado en lista desplegable. Los integrantes habilitados son:

- Presidencia del Consejo
- Secretaría Ejecutiva del Consejo (PRODHEG)
- Secretaría de Gobierno
- Secretaría del Nuevo Comienzo
- Secretaría de Derechos Humanos
- Secretaría de Educación
- Secretaría de Salud
- Secretaría de las Mujeres
- Dirección General del Sistema DIF Estatal
- Procuraduría Estatal de Protección de Niñas, Niños y Adolescentes
- Secretaría Ejecutiva del SIPINNA Estatal
- Presidencia Municipal de Guanajuato
- Presidencia Municipal de Moroleón
- Presidencia Municipal de Silao de la Victoria
- Presidencia Municipal de San Luis de la Paz
- Secretaría Instructora

---

## 📁 Estructura del Proyecto

```
plaren/
├── app.py                    # Aplicación principal Streamlit
├── database.py               # Conexión y operaciones con MySQL
├── requirements.txt          # Dependencias de Python
├── assets/
│   ├── icon_sectech.png      # Favicon de la app
│   ├── prodheg_horizontal.png # Logo de PRODHEG
│   └── segob_logo.png        # Logo de SEGOB
└── .streamlit/
    └── secrets.toml          # Credenciales (no versionar)
```

---

## 🎨 Características de la interfaz

- **Navegación jerárquica**: Capítulo → Sección → Resumen → Artículo → Fracción.
- **Formulario de opinión** con validación de campos obligatorios.
- **Clasificación de impacto** condicional (campos deshabilitados según selección).
- **Indicador visual** del integrante autenticado.
- **Diseño responsive** con tarjetas, divisores y estilos personalizados.
- **Caché de datos** (`@st.cache_data`) para optimizar consultas al catálogo.

---

## 🔒 Seguridad

- Las credenciales de base de datos se gestionan exclusivamente a través de `secrets.toml` de Streamlit.
- No se almacenan contraseñas de usuario; la autenticación es por selección de rol institucional.
- Se recomienda habilitar SSL/TLS en la conexión MySQL para entornos de producción.

---

## 🧑‍💻 Desarrollador

**SECtech** — [taquitoo3000.github.io/isael](https://taquitoo3000.github.io/isael)

---

## 📄 Licencia

© 2026 COPRAEDEG. Todos los derechos reservados.  
Desarrollado bajo encargo para el Consejo para Prevenir, Atender y Erradicar la Discriminación en el Estado de Guanajuato.

---

## 🐛 Reporte de errores

Para reportar fallas o sugerencias, visita: [sectechnologies.vercel.app](https://sectechnologies.vercel.app/)
