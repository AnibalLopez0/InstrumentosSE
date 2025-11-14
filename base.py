# ----------------------------------------------
# SISTEMA EXPERTO EN PYTHON – Instrumentos de Cuerda
# ----------------------------------------------
import requests
from PIL import Image
from io import BytesIO

# Base de conocimiento: instrumentos y características
instrumentos = {
    # Cuerda pulsada
    "guitarra_clasica": ["cuerdas6", "pulsada", "caja_hueca", "cuerdas_nylon"],
    "guitarra_acustica": ["cuerdas6", "pulsada", "caja_hueca", "cuerdas_metal"],
    "guitarra_electrica": ["cuerdas6", "pulsada", "caja_solida", "cuerdas_metal", "usa_amplificador"],
    "bajo_electrico": ["cuerdas4", "pulsada", "caja_solida", "usa_amplificador"],
    "charango": ["cuerdas10", "pulsada", "caja_hueca", "folklore"],
    "bandurria": ["cuerdas12", "pulsada", "caja_hueca", "acero"],
    "mandolina": ["cuerdas8", "pulsada", "caja_hueca", "orquestal"],
    "ukelele": ["cuerdas4", "pulsada", "caja_hueca", "tradicional"],
    "laud": ["cuerdas12", "pulsada", "caja_hueca", "tradicional"],
    "banjo": ["cuerdas5", "pulsada", "caja_hueca", "parche_resonante"],
    "koto": ["cuerdas13", "pulsada", "caja_hueca", "tradicional_japones"],
    "sitar": ["cuerdas18", "pulsada", "caja_hueca", "tradicional_india"],
    "citara": ["cuerdas30", "pulsada", "caja_plana", "tradicional"],
    "arpa": ["muchas_cuerdas", "pulsada", "caja_hueca"],

    # Cuerda frotada
    "violin": ["cuerdas4", "frotada", "caja_hueca", "orquestal"],
    "viola": ["cuerdas4", "frotada", "caja_hueca", "tamaño_medio"],
    "violonchelo": ["cuerdas4", "frotada", "caja_hueca", "tamaño_grande"],
    "contrabajo": ["cuerdas4", "frotada", "caja_hueca", "muy_grave"],
    "erhu": ["cuerdas2", "frotada", "caja_hueca", "tradicional_china"],

    # Cuerda percutida
    "piano": ["muchas_cuerdas", "percutida", "caja_hueca", "armonico"]
}


# ----------------------------------------------
# Función para buscar instrumentos por coincidencias parciales
# ----------------------------------------------
def buscar_instrumento(caracteristicas):
    posibles = []

    for nombre, datos in instrumentos.items():
        # Cuántas características del usuario están dentro del instrumento
        coincidencias = sum(1 for c in caracteristicas if c in datos)

        if coincidencias > 1:
            posibles.append((nombre, coincidencias))

    # Si no hay ningún instrumento relacionado
    if not posibles:
        return None

    # Ordenar por número de coincidencias (de mayor a menor)
    posibles.sort(key=lambda x: x[1], reverse=True)

    return posibles


#obtener imagen
def obtener_imagen(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return Image.open(BytesIO(resp.content))
    except:
        return None
# ----------------------------------------------
# Proceso de preguntas con limpieza de texto
# ----------------------------------------------
def preguntar_caracteristicas():
    def limpiar(txt):
        return txt.strip().lower()

    print("\nIngresa 3 características del instrumento.")
    print("Ejemplos válidos: cuerdas6, pulsada, caja_hueca, frotada, usa_amplificador...\n")

    A = limpiar(input("1: "))
    B = limpiar(input("2: "))
    C = limpiar(input("3: "))

    extra = limpiar(input("¿Quieres agregar una característica más? (s/n): "))

    if extra == "s":
        D = limpiar(input("4: "))
        return [A, B, C, D]

    return [A, B, C]


# ----------------------------------------------
# Sistema experto – flujo principal
# ----------------------------------------------
def inicio():
    print("\n--- SISTEMA EXPERTO: INSTRUMENTOS DE CUERDA ---\n")

    caracteristicas = preguntar_caracteristicas()
    posibles = buscar_instrumento(caracteristicas)

    if posibles is None:
        print("\n No se encontró ningún instrumento relacionado.\n")
        return

    print("\n INSTRUMENTOS RELACIONADOS (ordenados por coincidencias):\n")

    for nombre, score in posibles:
        print(f"- {nombre}  →  coincidencias: {score}")

    print("\n El primero es el más probable.\n")


# ----------------------------------------------
# Ejecutar
# ----------------------------------------------
if __name__ == "__main__":
    inicio()
