from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sklearn.metrics import silhouette_score
from typing import List
import numpy as np
import torch
from PIL import Image
# from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from torchvision import transforms
import io

app = FastAPI()

latest_clusters = {}
latest_total_images = 0
# ✅ CORS MIDDLEWARE (VERY IMPORTANT FOR REACT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/images", StaticFiles(directory="images"), name="images")

# device = torch.device(...)
device = "cpu"


model = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14")
model.eval().to(device)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.485, 0.456, 0.406),
                         std=(0.229, 0.224, 0.225))
])

@app.get("/")
def home():
    return {"message": "DINOv2 Clustering API Running"}

@app.get("/clusters")
def get_clusters():
    if not latest_clusters:
        return {
            "message": "No clustering done yet",
            "total_images": 0,
            "clusters": {}
        }

    return {
        "total_images": latest_total_images,
        "clusters": latest_clusters
    }




@app.post("/cluster-images")
async def cluster_images(files: List[UploadFile] = File(...)):
    global latest_clusters
    global latest_total_images

    embeddings = []
    image_names = []

    import os
    os.makedirs("images", exist_ok=True)

    for file in files:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        img_tensor = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            embedding = model(img_tensor)

        embeddings.append(embedding.cpu().numpy()[0])
        image_names.append(file.filename)

        # Save image
        with open(f"images/{file.filename}", "wb") as f:
            f.write(contents)

    if len(embeddings) < 2:
        return {"error": "Upload at least 2 images"}
    
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score

    embeddings = np.array(embeddings)


    # Normalize embeddings (VERY IMPORTANT)

    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms

# Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(embeddings)

# Convert similarity to distance
    distance_matrix = 1 - similarity_matrix

# Estimate number of clusters automatically
    n_samples = len(embeddings)
    n_clusters = max(2, min(5, n_samples // 3))

    clustering = AgglomerativeClustering(
        n_clusters=n_clusters,
        metric="precomputed",
        linkage="average"
)

    labels = clustering.fit_predict(distance_matrix)
    # Group results
    results = {}

    for name, label in zip(image_names, labels):
        label = str(label)
        results.setdefault(label, []).append(name)

    # ✅ Save latest session
    latest_clusters = results
    latest_total_images = len(image_names)

    return {
        "message": "Clustering completed",
        "total_images": latest_total_images,
        "clusters": latest_clusters
    }