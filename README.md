# EmbeddingGemma Video Search

A semantic video-search system that uses Google's EmbeddingGemma embedding model to find relevant moments in a video using natural-language queries.

Instead of searching only by filenames or manually written tags, this project represents text queries and video frames as embeddings and compares their semantic similarity.

## Overview

Searching for a particular event in a video can be difficult when the video contains no searchable text or metadata.

This project explores how multimodal embeddings can help users search video content using natural-language descriptions.

For example, a user can provide a query such as:

> A person getting into a car.

The system extracts representative frames from a video, generates image embeddings, encodes the text query, and ranks the frames according to their similarity to the query.

## Features

- **Natural-language search:** Search video content using text descriptions.
- **Video frame extraction:** Extract frames at regular time intervals.
- **Multimodal embeddings:** Represent text and images in a shared embedding space.
- **Semantic similarity:** Compare query and frame embeddings.
- **Frame ranking:** Rank extracted frames by their similarity to the query.
- **Local execution:** Run the project using Python in a local development environment.

## Technology Stack

- **Python** — Core programming language.
- **EmbeddingGemma** — Embedding model for representing text and images.
- **Sentence Transformers** — Model loading and embedding generation.
- **OpenCV** — Video reading and frame extraction.
- **Pillow** — Image handling.
- **PyTorch** — Tensor computation and model execution.
- **VS Code** — Development environment.

## Architecture

```text
Input Video
    |
    v
Extract Frames at Regular Intervals
    |
    v
Convert Frames into Image Embeddings
    |
    v
Store Embeddings in Memory

User's Text Query
    |
    v
Generate Text Embedding
    |
    v
Compare Query Embedding
with Frame Embeddings
    |
    v
Calculate Similarity Scores
    |
    v
Rank Frames by Relevance
    |
    v
Return the Most Relevant Frames
```

## How It Works

### 1. Video frame extraction

The system opens a video and extracts frames at regular intervals.

For example, extracting one frame every two seconds reduces the number of images that must be processed compared with analyzing every frame.

### 2. Generate image embeddings

Each extracted frame is passed to the embedding model using its image-input format.

An embedding is a numerical vector that represents information about the image. Images with semantically related content can have similar representations.

### 3. Encode the search query

The user enters a natural-language description of the content they want to find.

The text is converted into an embedding using the model's supported text-query encoding method.

### 4. Calculate similarity

The query embedding is compared with the image embeddings.

When the vectors are normalized, their dot product can be used as cosine similarity:

`similarity = query_embedding · image_embedding`

A higher similarity score generally indicates a stronger semantic match.

### 5. Rank the results

The extracted frames are sorted by their similarity scores. The highest-ranked frames are returned as the most relevant candidates.

**Important:** Similarity is a measure of semantic relevance, not a guarantee that the described event actually occurred.

## Requirements

- Python 3.10 or a compatible version supported by the installed dependencies.
- Git.
- Visual Studio Code or another Python editor.
- Internet access for downloading model files on the first run.
- Sufficient RAM and storage for the model and video-processing dependencies.

A compatible GPU is optional if the model and dependencies support CPU execution.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/vidyasagar55001-dot/embeddinggemma-video-search.git
cd embeddinggemma-video-search
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the virtual environment's Python executable directly instead.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install sentence-transformers transformers pillow soundfile torchcodec opencv-python
```

PyTorch is used by the embedding stack and may be installed automatically as a dependency. If necessary, install a compatible PyTorch build for your system.

### 4. Download or load the model

The model is loaded through the Sentence Transformers library. The first run may download model files from the configured model repository.

Use the exact model identifier and loading configuration from the working project code.

## Running the Project

Run the project's Python entry point from the repository root.

If your entry-point file is named `video_search.py`, execute:

```powershell
python video_search.py
```

If you use the virtual environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe video_search.py
```

Follow the prompts implemented in the program to select or process the video and enter a search query.

## Example Use Case

**Input:** A video containing several different activities.

**Search query:** `A person getting into a car`

**Processing:**

1. Extract frames from the video.
2. Generate image embeddings for the extracted frames.
3. Encode the search query.
4. Compare the query embedding with each image embedding.
5. Rank frames according to semantic similarity.

**Output:** The highest-ranked extracted frames that are semantically related to the query.

Actual results depend on the video, sampling interval, model behavior, and similarity threshold.

## Project Structure

The structure below is an example. Adjust the filenames to match the files in your repository.

```text
embeddinggemma-video-search/
├── README.md
├── .gitignore
├── requirements.txt
├── video_search.py
└── other_project_files/
```

The virtual environment, cached model weights, and large source videos should normally remain outside version control.

## Limitations

- Only extracted frames are searched; events between sampled frames may be missed.
- A similarity score does not prove that an event occurred.
- Processing every frame of a long video can be computationally expensive.
- Results depend on the model's ability to represent the visual content and the user's query.
- This implementation searches sampled visual frames rather than understanding the complete temporal sequence of a video.

## Future Improvements

- Search multiple videos from a single interface.
- Display timestamps and preview the matching frames.
- Adjust frame-sampling intervals.
- Cache embeddings to avoid recomputing them.
- Introduce a vector index for efficient search across large collections.
- Build a web or desktop interface for uploading videos and searching them.
- Extend the system to retrieve short video clips around relevant timestamps.

## Learning Outcomes

This project demonstrates practical concepts in:

- Multimodal machine learning.
- Text and image embeddings.
- Semantic search.
- Vector similarity.
- Video preprocessing.
- Python model integration.
- Building an AI-powered retrieval pipeline.

## License

Choose and add an appropriate open-source license if you want others to reuse your code. Check the model's license separately before redistributing model files or using the model commercially.
