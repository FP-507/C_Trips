"""
CTRIP'S — App de viajes
=======================
Punto de entrada de la aplicación. Aquí se configura la ventana,
se registran todas las rutas (pantallas) y se arranca Flet.

Requisitos : pip install flet
Python     : 3.10 o superior
Flet       : 0.80 o superior
Ejecutar   : python main.py
"""

# ── Comprobación de versión de Python ───────────────────────────────────────
# Lo hacemos ANTES de importar cualquier cosa, porque los f-strings con
# match/case y otras características modernas requieren Python 3.10+.
import sys

if sys.version_info < (3, 10):
    print("Se requiere Python 3.10 o superior")
    sys.exit(1)

# ── Parche SSL ───────────────────────────────────────────────────────────────
# En Windows con Python del Microsoft Store los certificados SSL del sistema
# no están configurados correctamente. Esto provoca que Flet no pueda
# descargar su cliente desktop la primera vez que se ejecuta.
# La línea siguiente desactiva la verificación de certificados SOLO para
# las descargas internas de Flet; no afecta a la seguridad de la app.
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# ── Imports estándar ─────────────────────────────────────────────────────────
import threading          # Para ejecutar la descarga de imagen en segundo plano
from typing import Any    # Para anotar tipos de eventos de Flet sin crashear

# ── Flet: el framework de la interfaz gráfica ────────────────────────────────
import flet as ft

# ── Importar todas las pantallas (vistas) ────────────────────────────────────
# Cada función "vista_X" construye y devuelve un ft.View (una pantalla completa)
from views import vista_splash, vista_get_started, vista_sign_in, vista_sign_up, vista_home

# ── Importar la función que descarga la imagen de fondo ──────────────────────
from views.image_utils import descargar_imagen


# ── Tabla de rutas ───────────────────────────────────────────────────────────
# Relaciona cada URL interna ("/ruta") con la función que construye esa pantalla.
# Cuando el usuario navega a una ruta, el router busca aquí la función correcta.
RUTAS = {
    "/":           vista_splash,        # Pantalla de inicio / logo
    "/getstarted": vista_get_started,   # Presentación de la app
    "/signin":     vista_sign_in,       # Inicio de sesión
    "/signup":     vista_sign_up,       # Registro de cuenta nueva
    "/home":       vista_home,          # Pantalla principal (tras login)
}


def main(page: ft.Page) -> None:
    """
    Función principal de la app. Flet la llama una vez por cada usuario/ventana.

    'page' es el objeto central de Flet: representa la ventana completa y
    expone métodos como page.go(), page.update(), page.session, etc.
    """

    # ── Configuración de la ventana ──────────────────────────────────────────
    page.title            = "CTRIP'S"        # Título que aparece en la barra del SO
    page.window.width     = 390              # Ancho en píxeles (tamaño de móvil)
    page.window.height    = 844              # Alto en píxeles (tamaño de móvil)
    page.window.resizable = False            # El usuario no puede redimensionar
    page.padding          = 0               # Sin margen interior en la página
    page.theme_mode       = ft.ThemeMode.LIGHT  # Forzar tema claro
    page.theme            = ft.Theme(color_scheme_seed="#1B3A6B")  # Color base azul

    # ── Descarga de imagen de fondo en segundo plano ─────────────────────────
    # daemon=True significa que el hilo se cierra automáticamente si la app
    # se cierra antes de que termine la descarga.
    threading.Thread(target=descargar_imagen, daemon=True).start()

    # ── Router: maneja los cambios de pantalla ────────────────────────────────
    def route_change(e: Any) -> None:
        """
        Se ejecuta cada vez que se llama a page.go("/ruta").
        1. Borra todas las pantallas apiladas.
        2. Construye la nueva pantalla según la ruta actual.
        3. La añade a la pila y refresca la UI.
        """
        page.views.clear()                                    # Limpia pantallas anteriores
        vista_fn = RUTAS.get(page.route, vista_splash)        # Busca la función de la ruta
        page.views.append(vista_fn(page))                     # Construye y apila la pantalla
        page.update()                                         # Redibuja la interfaz

    def view_pop(e: Any) -> None:
        """
        Se ejecuta cuando el usuario pulsa el botón físico "atrás" del sistema.
        Elimina la pantalla actual y vuelve a la anterior.
        """
        if len(page.views) > 1:          # Solo si hay más de una pantalla en la pila
            page.views.pop()             # Elimina la pantalla actual
            page.go(page.views[-1].route)  # Navega a la pantalla que quedó en el tope

    # ── Registrar los manejadores de eventos ─────────────────────────────────
    page.on_route_change = route_change   # Flet llama esto al cambiar de ruta
    page.on_view_pop     = view_pop       # Flet llama esto al presionar "atrás"

    # ── Navegar a la pantalla inicial ─────────────────────────────────────────
    page.go("/")   # Abre el Splash al arrancar


# ── Arranque de la aplicación ─────────────────────────────────────────────────
if __name__ == "__main__":
    # ft.app() inicia el servidor Flet y abre la ventana desktop.
    # 'target=main' indica la función que Flet debe llamar para cada sesión.
    ft.app(target=main)
