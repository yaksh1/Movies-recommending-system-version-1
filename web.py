import streamlit as st
import pickle
import requests

movies_df = pickle.load(open('movies.pkl','rb'))
movies_list = movies_df['title'].values # names of all the movies

# similarity list of movies with other movies
similarity = pickle.load(open('similarity.pkl','rb'))


# -------------------------------
# poster function
# -------------------------------
def poster(movie_id):
  response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=12804ad378a8ba3bd3da09faac00798a&language=en-US'.format(movie_id))
  data = response.json()
  return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


# -------------------------------
# recommending function
# -------------------------------
def recom(movie):
  # movies index
  movies_index = movies_df[movies_df['title'] == movie].index[0]
  # top similar movies
  recommended_list = sorted(list(enumerate(similarity[movies_index])), reverse = True, key = lambda x: x[1])[0:6]
  
  recommended_movies = []
  movie_poster =[]
  
  for i in recommended_list:
    # movie id
    movie_id = movies_df.iloc[i[0]].id
    # fetch poster from API
    movie_poster.append(poster(movie_id))
    # appending recommendations
    recommended_movies.append(movies_list[i[0]])
  return recommended_movies,movie_poster
  
  
# title of the website 
st.title('Movie Recommendation System🍿')

# user input
movie_name = st.selectbox(
    'Search:',
    movies_list)

# enter button
if st.button('Enter'):
  names,posters = recom(movie_name)
  col1, col2, col3, col4, col5,col6 = st.columns(6)
  col_list = [col1,col2,col3,col4,col5,col6]
  
  for i in col_list:
    with i:
      st.image(posters[col_list.index(i)])
  # with col1:
  #   st.image(posters[0])


