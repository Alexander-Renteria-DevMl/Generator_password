import string
import secrets  # Más seguro que random para criptografía

def generar_contrasena(longitud=16, usar_mayus=True, usar_minus=True, usar_digitos=True, usar_simbolos=True):
    """Genera una contraseña segura según los parámetros indicados."""

    # Construir conjunto de caracteres permitido
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

    # Generar contraseña usando 'secrets' para mayor seguridad
    contrasena = "".join(secrets.choice(caracteres) for _ in range(longitud))
    return contrasena

if __name__ == "__main__":
    try:
        longitud = int(input("Ingrese el tamaño de la contraseña (mínimo 8): "))
        if longitud < 8:
            raise ValueError("La longitud mínima recomendada es de 8 caracteres.")

        contrasena = generar_contrasena(longitud)
        print("\nContraseña generada:", contrasena)

    except ValueError as e:
        print("Error:", e)
