# ─────────────────────────────────────────────────────────────────────────────
# sign_in.py — Pantalla de inicio de sesión
# ─────────────────────────────────────────────────────────────────────────────
# Permite a usuarios con cuenta registrada entrar a la app.
# Llama a autenticar_usuario() de db.py para verificar credenciales.
# Si el login es exitoso, guarda los datos del usuario en page.session
# y navega a "/home".
# ─────────────────────────────────────────────────────────────────────────────

from typing import Any   # Para anotar el tipo del evento sin depender de Flet internamente
import flet as ft
from .constants import AMARILLO, AZUL_OSCURO, AZUL_MEDIO, BLANCO, GRIS, ROJO_ERROR
from .helpers import campo_texto, boton_primario, divider_texto, icono_social
from .db import autenticar_usuario


def vista_sign_in(page: ft.Page) -> ft.View:
    """
    Construye la pantalla de inicio de sesión.

    Elementos:
      - Campos de email y contraseña
      - Mensaje de error (oculto hasta que se necesite)
      - Botón "Iniciar sesión" que llama a la función iniciar()
      - Opciones de login social (Google, Apple, Facebook) — decorativas
      - Link para ir al registro
    """

    # ── Campos del formulario ─────────────────────────────────────────────────
    email_f = campo_texto("Email", icon=ft.Icons.EMAIL_OUTLINED)
    pass_f  = campo_texto("Contraseña", password=True, icon=ft.Icons.LOCK_OUTLINED)

    # Texto de error: comienza invisible y se muestra si algo falla
    error = ft.Text("", color=ROJO_ERROR, size=12, visible=False)

    # ── Función que se ejecuta al presionar "Iniciar sesión" ──────────────────
    def iniciar(e: Any) -> None:
        """
        Valida las credenciales contra la base de datos CSV.

        El try/except captura cualquier error inesperado (por ejemplo,
        si el archivo CSV no se puede leer) y lo muestra en pantalla
        en lugar de que la app se congele silenciosamente.
        """
        try:
            # Llamar a la función de db.py que verifica email y contraseña
            # "or ''" convierte None a cadena vacía si el campo está vacío
            exito, mensaje, usuario = autenticar_usuario(
                email_f.value or "", pass_f.value or ""
            )
        except Exception as ex:
            # Error inesperado (ej: problema al leer el CSV)
            error.value   = f"Error interno: {ex}"
            error.visible = True
            page.update()
            return

        if not exito:
            # Credenciales incorrectas → mostrar el mensaje de error
            error.value   = mensaje
            error.visible = True
            page.update()
            return

        # ── Login exitoso ─────────────────────────────────────────────────────
        error.visible = False

        # Guardar los datos del usuario en la sesión para usarlos en otras pantallas
        # page.session es un almacenamiento clave-valor que dura mientras la app está abierta
        page.session.set("usuario", usuario)

        page.update()
        page.go("/home")   # Navegar a la pantalla principal

    # ── Tarjeta blanca con el formulario ─────────────────────────────────────
    tarjeta = ft.Container(
        margin=ft.margin.symmetric(horizontal=20, vertical=20),
        padding=ft.padding.all(28),
        bgcolor=BLANCO,
        border_radius=28,
        shadow=ft.BoxShadow(blur_radius=20, color="#00000012", offset=ft.Offset(0, 4)),
        content=ft.Column(
            [
                # Título con palabras en distintos estilos (usando spans)
                # ft.Text con spans permite mezclar estilos dentro de la misma línea
                ft.Text(spans=[
                    ft.TextSpan("Let's ",  style=ft.TextStyle(size=26, color=AZUL_OSCURO)),
                    ft.TextSpan("Travel ", style=ft.TextStyle(size=26, weight=ft.FontWeight.BOLD, color=AZUL_OSCURO)),
                    ft.TextSpan("you ",    style=ft.TextStyle(size=26, color=AZUL_OSCURO)),
                    ft.TextSpan("in.",     style=ft.TextStyle(size=26, weight=ft.FontWeight.BOLD, color=AZUL_MEDIO)),
                ]),

                ft.Container(height=4),
                ft.Text("Descubre el mundo con cada inicio de sesión", size=13, color=GRIS),
                ft.Container(height=20),

                # Campos del formulario
                email_f,
                ft.Container(height=10),
                pass_f,
                ft.Container(height=4),

                # Mensaje de error (invisible hasta que ocurra un error)
                error,

                # Link "Olvidé mi contraseña" alineado a la derecha
                ft.Row(
                    [ft.TextButton("Olvidé mi contraseña", style=ft.ButtonStyle(color=AZUL_MEDIO))],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Container(height=8),

                # Botón principal de login
                boton_primario("Iniciar sesión", on_click=iniciar),

                ft.Container(height=16),

                # Separador "o inicia sesión con"
                divider_texto("o inicia sesión con"),

                ft.Container(height=16),

                # Botones de login social (solo visuales, sin funcionalidad real aún)
                ft.Row(
                    [
                        icono_social(ft.Icons.LANGUAGE,     "#DB4437"),  # Google (rojo)
                        icono_social(ft.Icons.PHONE_IPHONE, "#111111"),  # Apple (negro)
                        icono_social(ft.Icons.FACEBOOK,     "#1877F2"),  # Facebook (azul)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=16,
                ),

                ft.Container(height=20),

                # Link para ir al registro
                ft.Row(
                    [
                        ft.Text("¿No tienes cuenta?", size=13, color=GRIS),
                        ft.TextButton(
                            "Regístrate",
                            style=ft.ButtonStyle(color=AZUL_MEDIO),
                            on_click=lambda e: page.go("/signup"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                ),

                ft.Container(height=4),

                # Botón alternativo para ir directamente al registro
                boton_primario(
                    "Crear cuenta",
                    on_click=lambda e: page.go("/signup"),
                    bgcolor=AZUL_OSCURO,   # Botón azul para diferenciarlo del principal
                ),
                ft.Container(height=8),
            ],
            spacing=0,
        ),
    )

    # ── Vista completa ────────────────────────────────────────────────────────
    return ft.View(
        "/signin",
        bgcolor=AMARILLO,     # Fondo amarillo de la marca
        padding=0,
        # AppBar: barra superior con botón de retroceso y título
        appbar=ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS_NEW,
                icon_color=AZUL_OSCURO,
                on_click=lambda e: page.go("/getstarted"),  # Volver a la pantalla anterior
            ),
            bgcolor=AMARILLO,
            elevation=0,       # Sin sombra en la barra superior
            title=ft.Text("CTRIP'S", color=AZUL_OSCURO, weight=ft.FontWeight.BOLD, size=18),
            center_title=True, # Centrar el título
        ),
        # expand=True hace que la columna ocupe toda la altura disponible
        controls=[ft.Column([tarjeta], scroll=ft.ScrollMode.AUTO, expand=True)],
    )
