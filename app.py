import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    )
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Recommendation function
def recommend(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movies and similarity data
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommender System')

# CSS for background image and layout
st.markdown("""
    <style>
    /* Apply the background to the main container */
    [data-testid="stAppViewContainer"] {
        background-image: url('https://wallpapercave.com/wp/wp12389675.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .poster-container {
        display: flex;
        justify-content: space-around; /* Distributes posters evenly */
        gap: 20px; /* Adds space between posters */
    }
    .poster {
        text-align: center;
        border: 2px solid ; /* Border around each poster */
        border-radius: 10px; /* Rounded corners */
        padding: 10px;
        background-color: rgba(255, 255, 255, 0.8); /* Light background */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Shadow effect */
    }
    .poster img {
        width: 150px;
        height: 225px;
        object-fit: cover; /* Ensures the image fits nicely */
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

selected_movies_name = st.selectbox('Select a movie', movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movies_name)
    st.markdown('<div class="poster-container">', unsafe_allow_html=True)
    
    for name, poster in zip(recommended_movie_names, recommended_movie_posters):
        st.markdown(
            f"""
            <div class="poster">
                <img src="{poster}" alt="{name}">
                <p>{name}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

