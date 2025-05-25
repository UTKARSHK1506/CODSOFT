import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Dataset with titles and descriptions
data = {
    'title': [
        'The Matrix', 'Inception', 'The Notebook', 'Titanic', 'Avengers',
        'Oppenheimer', 'Interstellar', 'Avatar', 'The Dark Knight', 'Dune'
    ],
    'description': [
        "A hacker discovers reality is a simulation and joins a rebellion.",
        "A thief enters people's dreams to steal secrets, but struggles with his past.",
        "A woman falls in love with a poor artist in a story of passion and memory.",
        "A young couple from different social classes fall in love aboard the Titanic.",
        "Earth's mightiest heroes team up to stop an alien invasion.",
        "The story of J. Robert Oppenheimer and the development of the atomic bomb.",
        "A team travels through a wormhole in space to save humanity.",
        "A marine on an alien planet gets torn between duty and love for the native people.",
        "A vigilante fights crime in Gotham while facing his toughest moral tests.",
        "A gifted young man navigates political power struggles on a desert planet."
    ]
}

df = pd.DataFrame(data)

# Step 2: Vectorize descriptions using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['description'])

# Step 3: Compute cosine similarity between movies
similarity = cosine_similarity(tfidf_matrix)

# Step 4: Recommendation function
def recommend(movie_title, df, similarity):
    try:
        idx = df[df['title'].str.lower() == movie_title.lower()].index[0]
        scores = list(enumerate(similarity[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:4]  # Top 3 excluding itself
        top_movies = [df.iloc[i[0]]['title'] for i in scores]
        return top_movies
    except IndexError:
        return ["Movie not found in dataset."]

# Step 5: Test it
print("Recommendations for 'Inception':")
print(recommend('Inception', df, similarity))

print("\nRecommendations for 'Titanic':")
print(recommend('Titanic', df, similarity))

print("\nRecommendations for 'Dune':")
print(recommend('Dune', df, similarity))

print("\nRecommendations for 'Oppenheimer':")
print(recommend('Oppenheimer', df, similarity))
