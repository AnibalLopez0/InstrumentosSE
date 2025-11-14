# interfaz.py
import base
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO
import urllib.request
import unicodedata


# URLs de imágenes por instrumento
IMAGENES = {
    "guitarra_clasica": "https://upload.wikimedia.org/wikipedia/commons/4/45/Guitarra.jpg",
    "guitarra_acustica": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Acoustic_guitar.jpg",
    "guitarra_electrica": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Fender_Stratocaster.jpg",
    "bajo_electrico": "https://imgs.search.brave.com/3g7r7W4UkHrhplEYSCnevuKgc-AQFviV0tRKdAupj74/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/Z2l0YXJyZW50b3Rh/bC5jaC93cC1jb250/ZW50L3VwbG9hZHMv/MjAyMS8wNi9GZW5k/ZXJQcmVjaXNpb25C/YXNzQW1lcmljYW5Q/cm9mZXNzaW9uYWxJ/SU1pYW1pQmx1ZS0x/LTEwMjR4Mzg5Lmpw/Zw",
    "violin": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Violin_VL129.png",
    "piano": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Grand_piano_interior.jpg",
    "banjo": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Banjo_Example.jpg"
    # Hay que agregar más imágenes según los instrumentos definidos, solo sirve la del bajo
}
def normalize_key(s: str) -> str:
    """Normaliza una cadena para comparar claves:
       - cambia '_' por espacio
       - quita tildes/diacríticos
       - pasa a minúsculas y recorta espacios
    """
    if not isinstance(s, str):
        return ""
    s = s.replace("_", " ")
    s = s.strip().lower()
    # quitar tildes
    s = ''.join(ch for ch in unicodedata.normalize('NFKD', s) if not unicodedata.combining(ch))
    return s


# Crear un diccionario con claves normalizadas para búsqueda rápida
IMAGENES_NORMALIZADAS = {normalize_key(k): v for k, v in IMAGENES.items()}


# -----------------------------
# DESCARGA DE IMAGEN (urllib)
# -----------------------------
def descargar_imagen_url(url: str):
    """Descarga una imagen desde una url y retorna un objeto PIL.Image o None."""
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = resp.read()
        img = Image.open(BytesIO(data))
        img = img.convert("RGBA")  # asegurar formato compatible
        return img
    except Exception as e:
        # No hacemos crash; devolvemos None para manejarlo en la UI
        print("Error descargando imagen:", e)
        return None


# -----------------------------
# INTERFAZ
# -----------------------------
class Interfaz:
    def __init__(self, root):
        root.title("Sistema Experto – Instrumentos de Cuerda")
        root.geometry("600x650")
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        ttk.Label(root, text="Sistema Experto de Instrumentos", font=("Arial", 18, "bold")).pack(pady=10)

        marco = ttk.Frame(root)
        marco.pack(pady=10)

        # ----- Combobox de características -----
        ttk.Label(marco, text="Cantidad de cuerdas:").grid(row=0, column=0, sticky="w")
        self.cb_cuerdas = ttk.Combobox(marco, values=["4", "5", "6", "8", "10", "muchas"])
        self.cb_cuerdas.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(marco, text="Tipo de ejecución:").grid(row=1, column=0, sticky="w")
        self.cb_tipo = ttk.Combobox(marco, values=["pulsada", "frotada", "percutida"])
        self.cb_tipo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(marco, text="Tipo de caja:").grid(row=2, column=0, sticky="w")
        self.cb_caja = ttk.Combobox(marco, values=["hueca", "sólida", "plana"])
        self.cb_caja.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(marco, text="Observación:").grid(row=3, column=0, sticky="w")
        self.cb_obs = ttk.Combobox(
            marco,
            values=[
                "cuerdas de nylon", "cuerdas metálicas", "usa amplificador", "folklórico",
                "orquestal", "parche resonante", "armónico"
            ]
        )
        self.cb_obs.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(root, text="Buscar instrumento", command=self.buscar).pack(pady=15)

        self.resultado = ttk.Label(root, font=("Arial", 14))
        self.resultado.pack(pady=5)

        self.lista = ttk.Label(root, font=("Arial", 10), justify="left")
        self.lista.pack(pady=5)

        # contenedor para imagen + mensaje
        self.imagen_label = ttk.Label(root)
        self.imagen_label.pack(pady=10)

        # REFERENCIA para evitar que Tk libere la imagen
        self.img_tk = None

    def buscar(self):
        cuerdas = self.cb_cuerdas.get().strip()
        tipo = self.cb_tipo.get().strip()
        caja = self.cb_caja.get().strip()
        obs = self.cb_obs.get().strip()

        if not all([cuerdas, tipo, caja, obs]):
            messagebox.showwarning("Faltan datos", "Selecciona todas las características.")
            return

        # --- Convertir a formato de la base de conocimiento ---
        cuerdas_fmt = f"cuerdas{cuerdas}" if cuerdas.isdigit() else "muchas_cuerdas"
        caja_fmt = "caja_" + caja.replace("ó", "o").replace("í", "i")
        obs_fmt = obs.replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

        caracteristicas = [cuerdas_fmt, tipo, caja_fmt, obs_fmt]


        posibles = base.buscar_instrumento(caracteristicas)

        if posibles is None:
            self.resultado.config(text="No se encontró ningún instrumento relacionado.")
            self.lista.config(text="")
            self.imagen_label.config(image="", text="")
            return

        # Tomar el más probable
        mejor = posibles[0][0]           # ejemplo: "guitarra_clasica"
        nombre_bonito = mejor.replace("_", " ")

        self.resultado.config(text=f"Instrumento más probable: {nombre_bonito}")

        texto = "\n".join([
            f"{n.replace('_',' ')} → {c} coincidencias"
            for n, c in posibles
        ])
        self.lista.config(text=texto)

        # -----------------------------
        # Buscar URL de imagen con normalización
        # -----------------------------
        clave_normalizada = normalize_key(mejor)                 # normaliza "guitarra_clasica"
        url = IMAGENES_NORMALIZADAS.get(clave_normalizada)

        # fallback: intentar con la versión "bonita" (sin guion bajo)
        if url is None:
            clave_bonita = normalize_key(nombre_bonito)
            url = IMAGENES_NORMALIZADAS.get(clave_bonita)

        # Si aún no hay URL, intentar mapear variantes comunes (sin acentos, sin 'a'/'á', etc.)
        if url is None:
            # intenta buscar cualquier clave que contenga la palabra base (e.g. 'guitarra')
            for k, v in IMAGENES_NORMALIZADAS.items():
                if normalize_key(" ".join(nombre_bonito.split()[:1])) in k:
                    url = v
                    break

        if url is None:
            # no se encontró URL: mostrar mensaje y salir
            self.imagen_label.config(text="Sin imagen disponible para este instrumento.", image="")
            return

        # -----------------------------
        # Descargar y mostrar imagen
        # -----------------------------
        img = descargar_imagen_url(url)
        if img is None:
            self.imagen_label.config(text="No se pudo descargar la imagen.", image="")
            return

        # Redimensionar manteniendo proporción, máximo 320x320
        max_size = (320, 320)
        img.thumbnail(max_size, Image.LANCZOS)

        self.img_tk = ImageTk.PhotoImage(img)
        self.imagen_label.config(image=self.img_tk, text="")

# -----------------------------
# EJECUTABLE
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    Interfaz(root)
    root.mainloop()