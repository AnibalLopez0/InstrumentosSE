# interfaz.py
import base
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk




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


class Interfaz:
    def __init__(self, root):
        self.root = root
        root.title("Sistema Experto – Instrumentos de Cuerda")

        # Entrada
        tk.Label(root, text="Características (separadas por comas):").pack()
        self.entry = tk.Entry(root, width=60)
        self.entry.pack(pady=5)

        tk.Button(root, text="Buscar instrumento", command=self.buscar).pack(pady=10)

        # Resultados
        self.resultado = tk.Label(root, font=("Arial", 13))
        self.resultado.pack(pady=10)

        # Lista de coincidencias
        self.lista = tk.Label(root, font=("Arial", 10))
        self.lista.pack(pady=5)

        # Imagen
        self.imagen_label = tk.Label(root)
        self.imagen_label.pack()

    def buscar(self):
        texto = self.entry.get().strip().lower()
        if not texto:
            messagebox.showwarning("Error", "Ingresa al menos una característica")
            return

        caracteristicas = [c.strip() for c in texto.split(",")]

        posibles = base.buscar_instrumento(caracteristicas)
        if posibles is None:
            self.resultado.config(text="No se encontró ningún instrumento.")
            self.lista.config(text="")
            self.imagen_label.config(image="")
            return

        # Más probable
        mejor = posibles[0][0]
        self.resultado.config(text=f"Instrumento más probable: {mejor}")

        # Lista de coincidencias
        texto_lista = "\n".join([f"{n} → {c} coincidencias" for n, c in posibles])
        self.lista.config(text=texto_lista)

        # Mostrar imagen
        url = IMAGENES.get(mejor)
        if url:
            img = base.obtener_imagen(url)
            if img:
                img = img.resize((250, 250))
                self.img_tk = ImageTk.PhotoImage(img)
                self.imagen_label.config(image=self.img_tk)
            else:
                self.imagen_label.config(text="No se pudo cargar la imagen.")
        else:
            self.imagen_label.config(text="Sin imagen disponible.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
