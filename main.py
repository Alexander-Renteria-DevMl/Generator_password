import string
import random

longitud= int(input("Ingrese el tamaño de la contraseña"))
caracteres=string.ascii_letters + string.digits + string.punctuation
contrasena= "".join(ranndom.choice(caracteres) for i in range(longitud))
print("La contraseña generada es : "+contrasena)
