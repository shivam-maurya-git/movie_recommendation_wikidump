import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import pickle

# Loading FASIS Index
index = faiss.read_index("movies_vector_store.faiss")
print(index)

#Opening metadta file (dataframe of movies data)
with open("movies_metadata.pkl", "rb") as f:
    df = pickle.load(f)

# loading embedding model for encoding query vector
model = SentenceTransformer("all-MiniLM-L6-v2")

# Movie Query
query_movie_title = "Zodiac (film)"
# This is a good movie.

# Finding row index of movie from movie dataframe
movie_indexs = df.index[df['title'] == query_movie_title].tolist() # get list of matching indexs
if not movie_indexs:
    raise ValueError(f"Movie '{query_movie_title}' not found in DataFrame")
query_index = movie_indexs[0] # Taking first occurence of movie in case of duplication

# Query vector from query movie
query_text = df.loc[query_index, 'vector_text']  # Accesing Vector text used for embedding
# Encoding query vector using same model
query_vector = model.encode([query_text], convert_to_numpy=True).astype("float32")

# Normalize vector because we normalized FAISS Index (Needed for cosine similarity)
faiss.normalize_L2(query_vector)

# Searching for similar movies
k = 6 
distances, indices = index.search(query_vector, k) # Using search method of FASIS Index for query_vector
# indices are postional integer

# Excluding query movie
indices = indices[:,1:]

# print(distances,indices) # Both are 2D
# Sample : [[1.         0.6073408  0.59682775 0.5818113  0.5798911  0.57278365]] [[  8362  25640   2700  81982  22155 164303]]

print(f"Top 5 movies similar to '{query_movie_title}':\n")

# Mapping top indexes back to dataframe
for i, idx in enumerate(indices): # enumerate gives counter to i (from 0)
    print(f"{i+1}. {df.iloc[idx][['title','year']]} - Score: {distances[0][i]:.4f}")
