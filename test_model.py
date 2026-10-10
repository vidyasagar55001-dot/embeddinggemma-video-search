
from sentence_transformers import SentenceTransformer
from pathlib import Path
import torch

MODEL_NAME = "google/embeddinggemma-2"

print("Loading EmbeddingGemma 2...")
model = SentenceTransformer(MODEL_NAME, device="cuda")
print("Loaded on:", model.device)

video_path = input("Enter the full path to your video: ").strip().strip('"')

if not Path(video_path).is_file():
    raise FileNotFoundError(f"Video not found: {video_path}")

print("Testing video embedding...")

try:
    video_embedding = model.encode(
        {"video": video_path},
        normalize_embeddings=True,
    )

    print("Video embedding succeeded!")
    print("Embedding shape:", video_embedding.shape)

except Exception as error:
    print("\nVideo embedding failed.")
    print("Error type:", type(error).__name__)
    print("Error details:", error)
