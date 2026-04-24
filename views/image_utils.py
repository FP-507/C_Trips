# ─────────────────────────────────────────────────────────────────────────────
# image_utils.py — Manejo de la imagen de fondo
# ─────────────────────────────────────────────────────────────────────────────
# La app muestra una imagen de fondo en la pantalla "Get Started".
# Este módulo decide de dónde sacar esa imagen, en este orden de prioridad:
#
#   1. Imagen local en la carpeta assets/  (el usuario la puso ahí a mano)
#   2. Imagen en caché local (~/.ctrips_bg.jpg)  (ya se descargó antes)
#   3. URL de Unsplash  (Flet la descarga directamente, requiere internet)
#   4. Sin imagen → la pantalla mostrará un degradado azul como fallback
# ─────────────────────────────────────────────────────────────────────────────

import os               # Para rutas de archivos y verificar si existen
import ssl              # Para configurar la seguridad de las conexiones HTTPS
import glob             # Para buscar archivos con comodines (ej: "*.jpg")
import urllib.request   # Para descargar archivos desde internet

# ── URLs de imágenes de playas/viajes en Unsplash ────────────────────────────
# Unsplash permite usar estas URLs directamente sin registro ni API key.
# Parámetros: w=800 (ancho máximo), q=80 (calidad de compresión JPEG).
IMAGENES_ONLINE = [
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",  # playa tropical
    "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=800&q=80",  # viaje en avión
    "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&q=80",  # carretera al atardecer
    "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=800&q=80",  # costa caribeña
]

# ── Ruta del archivo de caché ─────────────────────────────────────────────────
# os.path.expanduser("~") devuelve la carpeta personal del usuario:
#   Windows → C:\Users\NombreUsuario
#   Linux/Mac → /home/nombreusuario
# El punto al inicio del nombre lo convierte en archivo "oculto" en sistemas Unix.
IMG_CACHE = os.path.join(os.path.expanduser("~"), ".ctrips_bg.jpg")

# ── Ruta de la carpeta assets/ ────────────────────────────────────────────────
# Este archivo está en C_Trips/views/image_utils.py
# __file__           → .../views/image_utils.py
# dirname(__file__)  → .../views/
# dirname(dirname()) → .../C_Trips/          (subimos un nivel)
# join(..., "assets")→ .../C_Trips/assets/
ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets"
)


def obtener_imagen_local() -> str | None:
    """
    Busca cualquier imagen en la carpeta assets/.

    Revisa los formatos más comunes: jpg, jpeg, png, webp.
    Devuelve la ruta completa de la primera imagen que encuentre,
    o None si la carpeta está vacía o no existe.
    """
    extensiones = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    for ext in extensiones:
        # glob.glob devuelve una lista de rutas que coinciden con el patrón
        resultados = glob.glob(os.path.join(ASSETS_DIR, ext))
        if resultados:
            return resultados[0]   # Retorna la primera imagen encontrada
    return None   # No se encontró ninguna imagen local


def obtener_src_imagen() -> tuple[str, bool]:
    """
    Decide qué imagen mostrar en la pantalla 'Get Started'.

    Retorna una tupla (src, es_url) donde:
      - src    : ruta de archivo local O URL de internet
      - es_url : True si es URL, False si es ruta local
                 (reservado para uso futuro si se necesita diferenciarlo)
    """
    # Prioridad 1: imagen en la carpeta assets/ del proyecto
    local = obtener_imagen_local()
    if local:
        return local, False

    # Prioridad 2: imagen descargada previamente en caché
    if os.path.exists(IMG_CACHE):
        return IMG_CACHE, False

    # Prioridad 3: URL online — Flet/Flutter la descarga internamente
    # Si no hay internet, Flet mostrará el error_content definido en ft.Image
    return IMAGENES_ONLINE[0], True


def descargar_imagen() -> None:
    """
    Descarga la primera imagen de IMAGENES_ONLINE al caché local.

    Esta función se ejecuta en un hilo separado (ver main.py) para no
    bloquear la interfaz mientras descarga. Si ya existe imagen local
    o en caché, no hace nada. Si falla la descarga (sin internet, etc.),
    simplemente ignora el error — la app usará la URL directa como fallback.
    """
    # Si ya tenemos imagen (local o caché), no hay nada que descargar
    if obtener_imagen_local() or os.path.exists(IMG_CACHE):
        return

    try:
        # Crear contexto SSL que no verifica certificados
        # (necesario en algunos entornos corporativos / Windows Store Python)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Abrir la URL y escribir el contenido en el archivo de caché
        # 'with ... as ...' garantiza que ambos (conexión y archivo) se cierren
        with urllib.request.urlopen(IMAGENES_ONLINE[0], context=ctx) as resp, \
             open(IMG_CACHE, "wb") as f:
            f.write(resp.read())   # Lee todos los bytes y los escribe en disco

    except Exception:
        # Si algo falla (sin internet, error de red, disco lleno, etc.)
        # simplemente continuamos — la app usará la URL como fallback
        pass
