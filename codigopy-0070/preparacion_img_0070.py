
# ============================================================
# Axel Guzman NC 0070
# UIII Act6 Preparacion y evaluacion de imagenes
# Categorias: Pintor y Escultor
# ============================================================

import cv2
import numpy as np
import os
import csv

# 1. CONFIGURACION INICIAL

# Obtener la ubicacion principal del proyecto
carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)

# Rutas de las carpetas
carpeta_original = os.path.join(
    carpeta_proyecto, "img-original-0070"
)

carpeta_preparadas = os.path.join(
    carpeta_proyecto, "img-preparadas-0070"
)

carpeta_resultados = os.path.join(
    carpeta_proyecto, "resultados-img-0070"
)

# Dimensiones de las imagenes
ANCHO_DESTINO = 224
ALTO_DESTINO = 224

# Categorias asignadas
categorias = ["pintor", "escultor"]

# Crear carpetas de salida
os.makedirs(carpeta_preparadas, exist_ok=True)
os.makedirs(carpeta_resultados, exist_ok=True)

for categoria in categorias:
    os.makedirs(
        os.path.join(carpeta_preparadas, categoria),
        exist_ok=True
    )

# Variables para resultados
reporte = []
imagenes_procesadas = 0
imagenes_aprobadas = 0
imagenes_error = 0

print("=" * 55)
print("PREPARACION Y EVALUACION DE IMAGENES")
print("Axel Guzman NC 0070")
print("=" * 55)

# 2. RECORRER LAS CARPETAS DE CATEGORIAS

for categoria in categorias:

    ruta_origen = os.path.join(
        carpeta_original, categoria
    )

    ruta_destino = os.path.join(
        carpeta_preparadas, categoria
    )

    print("\n" + "=" * 45)
    print("CATEGORIA:", categoria.upper())
    print("=" * 45)

    # Verificar que exista la carpeta
    if not os.path.exists(ruta_origen):
        print("ERROR: No existe la carpeta:", ruta_origen)
        continue

    # 3. LEER LOS ARCHIVOS DE CADA CARPETA

    for nombre_archivo in os.listdir(ruta_origen):

        # Identificar formatos de imagen
        if not nombre_archivo.lower().endswith(
            (".jpg", ".jpeg", ".png", ".bmp")
        ):
            continue

        ruta_imagen = os.path.join(
            ruta_origen, nombre_archivo
        )

        print("\nProcesando:", nombre_archivo)

        # 4. LEER LA IMAGEN

        imagen = cv2.imread(ruta_imagen)

        if imagen is None:

            print("ERROR: No se pudo leer la imagen")

            imagenes_error += 1

            reporte.append([
                categoria,
                nombre_archivo,
                "ERROR",
                "-", "-", "-", "-", "-", "-", "REVISAR"
            ])

            continue

        imagenes_procesadas += 1

        # 5. IDENTIFICAR DIMENSIONES ORIGINALES

        alto_orig, ancho_orig, canales = imagen.shape

        print("Ancho original:", ancho_orig)
        print("Alto original:", alto_orig)
        print("Canales de color:", canales)

        # 6. REDIMENSIONAR LA IMAGEN

        imagen_redimensionada = cv2.resize(
            imagen,
            (ANCHO_DESTINO, ALTO_DESTINO),
            interpolation=cv2.INTER_AREA
        )

        print("Ancho preparado:", ANCHO_DESTINO)
        print("Alto preparado:", ALTO_DESTINO)

        # 7. CONVERTIR Y GUARDAR EN FORMATO JPG

        nombre_sin_ext = os.path.splitext(
            nombre_archivo
        )[0]

        ruta_jpg = os.path.join(
            ruta_destino,
            nombre_sin_ext + ".jpg"
        )

        guardado_jpg = cv2.imwrite(
            ruta_jpg,
            imagen_redimensionada
        )

        # 8. NORMALIZAR LOS VALORES DE LOS PIXELES

        imagen_normalizada = (
            imagen_redimensionada.astype(np.float32) / 255.0
        )

        val_min = float(np.min(imagen_normalizada))
        val_max = float(np.max(imagen_normalizada))

        print("Valor minimo:", round(val_min, 3))
        print("Valor maximo:", round(val_max, 3))

        # 9. GUARDAR LOS DATOS NORMALIZADOS

        ruta_npy = os.path.join(
            ruta_destino,
            nombre_sin_ext + ".npy"
        )

        np.save(ruta_npy, imagen_normalizada)

        # 10. EVALUAR LA IMAGEN

        dimensiones_correctas = (
            imagen_redimensionada.shape[0] == ALTO_DESTINO
            and imagen_redimensionada.shape[1] == ANCHO_DESTINO
        )

        rango_correcto = (
            val_min >= 0.0 and val_max <= 1.0
        )

        archivos_guardados = (
            guardado_jpg and os.path.isfile(ruta_npy)
        )

        if (
            dimensiones_correctas
            and rango_correcto
            and archivos_guardados
        ):

            estado = "APROBADA"
            imagenes_aprobadas += 1
            print("Evaluacion: APROBADA")

        else:
            estado = "REVISAR"
            print("Evaluacion: REVISAR")
        # 11. AGREGAR RESULTADOS AL REPORTE
        reporte.append([
            categoria,
            nombre_archivo,
            "OK",
            ancho_orig,
            alto_orig,
            ANCHO_DESTINO,
            ALTO_DESTINO,
            round(val_min, 3),
            round(val_max, 3),
            estado
        ])
# 12. CREAR EL REPORTE CSV

ruta_reporte = os.path.join(
    carpeta_resultados,
    "reporte_preparacion.csv"
)

with open(
    ruta_reporte,
    "w",
    newline="",
    encoding="utf-8"
) as archivo:

    escritor = csv.writer(archivo)

    escritor.writerow([
        "Categoria",
        "Archivo original",
        "Lectura",
        "Ancho original",
        "Alto original",
        "Ancho preparado",
        "Alto preparado",
        "Valor minimo normalizado",
        "Valor maximo normalizado",
        "Evaluacion"
    ])

    escritor.writerows(reporte)

# 13. RESUMEN FINAL

imagenes_por_revisar = (
    imagenes_procesadas - imagenes_aprobadas
)

print("\n" + "=" * 55)
print("RESUMEN DE LA PRACTICA")
print("=" * 55)

print("Alumno: Axel Guzman")
print("NC: 0070")
print("Categorias: Pintor y Escultor")

print("Imagenes procesadas:", imagenes_procesadas)
print("Imagenes aprobadas:", imagenes_aprobadas)
print("Imagenes con error:", imagenes_error)
print("Imagenes por revisar:", imagenes_por_revisar)

print("\nReporte guardado en:")
print(ruta_reporte)

print("\nPRACTICA TERMINADA")
print("Axel Guzman NC 0070")
