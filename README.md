## HoMieS FooDS-

- Nicolás Cortés

## Descripción del Problema
El proyecto busca desarrollar un sistema de reconocimiento automático de imágenes basado en la técnica de **Eigen-objetos**, mediante descomposición en valores singulares (SVD). El problema que resolvemos es: *¿cómo representar un conjunto de imágenes de forma eficiente y clasificar nuevas imágenes basadas en sus rasgos principales?*

---

## 📂 Estructura del Proyecto

```
recomienda_alimentos/
│
├── data/
│   ├── fruver/               # Carpeta con imágenes de frutas y verduras
│   ├── mercado/              # Carpeta con imágenes de productos de mercado
│   └── nue_alim/             # Carpeta con nuevas imágenes a clasificar
│
├── src/
│   ├── visualizador.py       # Clase para visualizar imágenes en escala de grises
│   ├── procesador.py         # Clase para convertir imágenes en matrices y vectores planos
│   ├── generador_datos.py    # Clase para generar un DataFrame con nombres y ubicaciones
│   ├── base_datos.py         # Clase para crear y guardar datos en SQLite
│   ├── clasificador.py       # Clase que entrena y clasifica nuevas imágenes según similitud
│   └── main.py               # Script principal que ejecuta todo el flujo del proyecto
│
├── outputs/
│   ├── Recomiendalimentos.db # Base de datos SQLite generada automáticamente
│   ├── matriz_vectores.npy   # Matriz final con los vectores de todas las imágenes
│   ├── registro_datos.csv    # Copia en CSV de la base de datos (opcional)
│   └── logs.txt              # Archivo de registro con errores o movimientos realizados
│
├── requirements.txt          # Librerías necesarias para ejecutar el proyecto
└── README.md                 # Documentación completa del proyecto
```

---

## Objetivo del Proyecto

Este proyecto permite clasificar automáticamente imágenes de alimentos según su categoría (por ejemplo, frutas o productos de mercado).
Además, convierte las imágenes en matrices numéricas, genera una base de datos SQLite con su información y mueve automáticamente las nuevas imágenes a su carpeta correspondiente tras clasificarlas para luego hacer el filtrado de información y poder recomendar un alimento.

---

## Metodología: Eigen-Objetos con SVD
El enfoque consiste en:
1. Preprocesar las imágenes (escalas de grises, redimensionado uniforme, vectorización).
2. Apilar los vectores de todas las imágenes en una matriz \(X\) de dimensión \(n\_pixeles \times n\_imágenes\).
3. Aplicar la descomposición
   \[
     X = U \,\Sigma\, V^T
   \]
   para extraer los autovectores (columnas de \(U\)) que corresponden a los “Eigen-objetos”.
4. Seleccionar los \(k\) vectores singulares más relevantes.
5. Clasificar imágenes nuevas comparando errores de reconstrucción o distancias en ese espacio reducido.
   
---

El proyecto fue desarrollado y probado en:
```bash
Python 3.12.11 (Spyder IDE)
```
### Requerimientos del Sistema:
```bash
| Librería     | Versión recomendada   | Descripción                                       |
| ------------ | --------------------- | ------------------------------------------------- |
| `numpy`      | ≥ 1.26                | Manipulación de matrices y operaciones numéricas. |
| `pandas`     | ≥ 2.2                 | Creación y manejo de DataFrames.                  |
| `matplotlib` | ≥ 3.9                 | Visualización de imágenes y gráficos.             |
| `Pillow`     | ≥ 10.4                | Procesamiento de imágenes (PIL).                  |
| `sqlite3`    | (incluido con Python) | Gestión de base de datos local.                   |
| `shutil`     | (incluido con Python) | Mover y copiar archivos del sistema.              |
| `os`         | (incluido con Python) | Manejo de directorios y rutas.                    |

```
### Instalación Automática
Puedes instalar todas las dependencias ejecutando el siguiente comando en la terminal o consola de Spyder:
```bash

pip install -r requirements.txt

```
### 🚨🚨
Asegurate que el archivo "requirements.txt" contenga lo siguiente:
```bash

numpy>=1.26
pandas>=2.2
matplotlib>=3.9
Pillow>=10.4

```
##  Configuración del Entorno en Spyder

1. Abre Spyder.

2. Ve a:
Herramientas → Preferencias → Entorno de Python → Usar entorno existente (Anaconda o venv).

3. Asegúrate de que apunte a tu instalación de Python 3.12.11.
4.En la consola IPython, ejecuta:
```bash

import numpy, pandas, matplotlib, PIL
print("Entorno configurado correctamente ✅")

```
Si no aparece ningún error, el entorno está listo para usar.

---

## Estructura del Repositorio
- `data/`: Contiene las imágenes de cada clase, organizadas en carpetas por categoría.
- `src/`:
  - `image_processor.py`: Módulo que realiza la extracción-transformación-carga (ETL) de las imágenes.
  - `custom_svd.py`: Módulo que ejecuta la descomposición SVD personalizada.
  - `svd_classifier.py`: Módulo que implementa el clasificador basado en SVD.
- `outputs/`: Carpeta donde se almacenan los artefactos generados (matrices `.npy`, base de datos `.db`, vectores medios, etc.).
- `requirements.txt`: Lista de librerías necesarias.
- `README.md`: Este archivo de documentación.

---

## Instrucciones de Uso

## 1. Procesamiento y carga inicial
   
Ejecuta el script principal del módulo main.py para iniciar el flujo completo de procesamiento, análisis y clasificación de imágenes:
```bash
python src/main.py
```

Esto realizará las siguientes acciones:

Visualizará las imágenes de cada carpeta (fruver, mercado, nue_alim) en escala de grises.

Convertirá cada imagen en una matriz y vector numérico.

Generará un DataFrame con la información de todas las imágenes.

Creará o actualizará la base de datos Recomiendalimentos.db en la carpeta outputs/.

Clasificará las nuevas imágenes (de nue_alim/) y las moverá a su carpeta correspondiente.


## 2.  Ejecución por módulos individuales
Si prefieres ejecutar cada parte del sistema por separado, puedes hacerlo directamente desde Spyder o consola:

**Visualización de imágenes**

Muestra todas las imágenes en escala de grises:
```bash
python src/visualizador.py
```
**Procesamiento de imágenes**

Convierte las imágenes a matrices y vectores numéricos:
```bash

python src/procesador.py
```
**Generación de la base de datos**

Crea el DataFrame y guarda los datos en SQLite:
```bash
python src/base_datos.py
```
**Clasificación automática**

Clasifica las nuevas imágenes de la carpeta nue_alim/ y las mueve a su clase correspondiente:
```bash
python src/clasificador.py
```
## 3. Resultados generados

Tras la ejecución del flujo completo, se generarán o actualizarán los siguientes archivos:

Archivo / Carpeta	Descripción
outputs/Recomiendalimentos.db	Base de datos con las rutas e identificaciones de alimentos.
outputs/matriz_vectores.npy	Matriz con los vectores planos de todas las imágenes procesadas.
data/fruver/ y data/mercado/	Carpetas finales con las imágenes correctamente clasificadas.
data/nue_alim/	Carpeta que quedará vacía una vez las imágenes sean reubicadas.

## 4. Verificación de resultados en Spyder

Después de ejecutar el script principal, puedes abrir la consola IPython y ejecutar:

import pandas as pd
import sqlite3 as sql

con = sql.connect("outputs/Recomiendalimentos.db")
df = pd.read_sql("SELECT * FROM alimentos", con)
print(df.head())
con.close()


Esto mostrará una vista previa de los datos almacenados en la base de datos, confirmando que el procesamiento se realizó correctamente ✅

