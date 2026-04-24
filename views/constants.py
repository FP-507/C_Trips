# ─────────────────────────────────────────────────────────────────────────────
# constants.py — Paleta de colores de la app
# ─────────────────────────────────────────────────────────────────────────────
# Centralizar los colores aquí tiene dos ventajas:
#   1. Si se quiere cambiar un color, se modifica en UN solo lugar.
#   2. Los nombres descriptivos hacen el código más legible que poner
#      "#F5C842" disperso por todos lados.
#
# Los valores son cadenas de texto en formato hexadecimal RGB (#RRGGBB).
# El formato #RRGGBBAA incluye canal alfa (transparencia); 00=transparente, FF=opaco.
# ─────────────────────────────────────────────────────────────────────────────

AMARILLO    = "#F5C842"   # Color principal de la marca; fondos de pantallas de auth
AZUL_OSCURO = "#1B3A6B"   # Azul marino; textos principales, botón secundario
AZUL_MEDIO  = "#2451A3"   # Azul intermedio; acentos, links, gradiente de encabezado
BLANCO      = "#FFFFFF"   # Blanco puro; tarjetas, textos sobre fondos oscuros
GRIS        = "#888888"   # Gris medio; textos secundarios, placeholders
GRIS_CLARO  = "#F3F3F5"   # Gris muy claro; fondo de pantallas interiores
OVERLAY     = "#00000060" # Negro semitransparente (37% opacidad) para oscurecer imágenes
ROJO_ERROR  = "#D4183D"   # Rojo vivo; mensajes de error en formularios
