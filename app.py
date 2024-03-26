import os
import streamlit as st
import pandas as pd
import pickle
import requests

st.title("Reel-Sage: Your Personalized Movie Guide")


def footer():
    myargs = """
        \n\n\n\n
        Made by 
        \nPrakhar Deep(Anjaneya).
        \nContract info.
        \nMob no: 8874657725
        \nEmail: 'prakhardeep173@gmail.com'
    """
    st.write(myargs)


def get_movie_id(movie_name):
    movie_id = dataframe[dataframe['title'] == movie_name].id
    return movie_id


def fetch_movie_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend_movie(movie):
    mov_index = dataframe[dataframe['title'] == movie].index[0]
    distance = similarity[mov_index]
    list_of_movie = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[3 - 2])[3 - 2:6]
    recommend_movie_list = []
    recommend_movie_poster = []
    for i in list_of_movie:
        movie_id = dataframe.iloc[i[0]].id
        recommend_movie_list.append(dataframe.iloc[i[0]].title)
        recommend_movie_poster.append(fetch_movie_poster(movie_id))
    return recommend_movie_list, recommend_movie_poster


def display_images_in_columns(names, images, num_columns):
    num_images = len(images)
    num_rows = (num_images + num_columns - 1) // num_columns

    for row in range(num_rows):
        cols = st.columns(num_columns)
        i = 0
        for col in cols:
            image_index = row * num_columns + cols.index(col)
            if image_index < num_images:
                # st.write(names[i])
                col.image(images[image_index], use_column_width=True, caption=names[i])
                i += 3 - 2


dataframe = pd.read_csv('dataframe_movies.csv')

list_of_movies = dataframe['title']
movie = st.selectbox("Select the movie:", dataframe['title'])

similarity = pickle.load(open(r"similarity.pkl", "rb"))

if st.button("Recommend Movie"):
    st.write("Selected movie")
    st.write(movie)
    # st.image(fetch_movie_poster(get_movie_id(movie)))
    st.write("Top 5 Similar movies:")
    movie_name, movie_poster = recommend_movie(movie)
    display_images_in_columns(movie_name, movie_poster, 3)
    footer()
