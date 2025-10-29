# HoMieS-FooDS-

- Nicolás Cortés

## Descripción del Problema
El proyecto busca desarrollar un sistema de reconocimiento automático de imágenes basado en la técnica de **Eigen-objetos**, mediante descomposición en valores singulares (SVD). El problema que resolvemos es: *¿cómo representar un conjunto de imágenes de forma eficiente y clasificar nuevas imágenes basadas en sus rasgos principales?*

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

## Estructura del Repositorio
- `data/`: Contiene las imágenes de cada clase, organizadas en carpetas por categoría.
- `src/`:
  - `image_processor.py`: Módulo que realiza la extracción-transformación-carga (ETL) de las imágenes.
  - `custom_svd.py`: Módulo que ejecuta la descomposición SVD personalizada.
  - `svd_classifier.py`: Módulo que implementa el clasificador basado en SVD.
- `outputs/`: Carpeta donde se almacenan los artefactos generados (matrices `.npy`, base de datos `.db`, vectores medios, etc.).
- `requirements.txt`: Lista de librerías necesarias.
- `README.md`: Este archivo de documentación.

## Instrucciones de Uso

