
import cv2
import torch
from PIL import Image
from pathlib import Path
from sentence_transformers import SentenceTransformer

MODEL_NAME = "google/embeddinggemma-2"
SAMPLE_INTERVAL = 0.5

video_path = input("Enter the full path to your video: ").strip().strip('"')

if not Path(video_path).is_file():
    raise FileNotFoundError(f"Video not found: {video_path}")

query = input("What do you want to find in the video? ").strip()

if not query:
    raise ValueError("Please enter a search query.")

print("\nLoading EmbeddingGemma 2...")
model = SentenceTransformer(MODEL_NAME, device="cuda")
print("Model device:", model.device)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise RuntimeError("Could not open the video.")

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

if fps <= 0 or total_frames <= 0:
    cap.release()
    raise RuntimeError("Could not read video metadata.")

duration = total_frames / fps
frames = []
timestamps = []

print(f"Video duration: {duration:.2f} seconds")
print("Extracting frames...")

second = 0.0

while second < duration:
    cap.set(cv2.CAP_PROP_POS_MSEC, second * 1000)
    success, frame = cap.read()

    if success:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(Image.fromarray(frame))
        timestamps.append(second)

    second += SAMPLE_INTERVAL

cap.release()

if not frames:
    raise RuntimeError("No frames could be extracted.")

print(f"Extracted {len(frames)} frames.")
print("Embedding search query...")

query_embedding = model.encode(
    query,
    prompt_name="SearchQuery",
    normalize_embeddings=True,
    convert_to_tensor=True,
)

print("Embedding video frames...")

frame_embeddings = []

for i, frame in enumerate(frames):
    embedding = model.encode(
        {"image": frame},
        normalize_embeddings=True,
        convert_to_tensor=True,
    )
    frame_embeddings.append(embedding)
    print(f"Processed frame at {timestamps[i]:.1f} seconds")

frame_embeddings = torch.stack(frame_embeddings)

scores = frame_embeddings @ query_embedding

ranked_indices = torch.argsort(scores, descending=True)

print("\nBest matching timestamps")
print("-" * 40)

for rank, idx in enumerate(ranked_indices[:3], start=1):
    i = idx.item()
    print(
        f"{rank}. Timestamp: {timestamps[i]:.1f}s"
        f" | Similarity: {scores[i].item():.4f}"
    )

print("\nSearch complete.")

