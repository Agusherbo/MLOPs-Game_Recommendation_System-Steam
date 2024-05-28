<h1 align="center"> MLOPs-Game Recommendation System / Steam </h1>



## Introducción

En este proyecto, se desarrollará el rol de un Ingeniero MLOps en Steam (plataforma de juegos). El objetivo principal es crear un sistema de recomendación de videojuegos utilizando técnicas de Machine Learning. Los datos necesitan un respectivo tratamiento (ETL, EDA), y la tarea es transformarlos para disponer de ellos y desarrollar un Producto Mínimo Viable (MVP) que luego sea desplegado como una API.

## Descripción del Problema

Es necesario crear un modelo de aprendizaje automático para un sistema de recomendación de videojuegos. El estado actual de los datos es crudo y no procesado. Nuestro objetivo es empezar desde cero, realizar tareas de procesamiento de Datos y entregar un MVP al final del proyecto.


## Información dataset

Se trabajó con tres archivos JSON que contienen datos acerca de los juegos en la plataforma Steam:

- `steam_games.json.gz`

  Este conjunto de datos proporciona las características principales de cada juego, como títulos, desarrolladores, precios, géneros y etiquetas.

- `users_reviews.json.gz`
  
  Este conjunto de datos presenta opiniones de usuarios sobre los juegos que consumieron.
  
- `users_items.json.gz`
  
  Contiene información de los juegos consumidos y el tiempo jugado a lo largo del tiempo.

Fuente de datos: [Dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj)  

Los archivos json.gz fueron descomprimidos de manera local a .json y utilizados en este formato al iniciar el trabajo. 

## Desarrollo del proyecto 

## Limpieza y Transformación de Datos (ETL)

- Leer el conjunto de datos en el formato correcto.
- Desanidado de columnas anidadas, es decir, tienen un diccionario o una lista como valores en cada fila.
- Eliminar columnas innecesarias
- Eliminacion de valores nulos
- Eliminacion de datos sin valor
- Cambio de tipo de dato. (ej: fecha a datetime)
- Combinacion de datasets para optimizar futuras consultas 

Todas estas tareas se realizan con el fin de optimizar la estructura y tamaño de los datos para el obtener el mejor rendimiento de la API
[ETL](https://github.com/Agusherbo/MLOPs-Game_Recommendation_System-Steam/tree/main/ETL)

## Análisis Exploratorio de Datos (EDA)

Se realiza un EDA de forma manual para investigar las relaciones entre variables, identificar valores atípicos y descubrir patrones interesantes dentro del conjunto de datos, para esta tarea se utilizan diferentes librerías para hacer visualizaciones y medidas estadísticas. [EDA](https://github.com/Agusherbo/MLOPs-Game_Recommendation_System-Steam/blob/main/EDA/EDA.ipynb)

## Feature Engineering

Se crearon DataFrames auxiliares con el fin de optimizar el espacio y mejorar el rendimiento de las funciones. Estos DataFrames se utilizaron para almacenar datos específicos necesarios para las consultas de la API. Los datasets creados se encuentran aqui: [data_clean](https://github.com/Agusherbo/MLOPs-Game_Recommendation_System-Steam/tree/main/data_clean)

`Análisis de Sentimiento:` Crear una nueva columna, 'sentiment_analysis', aplicando análisis de sentimiento mediante Procesamiento de Lenguaje Natural (NLP) a las reseñas de usuarios. La escala que se utilizo fue: '0' para comentarios negativos, '1' para neutrales y '2' para positivos.

## Desarrollo de la API

**Framework:** Utilizar el framework FastAPI para exponer los datos de la empresa a través de endpoints RESTful.

**Endpoints (funciones objetivo):**

- `developer(desarrollador : str)`: Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.

- `userData(user_id : str)`: Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.

- `userForGenre(genero : str)`: Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

- `best_developer_year(año : int)`: Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)

- `developer_reviews_analysis(desarrollador : str)`: Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.

Enlace con las funciones desarrolladas: [Funciones_API](https://github.com/Agusherbo/MLOPs-Game_Recommendation_System-Steam/blob/main/Funciones_API.ipynb)

## Modelo de Recomendación

Se implementa un sistema de recomendación  item-item. En este caso el sistema de recomendación funciona tomando un item_id y encontrando cinco similares a este.
Nota: De manera similar a las funciones, en el modelo de recomendación, también se emplearon muestras reducidas de los dataframes originales. Esto se hizo para garantizar un rendimiento óptimo del modelo y evitar problemas de capacidad de procesamiento durante el despliegue (deploy) de la API en Render.
[Modelo](https://github.com/Agusherbo/MLOPs-Game_Recommendation_System-Steam/blob/main/Modelo_recommend.ipynb)

### Deploy en Render

Para el deploy de la API se seleccionó la plataforma Render que es una nube unificada para crear y ejecutar aplicaciones y sitios web, permitiendo el despliegue automático desde GitHub.
El servicio queda corriendo en [https://repo-deploy.onrender.com](https://api-render-r1zg.onrender.com/docs)

> [!NOTE]
> Para el despliegue automático, Render utiliza GitHub y dado que el servicio gratuito cuenta con una limitada capacidad de almacenamiento, se realizó un repositorio exclusivo para el deploy, el cual se encuentra [aquí](https://github.com/Agusherbo/API-Render)

## Video

En este [link] se encuentra el video donde se explica brevemente el desarrollo del proyecto y el correcto funcionamiento de la API desplegada en el servicio web de Render.

## Tecnologías Utilizadas

En el desarrollo de este proyecto, aprovechamos varias tecnologías para llevar a cabo las distintas etapas del proceso:

![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
![Seaborn](https://img.shields.io/badge/-Seaborn-333333?style=flat&logo=seaborn)
![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn)
![FastAPI](https://img.shields.io/badge/-FastAPI-333333?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/-Docker-333333?style=flat&logo=docker)
![Render](https://img.shields.io/badge/-Render-333333?style=flat&logo=render)








