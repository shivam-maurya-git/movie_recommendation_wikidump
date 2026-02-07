import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import pickle

df = pd.read_csv("movie1.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = df['vector_text'].to_list()
print(len(texts))


#If convert_to_numpy=True

# Output → NumPy array

# Example shape → (num_texts, embedding_dimension)

# Required when using:

# FAISS

# NumPy operations

# Saving embeddings to disk

# If convert_to_numpy=False

# Output → PyTorch tensors

# Useful when:

# Continuing deep-learning pipeline in PyTorch

# Training / fine-tuning models
embeddings = model.encode(
    sentences = texts, # list
    batch_size=128, #Processes 512 movies at a time to save RAM and speed up computation.
    show_progress_bar=True,
    convert_to_numpy=True
).astype("float32")
print("Step 1: embeddings created")

faiss.normalize_L2(embeddings)
print("Step 2: normalized")
dimension = embeddings.shape[1] # Number of elements in each vector
# Adding Index to vector databases
index = faiss.IndexFlatIP(dimension) #It only creates an empty container (index structure) that is ready to accept vectors of a specific size.
print("Step 3: index created")
index.add(embeddings) #Inserts all movie embeddings into the FAISS vector database.
print("Step 4: vectors added")

print("Total vectors:", index.ntotal)

# Save vector store permanently
faiss.write_index(index, "movies_vector_store.faiss")
print("Step 5: index saved")

# Save metadata separately
with open("movies_metadata.pkl", "wb") as f: #write-binary mode (create new file) #binary file suitable for pickle.
    pickle.dump(df, f)
#Pickle preserves data types and structure exactly.
# Faster to load/save than CSV for large DataFrames.
#But, we can use csv file also

# Need metadata because : 
# When you search in the vector index, FAISS returns only indices of vectors, not the actual movie info.

# You need the full DataFrame to map those indices back to movie information.
print("Vector store saved permanently.")
