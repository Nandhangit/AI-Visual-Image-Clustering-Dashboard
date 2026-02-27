import numpy as np
from sklearn.cluster import KMeans
import csv

embeddings = np.load("embeddings.npy", allow_pickle=True).item()

image_names = list(embeddings.keys())
embedding_vectors = list(embeddings.values())

kmeans = KMeans(n_clusters=2, random_state=42)
labels = kmeans.fit_predict(embedding_vectors)

with open("cluster_results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Image Name", "Cluster"])

    for name, label in zip(image_names, labels):
        writer.writerow([name, label])

print("Cluster results exported successfully")
