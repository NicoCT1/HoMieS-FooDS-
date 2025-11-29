# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 18:28:18 2025

@author: corte
"""

# -*- coding: utf-8 -*-
"""
Versión orientada a objetos del proyecto original.
Cada celda (#%%) fue convertida en una clase con sus métodos correspondientes.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import sqlite3 as sql
import shutil

# %%
# === CLASE 1: VISUALIZADOR DE IMÁGENES === #
class VisualizadorImagenes:
    def __init__(self, ruta_base):
        self.ruta_base = ruta_base

    def mostrar_imagenes(self):
        for carpeta in os.listdir(self.ruta_base):
            ruta_carpeta = os.path.join(self.ruta_base, carpeta)
            if os.path.isdir(ruta_carpeta):
                print(f"\nMostrando imágenes de la carpeta: {carpeta}\n")
                for nombre_imagen in os.listdir(ruta_carpeta):
                    ruta_imagen = os.path.join(ruta_carpeta, nombre_imagen)
                    if os.path.isfile(ruta_imagen) and nombre_imagen.lower().endswith(('.png', '.jpg', '.jpeg')):
                        try:
                            imagen = Image.open(ruta_imagen).convert('L')
                            imagen.save(ruta_imagen)
                            imagen = imagen.resize((80, 80))
                            plt.imshow(imagen, cmap='gray')
                            plt.axis("off")
                            plt.show()
                        except Exception as error:
                            print(f"No se pudo abrir {nombre_imagen}: {error}")

#%%
# === CLASE 2: PROCESADOR DE IMÁGENES === #
class ProcesadorImagenes:
    def __init__(self, ruta_base):
        self.ruta_base = ruta_base
        self.vectores_planos = []

    def procesar(self):
        for carpeta in os.listdir(self.ruta_base):
            ruta_carpeta = os.path.join(self.ruta_base, carpeta)
            if os.path.isdir(ruta_carpeta):
                for nombre_imagen in os.listdir(ruta_carpeta):
                    ruta_imagen = os.path.join(ruta_carpeta, nombre_imagen)
                    if nombre_imagen.lower().endswith(('.jpg', '.jpeg', '.png')):
                        try:
                            imagen = Image.open(ruta_imagen).convert('L').resize((80, 80))
                            matriz = np.array(imagen)
                            print(f"\nMatriz de la imagen {nombre_imagen} ({carpeta}):")
                            print(matriz)

                            vector = matriz.flatten()
                            print(f"\nVector plano de la imagen {nombre_imagen}:")
                            print(vector)

                            self.vectores_planos.append(vector)
                        except Exception as e:
                            print(f"No se pudo procesar {nombre_imagen}: {e}")

        if len(self.vectores_planos) > 0:
            matriz_final = np.vstack(self.vectores_planos)
            print("\n=== MATRIZ FINAL CON TODOS LOS VECTORES ===")
            print(matriz_final)
        else:
            print("\nNo se generaron vectores (verifica que haya imágenes).")

#%%
# === CLASE 3: BASE DE DATOS === #
class BaseDeDatos:
    def __init__(self, nombre_db="Recomiendalimentos.db"):
        self.nombre_db = nombre_db
        self.con = sql.connect(self.nombre_db)
        self.con.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.con.cursor()

    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS alimentos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ubicacion TEXT NOT NULL,
            sub_ubicacion TEXT NOT NULL,
            alimento TEXT NOT NULL
        );
        """)
        self.con.commit()

    def guardar_datos(self, df):
        try:
            df.to_sql('alimentos', con=self.con, if_exists='replace', index=False)
            self.con.commit()
            print("\nDatos guardados correctamente en la base de datos.")
        except Exception as e:
            print(f"\nError al guardar en la base de datos: {e}")

    def cerrar(self):
        self.con.close()


#%%
# === CLASE 4: GENERADOR DE DATAFRAME === #
class GeneradorDatos:
    def __init__(self, ruta_base):
        self.ruta_base = ruta_base

    def generar_dataframe(self):
        datos = []
        for subcarpeta in os.listdir(self.ruta_base):
            ruta_sub = os.path.join(self.ruta_base, subcarpeta)
            if os.path.isdir(ruta_sub):
                for archivo in os.listdir(ruta_sub):
                    if archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                        datos.append({
                            'ubicacion': os.path.basename(self.ruta_base),
                            'sub_ubicacion': subcarpeta,
                            'alimento': archivo
                        })

        df = pd.DataFrame(datos)
        print("\n=== BASE DE DATOS GENERADA CON TODAS LAS IMÁGENES ===")
        print(df)
        return df


#%%
# === CLASE 5: CLASIFICADOR DE IMÁGENES === #
class ClasificadorImagenes:
    def __init__(self, ruta_base, img_size=(70, 70)):
        self.ruta_base = ruta_base
        self.img_size = img_size
        self.modelo = None

    def entrenar(self):
        X, y = [], []
        for subcarpeta in os.listdir(self.ruta_base):
            ruta_sub = os.path.join(self.ruta_base, subcarpeta)
            if os.path.isdir(ruta_sub) and subcarpeta != "nue_alim":
                for archivo in os.listdir(ruta_sub):
                    if archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                        ruta_img = os.path.join(ruta_sub, archivo)
                        try:
                            img = Image.open(ruta_img).convert('L').resize(self.img_size)
                            X.append(np.array(img).flatten())
                            y.append(subcarpeta)
                        except Exception as e:
                            print(f"Error con {archivo}: {e}")
        self.modelo = {"imagenes": np.array(X), "etiquetas": np.array(y)}
        print(f"Imágenes cargadas: {len(X)}")
        print(f"Clases detectadas: {set(y)}")

    def clasificar(self, ruta_img):
        try:
            img = Image.open(ruta_img).convert('L').resize(self.img_size)
            vec = np.array(img).flatten()
        except:
            print(f"No se pudo abrir la imagen: {ruta_img}")
            return None

        distancias = np.linalg.norm(self.modelo["imagenes"] - vec, axis=1)
        indice_min = np.argmin(distancias)
        return self.modelo["etiquetas"][indice_min]

    def mover_nuevas(self):
        ruta_nuevos = os.path.join(self.ruta_base, "nue_alim")
        if not os.path.exists(ruta_nuevos):
            print("No existe la carpeta 'nue_alim'")
            return

        for archivo in os.listdir(ruta_nuevos):
            if archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                ruta_img = os.path.join(ruta_nuevos, archivo)
                clase = self.clasificar(ruta_img)
                if clase:
                    destino = os.path.join(self.ruta_base, clase, archivo)
                    try:
                        shutil.move(ruta_img, destino)
                        print(f"{archivo} movida a carpeta '{clase}'")
                    except Exception as e:
                        print(f"Error al mover {archivo}: {e}")
        print("\nClasificación y movimiento completados.")


#%%
# === PROGRAMA PRINCIPAL === #
if __name__ == "__main__":
    ruta = "PROYECTON"

    
    visualizador = VisualizadorImagenes(ruta)
    visualizador.mostrar_imagenes()

    
    procesador = ProcesadorImagenes(ruta)
    procesador.procesar()

    
    generador = GeneradorDatos(ruta)
    df = generador.generar_dataframe()

    
    db = BaseDeDatos()
    db.crear_tabla()
    db.guardar_datos(df)
    db.cerrar()

    
    clasificador = ClasificadorImagenes(ruta)
    clasificador.entrenar()
    clasificador.mover_nuevas()
