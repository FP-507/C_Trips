# ─────────────────────────────────────────────────────────────────────────────
# get_started.py — Pantalla de presentación "Get Started"
# ─────────────────────────────────────────────────────────────────────────────
# Segunda pantalla de la app. Muestra:
#   - Una imagen de fondo de playa/viaje (local, caché o URL online)
#   - Una tarjeta blanca con el CTA (Call To Action) principal
#   - Un botón "Sign now" que lleva al inicio de sesión
#
# La imagen se obtiene a través de image_utils.py, que maneja
# automáticamente la prioridad: assets/ → caché → URL online → degradado.
# ─────────────────────────────────────────────────────────────────────────────

import flet as ft
from .constants import AMARILLO, AZUL_OSCURO, BLANCO, GRIS, GRIS_CLARO, OVERLAY
from .helpers import boton_primario
from .image_utils import obtener_src_imagen


def vista_get_started(page: ft.Page) -> ft.View:
    """
    Construye la pantalla "Get Started".

    La pantalla tiene dos partes:
      1. Encabezado (430px de alto): imagen con overlay oscuro + título
      2. Tarjeta blanca inferior: descripción + botón de acción
    """

    # ── Obtener la fuente de la imagen ────────────────────────────────────────
    # obtener_src_imagen() devuelve (ruta_o_url, es_url)
    # Si src es None (sin imagen y sin internet), se usa el degradado.
    src, es_url = obtener_src_imagen()

    # ── Construir el fondo del encabezado ─────────────────────────────────────
    if src:
        # ── Caso 1: tenemos imagen (local o URL) ─────────────────────────────
        # ft.Stack apila capas; la última capa queda encima visualmente.
        fondo = ft.Stack([

            # Capa 1: la imagen de fondo
            # error_content: se muestra si la imagen no carga (sin internet, etc.)
            ft.Image(
                src=src,
                width=390, height=430,
                fit=ft.ImageFit.COVER,    # Recortar para llenar el espacio
                error_content=ft.Icon(ft.Icons.BEACH_ACCESS, size=60, color="#FFFFFF55"),
            ),

            # Capa 2: overlay semitransparente para oscurecer la imagen
            # Esto hace que el texto blanco encima sea legible
            ft.Container(width=390, height=430, bgcolor=OVERLAY),

            # Capa 3: contenido de texto encima de la imagen
            ft.Container(
                width=390, height=430,
                padding=ft.padding.only(left=20, right=20, top=50, bottom=24),
                content=ft.Column(
                    [
                        # Selector de idioma (decorativo, en la esquina derecha)
                        ft.Row(
                            [
                                ft.Text("English", color=BLANCO, size=14, weight=ft.FontWeight.W_500),
                                ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=BLANCO, size=18),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        ft.Container(expand=True),  # Empujar el título hacia abajo
                        # Nombre de la app sobre la imagen
                        ft.Text(
                            "CTRIP'S",
                            size=42, weight=ft.FontWeight.BOLD,
                            color=BLANCO,
                            style=ft.TextStyle(letter_spacing=3),
                        ),
                        ft.Container(height=12),
                    ],
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
        ])

    else:
        # ── Caso 2: sin imagen ni internet → degradado azul de fallback ──────
        fondo = ft.Container(
            width=390, height=430,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#0077B6", "#023E8A"],   # Dos tonos de azul océano
            ),
            padding=ft.padding.only(left=20, right=20, top=50, bottom=24),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("English", color=BLANCO, size=14, weight=ft.FontWeight.W_500),
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=BLANCO, size=18),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Container(expand=True),
                    # Ícono decorativo cuando no hay imagen
                    ft.Icon(ft.Icons.BEACH_ACCESS, size=60, color="#FFFFFF55"),
                    ft.Container(height=8),
                    ft.Text(
                        "CTRIP'S",
                        size=42, weight=ft.FontWeight.BOLD,
                        color=BLANCO,
                        style=ft.TextStyle(letter_spacing=3),
                    ),
                    ft.Container(height=12),
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    # ── Encabezado: el fondo recortado con esquinas inferiores redondeadas ────
    encabezado = ft.Container(
        height=430,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,  # Recortar estrictamente al borde
        border_radius=ft.border_radius.only(
            bottom_left=36, bottom_right=36    # Solo las esquinas de abajo son redondas
        ),
        content=fondo,
    )

    # ── Tarjeta blanca con el CTA ─────────────────────────────────────────────
    tarjeta = ft.Container(
        margin=ft.margin.symmetric(horizontal=20),   # Márgenes laterales de 20px
        padding=ft.padding.symmetric(horizontal=28, vertical=30),
        bgcolor=BLANCO,
        border_radius=28,
        shadow=ft.BoxShadow(
            blur_radius=24, spread_radius=0,
            color="#00000018",                  # Sombra negra muy suave
            offset=ft.Offset(0, 6),             # Sombra desplazada 6px hacia abajo
        ),
        content=ft.Column(
            [
                # Título en dos líneas
                ft.Text("Ready to explore the",  size=22, weight=ft.FontWeight.BOLD, color=AZUL_OSCURO, text_align=ft.TextAlign.CENTER),
                ft.Text("beauty of Colon?",       size=22, weight=ft.FontWeight.BOLD, color=AZUL_OSCURO, text_align=ft.TextAlign.CENTER),
                ft.Container(height=6),
                # Subtítulo descriptivo
                ft.Text(
                    "Discover stunning beaches, islands and history",
                    size=13, color=GRIS,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=24),
                # Botón principal → navega a la pantalla de login
                boton_primario(
                    "Sign now",
                    on_click=lambda e: page.go("/signin"),
                    icono=ft.Icons.ARROW_FORWARD,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
    )

    # ── Vista completa ────────────────────────────────────────────────────────
    return ft.View(
        "/getstarted",
        bgcolor=GRIS_CLARO,
        padding=0,
        controls=[
            # ft.Column con scroll para que funcione en pantallas pequeñas
            ft.Column(
                [encabezado, ft.Container(height=24), tarjeta, ft.Container(height=24)],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            )
        ],
    )
