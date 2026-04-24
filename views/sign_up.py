# ─────────────────────────────────────────────────────────────────────────────
# sign_up.py — Pantalla de registro de nueva cuenta
# ─────────────────────────────────────────────────────────────────────────────
# Permite crear una cuenta nueva. Recopila nombre, email y contraseña,
# los valida y los guarda en el CSV a través de registrar_usuario() de db.py.
# Tras un registro exitoso, navega automáticamente a la pantalla de login.
# ─────────────────────────────────────────────────────────────────────────────

from typing import Any
import flet as ft
from .constants import AMARILLO, AZUL_OSCURO, AZUL_MEDIO, BLANCO, GRIS, ROJO_ERROR
from .helpers import campo_texto, boton_primario
from .db import registrar_usuario


def vista_sign_up(page: ft.Page) -> ft.View:
    """
    Construye la pantalla de registro.

    Elementos:
      - Campos: nombre completo, email, contraseña, confirmar contraseña
      - Mensaje de error (oculto hasta que sea necesario)
      - Botón "Registrarse" que llama a la función registrar()
      - Link para volver al login
    """

    # ── Campos del formulario ─────────────────────────────────────────────────
    nombre_f = campo_texto("Nombre completo",               icon=ft.Icons.PERSON_OUTLINED)
    email_f  = campo_texto("Correo electrónico",            icon=ft.Icons.EMAIL_OUTLINED)
    pass_f   = campo_texto("Contraseña (mín. 6 caracteres)", password=True, icon=ft.Icons.LOCK_OUTLINED)
    pass_f2  = campo_texto("Confirmar contraseña",          password=True, icon=ft.Icons.LOCK_OUTLINED)

    # Texto de error: empieza oculto
    error = ft.Text("", color=ROJO_ERROR, size=12, visible=False)

    # ── Función que se ejecuta al presionar "Registrarse" ────────────────────
    def registrar(e: Any) -> None:
        """
        Verifica que las contraseñas coincidan y llama a registrar_usuario().

        La validación de contraseñas coincidentes se hace aquí (en la vista)
        porque involucra dos campos de la pantalla. Las demás validaciones
        (email válido, contraseña suficientemente larga, email no duplicado)
        las hace db.py, que es quien conoce las reglas de negocio.
        """

        # Verificación local: las contraseñas deben ser iguales
        if pass_f.value != pass_f2.value:
            error.value   = "Las contraseñas no coinciden"
            error.visible = True
            page.update()
            return

        try:
            # Llamar a db.py para validar y guardar el usuario
            # db.py verifica: campos vacíos, formato de email, longitud de password, email duplicado
            exito, mensaje = registrar_usuario(
                nombre_f.value or "",
                email_f.value  or "",
                pass_f.value   or "",
            )
        except Exception as ex:
            # Error inesperado (ej: no se pudo escribir el CSV por permisos)
            error.value   = f"Error interno: {ex}"
            error.visible = True
            page.update()
            return

        if not exito:
            # Alguna validación de db.py falló → mostrar el mensaje
            error.value   = mensaje
            error.visible = True
            page.update()
            return

        # ── Registro exitoso ──────────────────────────────────────────────────
        error.visible = False
        page.update()

        # Redirigir al login para que el usuario inicie sesión con su nueva cuenta
        page.go("/signin")

    # ── Tarjeta con el formulario ─────────────────────────────────────────────
    tarjeta = ft.Container(
        margin=ft.margin.symmetric(horizontal=20, vertical=20),
        padding=ft.padding.all(28),
        bgcolor=BLANCO,
        border_radius=28,
        shadow=ft.BoxShadow(blur_radius=20, color="#00000012", offset=ft.Offset(0, 4)),
        content=ft.Column(
            [
                ft.Text("Crear cuenta", size=26, weight=ft.FontWeight.BOLD, color=AZUL_OSCURO),
                ft.Container(height=4),
                ft.Text("Únete a CTRIP'S y empieza a explorar", size=13, color=GRIS),
                ft.Container(height=20),

                # Campos del formulario en orden lógico
                nombre_f,
                ft.Container(height=10),
                email_f,
                ft.Container(height=10),
                pass_f,
                ft.Container(height=10),
                pass_f2,
                ft.Container(height=8),

                # Mensaje de error (oculto por defecto)
                error,
                ft.Container(height=10),

                # Botón de registro
                boton_primario("Registrarse", on_click=registrar),

                ft.Container(height=20),

                # Link para usuarios que ya tienen cuenta
                ft.Row(
                    [
                        ft.Text("¿Ya tienes cuenta?", size=13, color=GRIS),
                        ft.TextButton(
                            "Inicia sesión",
                            style=ft.ButtonStyle(color=AZUL_MEDIO),
                            on_click=lambda e: page.go("/signin"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                ),
                ft.Container(height=8),
            ],
            spacing=0,
        ),
    )

    # ── Vista completa ────────────────────────────────────────────────────────
    return ft.View(
        "/signup",
        bgcolor=AMARILLO,
        padding=0,
        appbar=ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS_NEW,
                icon_color=AZUL_OSCURO,
                on_click=lambda e: page.go("/signin"),  # Volver al login
            ),
            bgcolor=AMARILLO,
            elevation=0,
            title=ft.Text("CTRIP'S", color=AZUL_OSCURO, weight=ft.FontWeight.BOLD, size=18),
            center_title=True,
        ),
        controls=[ft.Column([tarjeta], scroll=ft.ScrollMode.AUTO, expand=True)],
    )
