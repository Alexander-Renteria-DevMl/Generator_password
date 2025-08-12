import string
import secrets
import os
from cryptography.fernet import Fernet

CLAVE_FILE = "clave.key"
PASSWORDS_FILE = "contrasenas.enc"

# === Obtener o generar clave de cifrado ===
def obtener_clave():
    if not os.path.exists(CLAVE_FILE):
        clave = Fernet.generate_key()
        with open(CLAVE_FILE, "wb") as f:
            f.write(clave)
    else:
        with open(CLAVE_FILE, "rb") as f:
            clave = f.read()
    return clave

fernet = Fernet(obtener_clave())

# === Generar contraseña segura ===
def generar_contrasena(longitud=13, usar_mayus=True, usar_minus=True, usar_digitos=True, usar_simbolos=True):
    caracteres = ""
    if usar_mayus:
        caracteres += string.ascii_uppercase
    if usar_minus:
        caracteres += string.ascii_lowercase
    if usar_digitos:
        caracteres += string.digits
    if usar_simbolos:
        caracteres += string.punctuation

    if not caracteres:
        raise ValueError("Debe seleccionar al menos un tipo de carácter.")

    return "".join(secrets.choice(caracteres) for _ in range(longitud))

# === Guardar contraseña cifrada ===
def guardar_contrasena(nombre, contrasena):
    registro = f"{nombre}:{contrasena}"
    data_cifrada = fernet.encrypt(registro.encode())
    with open(PASSWORDS_FILE, "ab") as f:
        f.write(data_cifrada + b"\n")

# === Mostrar contraseñas guardadas ===
def mostrar_contrasenas():
    if not os.path.exists(PASSWORDS_FILE):
        print("No hay contraseñas guardadas aún.")
        return

    with open(PASSWORDS_FILE, "rb") as f:
        lineas = f.readlines()

    print("\n--- Contraseñas Guardadas ---")
    for linea in lineas:
        try:
            descifrada = fernet.decrypt(linea.strip()).decode()
            nombre, password = descifrada.split(":")
            print(f"{nombre} → {password}")
        except Exception as e:
            print(f"[ERROR] No se pudo leer una entrada: {e}")

# === Menú principal ===
if __name__ == "__main__":
    while True:
        print("\n=== Gestor de Contraseñas Seguras ===")
        print("1. Generar nueva contraseña")
        print("2. Mostrar contraseñas guardadas")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                longitud = int(input("Ingrese el tamaño de la contraseña (mínimo 8): "))
                if longitud < 8:
                    raise ValueError("La longitud mínima recomendada es de 8 caracteres.")

                nombre = input("Nombre o servicio asociado: ")
                contrasena = generar_contrasena(longitud)
                guardar_contrasena(nombre, contrasena)
                print(f"\nContraseña para '{nombre}': {contrasena} (Guardada de forma segura)")

            except ValueError as e:
                print("Error:", e)

        elif opcion == "2":
            mostrar_contrasenas()

        elif opcion == "3":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")
