import os
import torch
from PIL import Image
from torchvision import transforms
import numpy as np
# from dinov2.models import dinov2_vitb14

# Select device (CPU for you)
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# Load DINOv2 ViT-B/14 model
# model = dinov2_vitb14(pretrained=True)
model = torch.hub.load(
    "facebookresearch/dinov2","dinov2_vitb14"
)
model.eval()
model.to(device)
print("Model loaded successfully on", device)

# Image preprocessing (required)
transform = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=(0.485, 0.456, 0.406),
        std=(0.229, 0.224, 0.225),
    ),
])



def extract_folder_embeddings(folder_path):
    embeddings = {}

    for file in os.listdir(folder_path):
        if file.lower().endswith(("project1.jpg", "project2.png", "project3.jpeg","project4.jpg")):
            img_path = os.path.join(folder_path, file)

            img = Image.open(img_path).convert("RGB")
            img = transform(img).unsqueeze(0).to(device)

            with torch.no_grad():
                emb = model(img)

            # embeddings[file] = emb.cpu().numpy()[0]
            vector = emb.cpu().numpy()[0]
            vector = vector / np.linalg.norm(vector)   # 🔥 NORMALIZATION
            embeddings[file] = vector

    return embeddings

folder_path = "images"
embeddings = extract_folder_embeddings(folder_path)

print("Total images processed:", len(embeddings))

for name, emb in embeddings.items():
    print("Image:", name)
    print("Embedding shape:", emb.shape)
    print("First 5 values:", emb[:5])
    break

if __name__ == "__main__":
    folder_path = "images"
    embeddings_dict = extract_folder_embeddings(folder_path)

    print("Total images processed:", len(embeddings_dict))
    
    
    
    # Convert dictionary to array (IMPORTANT)
    image_names = list(embeddings_dict.keys())
    embeddings = np.array(list(embeddings_dict.values()))

    print("Embedding shape:", embeddings.shape)

    # Save both
    np.save("embeddings.npy", embeddings)
    np.save("image_names.npy", image_names)

    print("Embeddings saved successfully")