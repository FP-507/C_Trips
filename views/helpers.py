# ─────────────────────────────────────────────────────────────────────────────
# helpers.py — Componentes de UI reutilizables
# ─────────────────────────────────────────────────────────────────────────────
# Cada función de este archivo devuelve un widget de Flet ya configurado
# con el estilo visual de la app. Usarlos evita repetir el mismo bloque
# de código en cada pantalla.
#
# Funciones disponibles:
#   campo_texto()    → TextField estilizado para formularios
#   boton_primario() → Botón redondeado con gradiente y animación
#   divider_texto()  → Separador horizontal con texto en el centro
#   icono_social()   → Botón circular para login con Google / Apple / Facebook
# ─────────────────────────────────────────────────────────────────────────────

import flet as ft

# Importamos Animation y AnimationCurve directamente desde el módulo flet
# para evitar el error "ft.animation has no attribute Animation" en Flet 0.80+
from flet import Animation, AnimationCurve

# Importar solo los colores que usamos aquí
from .constants import AZUL_OSCURO, BLANCO, GRIS, GRIS_CLARO


def campo_texto(
    hint: str,
    password: bool = False,
    icon: str | None = None,
) -> ft.TextField:
    """
    Crea un campo de texto con el estilo visual de la app.

    Parámetros:
      hint     → Texto de placeholder que se muestra cuando el campo está vacío
      password → Si es True, oculta el texto y muestra el ojo para revelar
      icon     → Icono a la izquierda del campo (usar ft.Icons.ALGO)

    Ejemplo de uso:
      email_f = campo_texto("Tu email", icon=ft.Icons.EMAIL_OUTLINED)
      pass_f  = campo_texto("Contraseña", password=True, icon=ft.Icons.LOCK_OUTLINED)
    """
    return ft.TextField(
        hint_text=hint,                          # Texto placeholder
        password=password,                       # True = ocultar caracteres
        can_reveal_password=password,            # Muestra el ojo solo si es password
        prefix_icon=icon,                        # Icono a la izquierda
        border_radius=12,                        # Esquinas redondeadas
        bgcolor=GRIS_CLARO,                      # Fondo gris claro por defecto
        border_color="transparent",              # Sin borde visible normalmente
        focused_border_color=AZUL_OSCURO,        # Borde azul al hacer clic
        focused_bgcolor=BLANCO,                  # Fondo blanco al hacer clic
        hint_style=ft.TextStyle(color=GRIS, size=14),          # Estilo del placeholder
        text_style=ft.TextStyle(color=AZUL_OSCURO, size=14),   # Estilo del texto escrito
        height=52,                               # Altura fija para uniformidad
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )


def boton_primario(
    texto: str,
    on_click,
    bgcolor: str = "#F5C842",
    color: str = BLANCO,
    icono: str | None = None,
) -> ft.Container:
    """
    Crea un botón redondeado con animación al presionar.

    Parámetros:
      texto    → Texto visible en el botón
      on_click → Función que se ejecuta al hacer clic (ej: lambda e: page.go("/home"))
      bgcolor  → Color de fondo del botón (por defecto amarillo de la marca)
      color    → Color del texto e ícono (por defecto blanco)
      icono    → Ícono opcional a la derecha del texto (ej: ft.Icons.ARROW_FORWARD)

    Ejemplo de uso:
      boton_primario("Iniciar sesión", on_click=iniciar)
      boton_primario("Crear cuenta",   on_click=lambda e: page.go("/signup"), bgcolor=AZUL_OSCURO)
    """
    # Construimos la fila interna: siempre tiene el texto, y opcionalmente el ícono
    fila: list[ft.Control] = [
        ft.Text(texto, color=color, size=16, weight=ft.FontWeight.BOLD),
    ]

    if icono:
        # Espacio entre el texto y el ícono
        fila.append(ft.Container(width=6))
        # Círculo semitransparente que envuelve el ícono
        fila.append(
            ft.Container(
                width=30, height=30,
                border_radius=15,             # Círculo perfecto (la mitad del ancho)
                bgcolor="#FFFFFF33",           # Blanco con 20% de opacidad
                alignment=ft.alignment.center,
                content=ft.Icon(icono, color=color, size=16),
            )
        )

    return ft.Container(
        height=54,
        border_radius=30,                     # Muy redondeado para aspecto de "píldora"
        bgcolor=bgcolor,
        on_click=on_click,                    # Función a ejecutar al hacer clic
        animate=Animation(100, AnimationCurve.EASE_IN_OUT),  # Animación de 100ms al presionar
        content=ft.Row(fila, alignment=ft.MainAxisAlignment.CENTER, spacing=0),
    )


def divider_texto(texto: str) -> ft.Row:
    """
    Crea un separador horizontal con texto centrado.

    Se usa para separar el login normal del login social:
      ──────── o inicia sesión con ────────

    Parámetro:
      texto → El texto que aparece en el centro
    """
    # Una línea horizontal que se expande para ocupar el espacio disponible
    linea = ft.Container(expand=True, height=1, bgcolor="#E0E0E0")

    return ft.Row(
        [linea, ft.Text(f"  {texto}  ", size=12, color=GRIS), linea],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Alinear verticalmente al centro
    )


def icono_social(icono: str, color: str, on_click=None) -> ft.Container:
    """
    Crea un botón circular para opciones de login social (Google, Apple, Facebook).

    Parámetros:
      icono    → Ícono a mostrar (ej: ft.Icons.LANGUAGE para Google)
      color    → Color del ícono (ej: "#DB4437" para rojo de Google)
      on_click → Función a ejecutar al hacer clic (opcional)

    El botón tiene sombra suave para dar sensación de elevación.
    """
    return ft.Container(
        width=50, height=50,
        border_radius=25,                       # Círculo perfecto
        bgcolor=BLANCO,
        border=ft.border.all(1, "#E0E0E0"),     # Borde gris muy sutil
        alignment=ft.alignment.center,
        on_click=on_click,
        shadow=ft.BoxShadow(
            blur_radius=6,
            color="#00000010",                  # Negro al 6% de opacidad
            offset=ft.Offset(0, 2),             # Sombra desplazada 2px hacia abajo
        ),
        content=ft.Icon(icono, color=color, size=22),
    )
