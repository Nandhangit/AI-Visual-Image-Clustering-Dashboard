
import numpy as np
from sklearn.cluster import KMeans

# Load embeddings and image names
embeddings = np.load("embeddings.npy")
image_names = np.load("image_names.npy")

print("Total images:", len(image_names))
print("Embedding size:", embeddings.shape)

# Number of clusters
k = 2

# Run clustering
kmeans = KMeans(n_clusters=k, random_state=42)
labels = kmeans.fit_predict(embeddings)

print("\nCluster Results:")
print("-----------------")

for name, label in zip(image_names, labels):
    print(f"{name} -> Cluster {label}")
