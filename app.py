# app.py
import string
import secrets
import os
from cryptography.fernet import Fernet
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query

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

# === Backend con FastAPI ===
app = FastAPI()

# Permitir acceso desde tu HTML local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generador de contreaseñas

@app.get("/generate")
def generate_password(length: int = Query(12), name: str = Query(...)):
    password = generar_contrasena(length)  # función actual
    guardar_contrasena(name, password)     # guardar con nombre y pass
    return {"name": name, "password": password}


@app.get("/")
def home():
    return HTMLResponse("<h1>API funcionando ✅</h1><p>Usa /generate para generar contraseñas.</p>")

# Historial de contraseñas
@app.get("/list")
def list_passwords():
    if not os.path.exists(PASSWORDS_FILE):
        return []
    contrasenas = []
    with open(PASSWORDS_FILE, "rb") as f:
        lineas = f.readlines()
    for linea in lineas:
        try:
            descifrada = fernet.decrypt(linea.strip()).decode()
            nombre, password = descifrada.split(":")
            contrasenas.append({"name": nombre, "password": password})
        except Exception:
            continue
    return contrasenas
# Borrar Historial de Contraseñas
@app.delete("/delete")
def delete_password():
    if os.path.exists(PASSWORDS_FILE):
        os.remove(PASSWORDS_FILE)
        return{"status":"ok","message":"Historial Eliminado"}
    return{"status":"ok","message":"Historial Vacio"}

