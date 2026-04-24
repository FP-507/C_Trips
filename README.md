# CTRIP'S

App de viajes construida con [Flet](https://flet.dev/) (Python). Diseñada para explorar destinos en Colón, Panamá.

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
pip install -r requirements.txt
```

> **Windows (Microsoft Store Python):** Si ves un error `SSL: CERTIFICATE_VERIFY_FAILED` al instalar o correr la app, es un problema conocido con los certificados del sistema. El código ya incluye el bypass necesario para que Flet descargue su cliente desktop.

## Uso

```bash
python main.py
```

## Estructura del proyecto

```
C_Trips/
├── main.py              # Punto de entrada y router de rutas
├── requirements.txt
├── assets/              # Coloca aquí tus imágenes locales (.jpg, .png, .webp)
├── data/
│   └── usuarios.csv     # Base de datos de usuarios (se crea automáticamente)
└── views/
    ├── __init__.py
    ├── constants.py     # Colores y constantes de diseño
    ├── helpers.py       # Componentes UI reutilizables
    ├── image_utils.py   # Manejo de imágenes (local, cache, online)
    ├── db.py            # Capa de acceso a datos (CSV)
    ├── splash.py        # Pantalla de inicio
    ├── get_started.py   # Pantalla "Get Started"
    ├── sign_in.py       # Pantalla de inicio de sesión
    └── sign_up.py       # Pantalla de registro
```

## Pantallas

| Ruta | Pantalla |
|---|---|
| `/` | Splash — toca para continuar |
| `/getstarted` | Presentación con imagen de fondo |
| `/signin` | Inicio de sesión |
| `/signup` | Registro de cuenta nueva |

## Base de datos (CSV)

Los usuarios se guardan en `data/usuarios.csv` con estas columnas:

| Campo | Descripción |
|---|---|
| `nombre` | Nombre completo |
| `email` | Email en minúsculas (clave única) |
| `password_hash` | SHA-256 de la contraseña — nunca en texto plano |

El archivo se crea automáticamente al registrar el primer usuario. Puedes abrirlo con Excel o cualquier editor de texto.

### Validaciones en registro
- Todos los campos obligatorios
- Formato de email válido
- Contraseña mínimo 6 caracteres
- Email no repetido

### Sesión activa
Al iniciar sesión los datos del usuario quedan en `page.session` bajo la clave `"usuario"` para ser usados en pantallas futuras.

## Imágenes de fondo

La app carga la imagen de fondo con este orden de prioridad:

1. **`assets/`** — cualquier `.jpg`, `.png` o `.webp` que coloques ahí
2. **Cache local** — `~/.ctrips_bg.jpg` (descargado automáticamente en el primer inicio)
3. **URL online** — Unsplash (Flet lo carga directamente, requiere internet)
4. **Degradado** — fallback visual si no hay imagen ni internet

## Dependencias

| Paquete | Uso |
|---|---|
| `flet` | Framework UI multiplataforma |

> `csv`, `hashlib`, `ssl`, `threading` y `glob` son módulos de la biblioteca estándar de Python — no requieren instalación.
