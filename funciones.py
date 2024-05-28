## FUNCIONES A UTILIZAR EN app.py

# Importaciones
import pandas as pd
import operator

# Datos a usar

reviews = pd.read_parquet("data_clean/2-reviews.parquet")
items_spend = pd.read_parquet("data_clean/4-items_spend.parquet")
items_dev = pd.read_parquet("data_clean/7-items_dev.parquet")
usertime_year = pd.read_parquet("data_clean/8-usertime_year.parquet")
best_dev = pd.read_parquet("data_clean/9-best_dev.parquet")
similar_item = pd.read_parquet("data_clean/13-similar_item.parquet")


def developer(desarrollador:str):
    """
    Esta función devuelve la cantidad de items y el porcentaje de contenido gratuito por año para una empresa desarrolladora.

    Args:
        desarrollador (str): El nombre de la empresa desarrolladora.

    Returns:
        dict: Un diccionario con la cantidad de items y el porcentaje de contenido gratuito por año.
              Las claves son los años de lanzamiento y los valores son diccionarios con la siguiente estructura:
              {'cantidad_items': int, 'porcentaje_gratis': float}
    """
    # Filtrar el dataframe items_dev por la empresa desarrolladora especificada
    df_filtrado = items_dev[items_dev['developer'] == desarrollador]

    # Agrupar el dataframe filtrado por año de lanzamiento y calcular la cantidad de items y el conteo de contenido gratuito
    resultado = df_filtrado.groupby('release_year').agg(cantidad_items=('item_id', 'count'),
                                                        conteo_gratis=('price', lambda x: (x == 0.0).sum()))

    # Calcular el porcentaje de contenido gratuito por año
    resultado['porcentaje_gratis'] = (resultado['conteo_gratis'] / resultado['cantidad_items']) * 100

    return resultado.to_dict(orient='index')



def userData(user_id):
    """
    Esta función devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews_recommend y cantidad de items.

    Parámetros:
    - user_id (int): Identificador único del usuario de interés.

    Devuelve:
    dict:
        - 'usuario_': Identificador único del usuario.
        - 'cantidad_dinero': Suma total de dinero gastado por el usuario en items_spend.
        - 'porcentaje_recomendacion': Porcentaje de recomendaciones realizadas por el usuario en comparación
          con el total de revisiones en el conjunto de datos.
        - 'total_items': La cantidad máxima de items comprados por el usuario en items_spend.
    """
    # Filtrar datos del usuario en items_spend
    usuario_gastos = items_spend[items_spend["user_id"] == user_id]

    # Calcular la cantidad de dinero gastado y el total de items para el usuario de interés
    cantidad_dinero = usuario_gastos["price"].sum()
    total_items = usuario_gastos["items_count"].max()

    # Calcular el total de recomendaciones realizadas por el usuario de interés
    total_recomendaciones = reviews[reviews["user_id"] == user_id]["reviews_recommend"].sum()

    # Calcular el total de revisiones realizadas por todos los usuarios
    total_reviews = len(reviews["user_id"].unique())

    # Calcular el porcentaje de recomendaciones realizadas por el usuario de interés
    porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100

    # Retornar los resultados en un diccionario
    return {
        "usuario_": user_id,
        "cantidad_dinero": int(cantidad_dinero),
        "porcentaje_recomendacion": round(porcentaje_recomendaciones, 2),
        "total_items": int(total_items),
    }
    
    

def userForGenre(genero:str):
    """
    Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

    Parámetros:
    - genero (str): Género específico para el cual se desea obtener la información.
    
    Retorna:
    dict: Un diccionario con la siguiente estructura:
        {
            "Usuario con más horas jugadas para <genero>": <usuario>,
            "Horas jugadas": [
                {"Año": <año1>, "Horas": <horas1>},
                {"Año": <año2>, "Horas": <horas2>},
                ...
            ]
        }
    """
    # Filtrar el dataframe por el género dado
    usertime_year_filtrado = usertime_year[usertime_year['genres'] == genero]

    # Obtener el usuario con más horas jugadas para el género dado
    usuario_mas_jugado = usertime_year_filtrado.loc[usertime_year_filtrado['playtime_forever'].idxmax(), 'user_id']

    # Calcular la acumulación de horas jugadas por año de lanzamiento
    acumulacion_horas = usertime_year_filtrado.groupby('release_year')['playtime_forever'].sum().reset_index()
    acumulacion_horas = acumulacion_horas.rename(columns={'playtime_forever': 'Horas'})

    # Convertir el resultado a un diccionario
    resultado = {
        "Usuario con más horas jugadas para " + genero: usuario_mas_jugado,
        "Horas jugadas": acumulacion_horas.to_dict(orient='records')
    }

    return resultado



def best_developer_year(year):
    """
    Esta función devuelve el top 3 de desarrolladores con los juegos más recomendados y con un análisis de sentimiento igual a 2 para el año dado.

    Args:
        best_dev (pandas.DataFrame): El dataframe que contiene los datos.
        year (int): El año para el cual se desea obtener el top.

    Returns:
        list: Una lista con los nombres de los desarrolladores en el top 3.
    """
    # Filtrar el dataframe por el año y las condiciones de recomendación y análisis de sentimiento
    filtered_df = best_dev[(best_dev['release_year'] == year) & (best_dev['reviews_recommend'] == True) & (best_dev['sentiment_analysis'] == 2)]

    # Agrupar por desarrollador y contar el número de juegos recomendados
    developer_counts = filtered_df.groupby('developer').size().reset_index(name='count')

    # Ordenar en orden descendente y obtener los 3 primeros desarrolladores
    top_developers = developer_counts.nlargest(3, 'count')['developer'].tolist()
    
    #imprimir el resultado como un ranking del 1 al 3
    for i, developer in enumerate(top_developers):
        print(f'{i + 1}. {developer}')

    return top_developers


def developer_reviews_analysis(desarrollador):
    """
    Analiza las reseñas de usuarios para un desarrollador específico y devuelve un diccionario con la cantidad total
    de registros de reseñas categorizados con un análisis de sentimiento como positivo o negativo.

    Parámetros:
    - desarrollador (str): Nombre del desarrollador para el cual se desea realizar el análisis.

    Retorna:
    dict: Un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de
    reseñas categorizados con un análisis de sentimiento como valor positivo o negativo.
    """
    # Filtra el DataFrame por el desarrollador deseado
    df_desarrollador = best_dev[best_dev['developer'] == desarrollador]

    # Cuenta la cantidad total de registros de reseñas categorizados como positivos o negativos
    sentiment_counts = df_desarrollador['sentiment_analysis'].value_counts().to_dict()

    # Asegurar que ambos sentimientos (positivo y negativo) están en el diccionario, incluso si son 0
    result = {
        desarrollador: {
            'Negativas': sentiment_counts.get(0, 0), 
            'Positivas': sentiment_counts.get(2, 0)
        }
    }

    return result




def recomendacionJuego(item_id):
  '''
  Esta función muestra una lista de juegos similares a un item_id dado.

  Parameters:
  ----------
  item_id: El item_id para el cual se desean encontrar item_id similares.

  Returns:
  ----------
  id_similares: Esta función imprime una lista de juegos 5 similares al dado.

  Pasos:
  ----------
  
Verificamos si el juego está en el DataFrame de similitud
Obtenemos la lista de juegos similares y mostrarlos
Imprimimos la lista de juegos similares

  '''

  if item_id not in similar_item.index:
      print(f'No se encontraron juegos similares para {item_id}.')
      return

  similar_juegos = similar_item.sort_values(by=item_id, ascending=False).index[1:6]  # Mostrar siempre los primeros 5

  id_similares = [item for item in similar_juegos]

  return id_similares