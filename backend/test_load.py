import numpy as np

embeddings = np.load("embeddings.npy", allow_pickle=True).item()

print("Loaded embeddings:", len(embeddings))

for name, emb in embeddings.items():
    print(name, emb.shape)
    break
