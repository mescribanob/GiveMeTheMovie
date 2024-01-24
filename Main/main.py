import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import tkinter as tk
from tkinter import Entry, Button , Text, Scrollbar

#recoger el archivo de peliculas
movies = pd.read_csv('C:/Users/migue.DESKTOP-NTK1ITH/Desktop/ml-25m/movies.csv')

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

#Para la busqueda de peliculas
#print(search("The Hulk"))

#leemos las recomendaciones de las peliculas
ratings = pd.read_csv('C:/Users/migue.DESKTOP-NTK1ITH/Desktop/ml-25m/ratings.csv')

#encontramos los usuarios que les gusta la misma pelicula
movie_id = 1
similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] >= 5)]["userId"].unique()

similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] >= 5)]["movieId"]

similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
similar_user_recs = similar_user_recs[similar_user_recs > .1]

#encontramos peliculas que esten relacionadas con la pelicula que hemos buscado
all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] >=5)]
all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
rec_percentages.columns = ["similar", "all"]
rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
rec_percentages = rec_percentages.sort_values("score", ascending=False)


#hacemos una funcion de recomendacion que junte lo anterior
def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] >= 5)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] >= 5)]["movieId"]

    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > .10]

    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] >=5)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())

    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(movies, left_index=True, right_on='movieId')[["title", "genres"]]

#Creamos una funcion donde el parametro de entrada sea el titulo
def GiveMeTheMovie(movieTitle):
    results = search(movieTitle)
    movie_id = results.iloc[0]["movieId"]
    return find_similar_movies(movie_id)

def ejecutar_funcion():
    # Obtener el valor del Entry
    parametro = entry_parametro.get()
    
    # Llamar a la función con el parámetro
    resultado = GiveMeTheMovie(parametro)

    # Mostrar el resultado en el Text widget
    resultado_text.delete("1.0", tk.END)  # Limpiar el contenido anterior
    resultado_text.insert(tk.END, resultado)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz con Parámetros")

# Crear un Entry para ingresar el parámetro
entry_parametro = Entry(ventana, width=20)
entry_parametro.pack(pady=10)

# Crear un botón para ejecutar la función
boton_ejecutar = Button(ventana, text="Ejecutar Función", command=ejecutar_funcion)
boton_ejecutar.pack(pady=10)

# Crear un Text widget para mostrar el resultado
resultado_text = Text(ventana, height=70, width=120)
resultado_text.pack(pady=10)

# Agregar una barra de desplazamiento al Text widget
scrollbar = Scrollbar(ventana, command=resultado_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
resultado_text.config(yscrollcommand=scrollbar.set)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()