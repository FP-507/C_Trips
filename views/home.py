# ─────────────────────────────────────────────────────────────────────────────
# home.py — Pantalla principal (después del login)
# ─────────────────────────────────────────────────────────────────────────────
# Primera pantalla que ve el usuario tras iniciar sesión.
# Muestra un saludo personalizado, una barra de búsqueda decorativa,
# tarjetas de destinos populares en Colón y categorías explorables.
#
# Datos del usuario disponibles en page.session.get("usuario"), que es un
# diccionario con claves: "nombre", "email", "password_hash".
# ─────────────────────────────────────────────────────────────────────────────

from typing import Any
import flet as ft
from .constants import AMARILLO, AZUL_OSCURO, AZUL_MEDIO, BLANCO, GRIS, GRIS_CLARO


def vista_home(page: ft.Page) -> ft.View:
    """
    Construye la pantalla principal de la app.

    Estructura:
      1. Encabezado con gradiente azul: saludo + búsqueda
      2. Sección "Destinos populares": tarjetas horizontales con scroll
      3. Sección "Explora Colón": lista de categorías
    """

    # ── Recuperar datos del usuario desde la sesión ───────────────────────────
    # page.session.get() devuelve None si la clave no existe, por eso usamos "or {}"
    # .get("nombre", "Viajero") usa "Viajero" como valor por defecto si no hay nombre
    usuario = page.session.get("usuario") or {}
    nombre  = usuario.get("nombre", "Viajero")

    # ── Función de cierre de sesión ───────────────────────────────────────────
    def cerrar_sesion(e: Any) -> None:
        """
        Elimina los datos del usuario de la sesión y vuelve al login.
        Después de esto, page.session.get("usuario") devolverá None.
        """
        page.session.remove("usuario")
        page.go("/signin")

    # ── Encabezado con gradiente azul ────────────────────────────────────────
    encabezado = ft.Container(
        padding=ft.padding.only(left=24, right=24, top=48, bottom=32),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[AZUL_OSCURO, AZUL_MEDIO],   # Gradiente de azul marino a azul medio
        ),
        content=ft.Column(
            [
                # Fila superior: saludo a la izquierda, botón logout a la derecha
                ft.Row(
                    [
                        # Columna con dos líneas de texto de saludo
                        ft.Column(
                            [
                                ft.Text("Bienvenido,", size=14, color="#FFFFFF99"),   # Texto sutil
                                ft.Text(nombre, size=24, weight=ft.FontWeight.BOLD, color=BLANCO),
                            ],
                            spacing=2,
                            expand=True,   # Ocupa el espacio disponible para empujar el botón a la derecha
                        ),
                        # Botón circular de logout
                        ft.Container(
                            width=42, height=42,
                            border_radius=21,        # Círculo perfecto
                            bgcolor=AMARILLO,
                            alignment=ft.alignment.center,
                            on_click=cerrar_sesion,
                            tooltip="Cerrar sesión",  # Texto al pasar el mouse
                            content=ft.Icon(ft.Icons.LOGOUT, color=AZUL_OSCURO, size=20),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                ft.Container(height=20),

                # Barra de búsqueda (decorativa — sin funcionalidad real aún)
                ft.Container(
                    bgcolor="#FFFFFF15",       # Blanco muy transparente sobre el gradiente
                    border_radius=14,
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.SEARCH, color=BLANCO, size=20),
                            ft.Text("¿A dónde quieres ir?", size=14, color="#FFFFFF88"),
                        ],
                        spacing=10,
                    ),
                ),
            ],
            spacing=0,
        ),
    )

    # ── Cuerpo scrolleable con las secciones de contenido ────────────────────
    cuerpo = ft.Column(
        [
            ft.Container(height=24),

            # ── Sección: Destinos populares ───────────────────────────────────
            ft.Container(
                padding=ft.padding.symmetric(horizontal=24),
                content=ft.Text("Destinos populares", size=18, weight=ft.FontWeight.BOLD, color=AZUL_OSCURO),
            ),
            ft.Container(height=12),

            # Fila horizontal de tarjetas con scroll lateral
            # padding.only(left=24) para que la primera tarjeta tenga margen izquierdo
            ft.Container(
                padding=ft.padding.only(left=24),
                content=ft.Row(
                    [
                        # Cada tarjeta tiene: ícono, nombre y descripción del destino
                        tarjeta_destino("Portobelo",   "Historia y mar",    ft.Icons.ACCOUNT_BALANCE, "#2451A3"),
                        tarjeta_destino("Isla Grande", "Playa cristalina",  ft.Icons.BEACH_ACCESS,    "#0077B6"),
                        tarjeta_destino("San Lorenzo", "Fuerte colonial",   ft.Icons.FORT,            "#1B3A6B"),
                    ],
                    spacing=16,
                    scroll=ft.ScrollMode.AUTO,   # Permite deslizar horizontalmente
                ),
            ),

            ft.Container(height=28),

            # ── Sección: Explora Colón ────────────────────────────────────────
            ft.Container(
                padding=ft.padding.symmetric(horizontal=24),
                content=ft.Text("Explora Colón", size=18, weight=ft.FontWeight.BOLD, color=AZUL_OSCURO),
            ),
            ft.Container(height=12),

            # Lista vertical de categorías
            ft.Container(
                padding=ft.padding.symmetric(horizontal=24),
                content=ft.Column(
                    [
                        # Cada fila tiene: ícono con color, nombre y flecha a la derecha
                        _fila_categoria("Playas",      ft.Icons.WAVES,           "#0077B6"),
                        _fila_categoria("Historia",    ft.Icons.ACCOUNT_BALANCE, "#1B3A6B"),
                        _fila_categoria("Gastronomía", ft.Icons.RESTAURANT,      "#F5A623"),
                        _fila_categoria("Aventura",    ft.Icons.HIKING,          "#2DAA4D"),
                    ],
                    spacing=10,
                ),
            ),

            ft.Container(height=32),   # Espacio al final para que el scroll no corte el contenido
        ],
        scroll=ft.ScrollMode.AUTO,   # La columna entera es scrolleable verticalmente
        spacing=0,
    )

    # ── Vista completa ────────────────────────────────────────────────────────
    return ft.View(
        "/home",
        bgcolor=GRIS_CLARO,
        padding=0,
        controls=[
            ft.Column(
                [encabezado, cuerpo],
                spacing=0,
                expand=True,   # Ocupar toda la altura de la ventana
            )
        ],
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Funciones auxiliares (fuera de vista_home para que no se recreen cada render)
# ─────────────────────────────────────────────────────────────────────────────

def tarjeta_destino(nombre: str, descripcion: str, icono: str, color: str) -> ft.Container:
    """
    Crea una tarjeta vertical de destino turístico para la sección de populares.

    Parámetros:
      nombre      → Nombre del destino (ej: "Portobelo")
      descripcion → Descripción corta (ej: "Historia y mar")
      icono       → Ícono representativo (ej: ft.Icons.BEACH_ACCESS)
      color       → Color del ícono y su fondo circular (en hex)
    """
    return ft.Container(
        width=160,
        padding=ft.padding.all(16),
        bgcolor=BLANCO,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=12, color="#00000012", offset=ft.Offset(0, 4)),
        content=ft.Column(
            [
                # Círculo de color con el ícono adentro
                # color + "22" agrega "22" al hex para hacerlo transparente al 13%
                # Ejemplo: "#2451A3" + "22" = "#2451A322"
                ft.Container(
                    width=44, height=44,
                    border_radius=22,
                    bgcolor=color + "22",
                    alignment=ft.alignment.center,
                    content=ft.Icon(icono, color=color, size=24),
                ),
                ft.Container(height=10),
                ft.Text(nombre,      size=14, weight=ft.FontWeight.BOLD, color=AZUL_OSCURO),
                ft.Text(descripcion, size=11, color=GRIS),
            ],
            spacing=0,
        ),
    )


def _fila_categoria(nombre: str, icono: str, color: str) -> ft.Container:
    """
    Crea una fila de categoría para la sección "Explora Colón".

    Cada fila tiene: [ícono circular] [nombre] [flecha →]
    El nombre tiene expand=True para empujar la flecha al extremo derecho.
    """
    return ft.Container(
        bgcolor=BLANCO,
        border_radius=16,
        padding=ft.padding.symmetric(horizontal=16, vertical=14),
        shadow=ft.BoxShadow(blur_radius=8, color="#00000010", offset=ft.Offset(0, 2)),
        content=ft.Row(
            [
                # Ícono con fondo circular de color
                ft.Container(
                    width=38, height=38,
                    border_radius=19,
                    bgcolor=color + "22",
                    alignment=ft.alignment.center,
                    content=ft.Icon(icono, color=color, size=20),
                ),
                ft.Container(width=14),   # Espacio entre ícono y texto

                # Nombre de la categoría (expand=True lo estira para llenar el espacio)
                ft.Text(nombre, size=14, weight=ft.FontWeight.W_500, color=AZUL_OSCURO, expand=True),

                # Flecha a la derecha como indicador de que es navegable
                ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=GRIS, size=14),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
