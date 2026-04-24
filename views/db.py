# ─────────────────────────────────────────────────────────────────────────────
# db.py — Base de datos de usuarios (archivo CSV)
# ─────────────────────────────────────────────────────────────────────────────
# Este módulo es la única parte de la app que toca el archivo de usuarios.
# Todas las demás pantallas deben usar las funciones públicas de aquí;
# ninguna pantalla abre el CSV directamente.
#
# Estructura del CSV (data/usuarios.csv):
#   nombre        → Nombre completo del usuario
#   email         → Correo en minúsculas, sirve como identificador único
#   password_hash → SHA-256 del password; NUNCA se guarda el password real
#
# ¿Por qué hashear contraseñas?
#   Si alguien abre el CSV a mano no verá las contraseñas reales, solo
#   una cadena de 64 caracteres sin sentido. SHA-256 es una función de
#   un solo sentido: no se puede "revertir" para obtener la contraseña.
# ─────────────────────────────────────────────────────────────────────────────

import csv       # Para leer y escribir archivos CSV de forma estructurada
import hashlib   # Para calcular el hash SHA-256 de las contraseñas
import os        # Para trabajar con rutas y verificar si existen archivos
import re        # Para validar el formato del email con expresiones regulares

# ── Ruta al archivo CSV ───────────────────────────────────────────────────────
# Este archivo está en C_Trips/views/db.py
# Subimos dos niveles para llegar a C_Trips/, luego entramos a data/
_BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(_BASE, "data", "usuarios.csv")

# ── Nombres de las columnas del CSV ──────────────────────────────────────────
# Se usan al crear el encabezado y al leer/escribir filas como diccionarios.
_CAMPOS = ["nombre", "email", "password_hash"]

# ── Expresión regular para validar emails ────────────────────────────────────
# El patrón exige: algo@algo.algo
# [^@\s]+ → uno o más caracteres que NO sean @ ni espacios
# Esto rechaza correos como "sin_arroba", "a@", "@sin_dominio", etc.
_RE_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ═════════════════════════════════════════════════════════════════════════════
#  FUNCIONES INTERNAS (privadas — no usar desde afuera)
# ═════════════════════════════════════════════════════════════════════════════

def _hash(password: str) -> str:
    """
    Convierte una contraseña en texto plano a su hash SHA-256.

    Ejemplo:
      "123456" → "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"

    El resultado siempre tiene 64 caracteres hexadecimales.
    La misma contraseña siempre produce el mismo hash, lo que permite
    comparar sin guardar la contraseña real.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def _inicializar() -> None:
    """
    Crea el archivo CSV con su fila de encabezado si todavía no existe.

    Se llama automáticamente antes de cada lectura, así que nunca hay que
    preocuparse por crear el archivo a mano.
    """
    if not os.path.exists(CSV_PATH):
        # "w" = modo escritura; newline="" evita líneas en blanco dobles en Windows
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=_CAMPOS).writeheader()


def _leer_todos() -> list[dict]:
    """
    Lee todos los usuarios del CSV y los devuelve como lista de diccionarios.

    Cada diccionario tiene las claves: "nombre", "email", "password_hash".
    Si el archivo está vacío (solo encabezado), devuelve una lista vacía [].
    """
    _inicializar()   # Asegurarse de que el archivo existe antes de leerlo
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        # DictReader convierte cada fila en un dict usando el encabezado como claves
        return list(csv.DictReader(f))


def _escribir_todos(usuarios: list[dict]) -> None:
    """
    Reemplaza todo el contenido del CSV con la lista de usuarios dada.

    Se usa después de agregar un nuevo usuario: se lee la lista completa,
    se añade el nuevo usuario, y se escribe todo de vuelta.
    """
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=_CAMPOS)
        w.writeheader()      # Escribe la fila de títulos
        w.writerows(usuarios)  # Escribe todas las filas de datos


# ═════════════════════════════════════════════════════════════════════════════
#  FUNCIONES PÚBLICAS (usar desde sign_in.py y sign_up.py)
# ═════════════════════════════════════════════════════════════════════════════

def email_valido(email: str) -> bool:
    """
    Verifica que el email tenga un formato básico válido (algo@algo.algo).
    Devuelve True si es válido, False si no lo es.
    """
    return bool(_RE_EMAIL.match(email.strip()))


def email_existe(email: str) -> bool:
    """
    Verifica si ya hay una cuenta registrada con ese email.
    La comparación ignora mayúsculas/minúsculas.
    """
    return any(u["email"].lower() == email.strip().lower() for u in _leer_todos())


def registrar_usuario(nombre: str, email: str, password: str) -> tuple[bool, str]:
    """
    Registra un nuevo usuario en el CSV después de validar todos los datos.

    Validaciones en orden:
      1. Ningún campo puede estar vacío
      2. El email debe tener formato válido
      3. La contraseña debe tener al menos 6 caracteres
      4. El email no puede estar ya registrado

    Retorna una tupla (éxito, mensaje):
      - (True,  "Cuenta creada para Juan")  → todo bien
      - (False, "Ya existe una cuenta...")  → hay un error, mostrar al usuario
    """
    # Limpiar espacios accidentales al inicio/final
    nombre = nombre.strip()
    email  = email.strip().lower()   # Guardar siempre en minúsculas

    # ── Validaciones ─────────────────────────────────────────────────────────
    if not nombre or not email or not password:
        return False, "Todos los campos son obligatorios"

    if not email_valido(email):
        return False, "El formato del email no es válido"

    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"

    if email_existe(email):
        return False, "Ya existe una cuenta con ese email"

    # ── Guardar el nuevo usuario ──────────────────────────────────────────────
    usuarios = _leer_todos()          # Leer usuarios actuales
    usuarios.append({
        "nombre":        nombre,
        "email":         email,
        "password_hash": _hash(password),  # Guardar hash, NUNCA la contraseña real
    })
    _escribir_todos(usuarios)         # Escribir la lista actualizada al CSV

    return True, f"Cuenta creada para {nombre}"


def autenticar_usuario(email: str, password: str) -> tuple[bool, str, dict | None]:
    """
    Verifica si el email y la contraseña corresponden a una cuenta registrada.

    Proceso:
      1. Busca un usuario con ese email en el CSV
      2. Si lo encuentra, compara el hash de la contraseña ingresada
         con el hash guardado
      3. Si coinciden, el login es exitoso

    Retorna una tupla (éxito, mensaje, datos_usuario):
      - (True,  "Bienvenido, Juan!", {"nombre": "Juan", "email": ...})
      - (False, "Contraseña incorrecta", None)
      - (False, "No existe una cuenta...", None)
    """
    email = email.strip().lower()

    # Validación mínima antes de buscar en el CSV
    if not email or not password:
        return False, "Por favor completa todos los campos", None

    # Recorrer todos los usuarios buscando el email
    for usuario in _leer_todos():
        if usuario["email"] == email:
            # Email encontrado — ahora verificar la contraseña
            if usuario["password_hash"] == _hash(password):
                # Hash coincide → login exitoso, devolver datos del usuario
                return True, f"Bienvenido, {usuario['nombre']}!", usuario
            # Hash no coincide → contraseña incorrecta
            return False, "Contraseña incorrecta", None

    # Ninguna fila tenía ese email
    return False, "No existe una cuenta con ese email", None
