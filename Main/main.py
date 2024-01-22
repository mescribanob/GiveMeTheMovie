import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

#recoger el archivo de peliculas
movies = pd.read_csv('C:/Users/migue.DESKTOP-NTK1ITH/Desktop/ml-25m/movies.csv')
print(movies)

#limpiar el titulo de la pelicula
def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

#creacion de una nueva columna
movies["clean_title"] = movies["title"].apply(clean_title)

#Comandos para facilitar la busqueda de la pelicula
vectorizer = TfidfVectorizer(ngram_range=(1,2))
tfidf = vectorizer.fit_transform(movies["clean_title"])

#Creamos la funcion de busqueda
#Esto lo que nos permite es que el usuario no le va hacer falta escribir todo el titulo de la pelicula sino que con que escriba algo parecido al titulo la funcion devuelve las peliculas mas parecidas
def search(title):
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    result = movies.iloc[indices][::-1]
    return result
