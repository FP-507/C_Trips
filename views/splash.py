# ─────────────────────────────────────────────────────────────────────────────
# splash.py — Pantalla de inicio (Splash Screen)
# ─────────────────────────────────────────────────────────────────────────────
# Es la primera pantalla que ve el usuario al abrir la app.
# Muestra el logo de CTRIP'S sobre fondo amarillo.
# Al tocar cualquier parte de la pantalla, navega a "/getstarted".
# ─────────────────────────────────────────────────────────────────────────────

import flet as ft
from .constants import AMARILLO, AZUL_OSCURO, BLANCO


def vista_splash(page: ft.Page) -> ft.View:
    """
    Construye y devuelve la vista del Splash Screen.

    El logo está compuesto por varias capas apiladas con ft.Stack:
      - Círculo exterior con borde blanco
      - Fondo interior semitransparente
      - Ícono de palmera centrado
      - Ícono de olas en la parte inferior
      - Línea orbital diagonal decorativa
    """

    # ── Logo circular con capas apiladas ─────────────────────────────────────
    # ft.Stack posiciona sus hijos en capas una encima de la otra,
    # todos anclados en la esquina superior izquierda por defecto.
    logo = ft.Container(
        width=190, height=190,
        content=ft.Stack([

            # Capa 1: círculo exterior con borde blanco
            ft.Container(
                width=190, height=190,
                border_radius=95,              # Radio = mitad del ancho → círculo perfecto
                border=ft.border.all(3, BLANCO),  # Borde de 3px blanco
            ),

            # Capa 2: relleno semitransparente del círculo (da sensación de vidrio)
            ft.Container(
                width=190, height=190,
                border_radius=95,
                bgcolor="#FFFFFF20",           # Blanco con ~12% de opacidad
            ),

            # Capa 3: ícono de palmera centrado y subido para dejar espacio a las olas
            ft.Container(
                width=190, height=190,
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=30),  # Subir el ícono 30px
                content=ft.Icon(ft.Icons.PARK, size=80, color=BLANCO),
            ),

            # Capa 4: ícono de olas en la parte inferior del círculo
            ft.Container(
                width=190, height=190,
                alignment=ft.alignment.bottom_center,
                padding=ft.padding.only(bottom=22),
                content=ft.Row(
                    [ft.Icon(ft.Icons.WAVES, size=44, color=ft.Colors.BLUE_300)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),

            # Capa 5: línea diagonal decorativa (simula una órbita)
            ft.Container(
                width=190, height=190,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=220, height=3,
                    bgcolor="#FFFFFF40",        # Blanco al 25% de opacidad
                    border_radius=2,
                    rotate=ft.Rotate(angle=-0.45),  # Rotar ~26 grados en sentido antihorario
                ),
            ),
        ]),
    )

    # ── Vista completa ────────────────────────────────────────────────────────
    # ft.View define una pantalla completa con su ruta, color de fondo y controles.
    return ft.View(
        "/",                   # Ruta que identifica esta pantalla en el router
        bgcolor=AMARILLO,      # Fondo amarillo de marca en toda la pantalla
        padding=0,             # Sin márgenes para que el fondo cubra todo

        controls=[
            # Container que ocupa toda la pantalla y detecta el toque
            ft.Container(
                expand=True,                          # Expandirse para llenar la pantalla
                bgcolor=AMARILLO,
                alignment=ft.alignment.center,        # Centrar el contenido
                on_click=lambda e: page.go("/getstarted"),  # Navegar al tocar

                content=ft.Column(
                    [
                        logo,

                        ft.Container(height=28),   # Espacio vertical

                        # Nombre de la app
                        ft.Text(
                            "CTRIP'S",
                            size=46, weight=ft.FontWeight.BOLD,
                            color=AZUL_OSCURO,
                            style=ft.TextStyle(letter_spacing=3),  # Espaciado entre letras
                        ),

                        ft.Container(height=8),

                        # Slogan de la app
                        ft.Text(
                            "A TRIP FOR THE SOUL, A HISTORY FOR THE HOLD",
                            size=11, color=AZUL_OSCURO,
                            weight=ft.FontWeight.W_600,
                            text_align=ft.TextAlign.CENTER,
                            style=ft.TextStyle(letter_spacing=1.2),
                        ),

                        ft.Container(height=60),

                        # Indicador de puntos (como en apps de onboarding)
                        # El punto más largo indica que estamos en la primera pantalla
                        ft.Row(
                            [
                                ft.Container(width=8,  height=8, border_radius=4, bgcolor=AZUL_OSCURO),
                                ft.Container(width=20, height=8, border_radius=4, bgcolor=AZUL_OSCURO),  # punto activo
                                ft.Container(width=8,  height=8, border_radius=4, bgcolor="#1B3A6B55"),  # punto inactivo (semitransparente)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=6,
                        ),

                        ft.Container(height=20),

                        # Instrucción para el usuario
                        ft.Text("Toca para comenzar", size=12, color="#1B3A6B88"),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            )
        ],
    )
