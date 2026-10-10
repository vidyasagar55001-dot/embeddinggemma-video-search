# EmbeddingGemma 2 — Local Video Semantic Search

A Python-based video semantic search prototype powered by Google's `google/embeddinggemma-2` model. Search a local video using natural-language descriptions and retrieve the three most semantically relevant timestamps.

Instead of searching for exact words or filenames, the system compares embeddings of a text query and sampled video frames to identify visually relevant moments.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Understanding the Results](#understanding-the-results)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Learning Outcomes](#learning-outcomes)

## Project Overview

Finding a specific event in a video can be time-consuming, especially when the video does not contain searchable text or metadata.

This project demonstrates how multimodal embeddings can make video content searchable using ordinary language.

For example, a user can enter:

`A person getting into a car`

The program samples frames from a local video, generates image embeddings, encodes the text query, calculates similarity scores, and displays the three highest-ranked timestamps.

**Project status:** Working command-line prototype.

**Model:** `google/embeddinggemma-2`

**Frame sampling interval:** 0.5 seconds.

**Search output:** Top three matching timestamps and similarity scores.

## Features

- Natural-language search over local video content.
- Automatic video frame extraction using OpenCV.
- Text and image embedding generation using EmbeddingGemma 2.
- Semantic similarity scoring between queries and frames.
- Ranking of frames based on similarity scores.
- Timestamp-based results for locating relevant moments.
- GPU-based model execution using CUDA-compatible PyTorch.
- Local video processing through a Python command-line interface.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Google EmbeddingGemma 2 | Generates text and image embeddings |
| Sentence Transformers | Loads the model and generates embeddings |
| PyTorch | Tensor operations and GPU execution |
| OpenCV | Reads videos and extracts frames |
| Pillow | Converts frames into image objects |
| FFmpeg and TorchCodec | Support for video decoding in the model's video-input workflow |
| Visual Studio Code | Development environment |
| Git and GitHub | Version control and project hosting |

## How It Works

The system uses the following pipeline:

```text
              Local Video
                  |
                  v
          Open video with OpenCV
                  |
                  v
       Extract frames every 0.5 seconds
                  |
                  v
       Convert frames to RGB images
                  |
                  v
       Generate image embeddings
                  |
                  | 
                  |             Text Query
                  |                 |
                  |                 v
                  |       Generate text embedding
                  |                 |
                  v                 v
              Compare embeddings
                     |
                     v
             Calculate similarity
                     |
                     v
             Rank matching frames
                     |
                     v
          Display the top 3 timestamps
```

### Step 1: Read the video

The program asks the user for the full path to a local video file. It checks whether the file exists before processing it.

### Step 2: Extract video frames

OpenCV reads the video's frame rate and total frame count to estimate its duration.

The program samples frames every 0.5 seconds. Each successfully extracted frame is associated with its sampling timestamp.

### Step 3: Generate image embeddings

Each frame is converted from OpenCV's BGR format to RGB and represented as a Pillow image.

The embedding model transforms the image into a numerical vector that represents its learned semantic information.

### Step 4: Generate the text embedding

The user enters a natural-language search query.

The model encodes the query using its `SearchQuery` prompt configuration. The resulting vector represents the query in the model's embedding space.

### Step 5: Calculate similarity

The query and image embeddings are normalized. The program then calculates their dot product.

For normalized vectors, this is equivalent to cosine similarity:

`similarity = query_embedding · frame_embedding`

Higher scores indicate a stronger semantic match according to the model.

### Step 6: Rank and display results

The program sorts the similarity scores in descending order and displays the three highest-ranked timestamps with their scores.

These timestamps help the user locate and inspect potentially relevant moments in the original video.

## Project Structure

The current project contains these files:

```text
embedding-video-search/
├── .git/
├── .venv/
├── .gitignore
├── test_model.py
└── video_search.py
```

Additional documentation and dependency files can be added as follows:

```text
embedding-video-search/
├── .gitignore
├── README.md
├── requirements.txt
├── test_model.py
└── video_search.py
```

The `.git/` directory stores local Git history and configuration. The `.venv/` directory contains the Python virtual environment. These folders are not normally committed to GitHub.

### `test_model.py`

Tests the embedding model and its text-embedding functionality.

### `video_search.py`

Implements the final video semantic search pipeline: video input, frame sampling, embedding generation, similarity calculation, and top-three result ranking.

### `requirements.txt`

Lists the Python packages required to recreate the project environment.

## Requirements

- Windows 11 or another compatible operating system.
- Python version compatible with the installed model and dependencies.
- Git.
- Visual Studio Code or another Python development environment.
- A compatible NVIDIA GPU and CUDA-enabled PyTorch installation for the current GPU execution configuration.
- Internet access for downloading model files during the initial model load.
- Sufficient memory and disk space for model execution.

**Note:** The current program explicitly selects CUDA. A CPU-only computer will require a code change to support CPU execution.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/vidyasagar55001-dot/embedding-video-search.git
cd embedding-video-search
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

If PowerShell blocks activation, use the environment's Python executable directly instead.

### 3. Install PyTorch

Install a PyTorch build compatible with your Python version and CUDA environment using the official selector:

https://pytorch.org/get-started/locally/

Verify GPU availability:

```powershell
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CUDA GPU unavailable')"
```

The current video-search script expects CUDA to be available.

### 4. Install Python dependencies

Install the packages used by the project:

```powershell
python -m pip install --upgrade pip
python -m pip install sentence-transformers transformers pillow opencv-python
```

PyTorch is required for tensor calculations and model execution. Install it separately as described above if it is not already installed correctly.

For workflows that use the model's native video-input functionality, TorchCodec, FFmpeg, and any additional audio/video dependencies required by that workflow may also be needed. The final `video_search.py` implementation described here extracts frames with OpenCV.

## Running the Project

Run commands from the repository root.

### 1. Test the model

```powershell
.\.venv\Scripts\python.exe test_model.py
```

This runs the model test script.

### 2. Start video semantic search

```powershell
.\.venv\Scripts\python.exe video_search.py
```

### 3. Enter the video path

When prompted, enter the full path to an existing local video file, for example:

`C:\Videos\sample.mp4`

Use the path to a video that exists on your computer. The example path is illustrative.

### 4. Enter a search query

For example:

`A person getting into a car`

### 5. Wait for processing

The program loads EmbeddingGemma 2, extracts frames, generates embeddings, compares the vectors, and ranks the results.

The first model load can take longer because model files may need to be downloaded.

### 6. Inspect the results

The program prints the three highest-ranked timestamps and their similarity scores.

Open the original video at these timestamps to verify whether the results match the requested event.

## Understanding the Results

Example output format:

```text
1. Timestamp: 2.0s | Similarity: 0.XXXX
2. Timestamp: 6.5s | Similarity: 0.XXXX
3. Timestamp: 9.0s | Similarity: 0.XXXX
```

The values above illustrate the output format only; actual timestamps and scores depend on the video and query.

- **Timestamp:** The time associated with the sampled frame.
- **Similarity score:** The calculated similarity between the text query and the image embedding.
- **Ranking:** Results are ordered from highest to lowest similarity.

A high similarity score does not guarantee that an event occurred. Always inspect the corresponding video moments.

## Limitations

- The system analyzes sampled frames, not every frame of the video.
- An event occurring between sampled frames may be missed.
- The program returns timestamps rather than playable video clips or thumbnails.
- Similarity ranking is not a factual verification system.
- Processing a large video can require substantial time and GPU memory.
- The current implementation handles one local video and one query at a time.
- The project currently provides a command-line interface rather than a web or mobile application.

## Future Improvements

- Display matching frame thumbnails alongside timestamps.
- Allow users to configure the frame-sampling interval.
- Cache frame embeddings to speed up repeated searches.
- Add a graphical interface for video selection and query input.
- Play the video directly from a selected result timestamp.
- Support searching across multiple videos.
- Add a vector index for faster retrieval over large video collections.
- Explore temporal and native video embeddings for understanding events across sequences of frames.

## Learning Outcomes

This project demonstrates practical applications of:

- Multimodal embeddings.
- Semantic search and information retrieval.
- Text and image representation.
- Cosine similarity and vector operations.
- Video processing using OpenCV.
- GPU-based model execution.
- Python environment management.
- Git version control and GitHub collaboration.

## Acknowledgements

- Google for the EmbeddingGemma 2 model.
- Sentence Transformers for model integration and embedding APIs.
- OpenCV and Pillow for video and image processing.
- PyTorch for tensor operations and GPU computation.

## License

This repository does not currently specify a project license. Add an appropriate license if you want to permit others to reuse, modify, or distribute your code. Check the model's license separately before redistributing model files or using the model commercially.
# EmbeddingGemma 2 — Local Video Semantic Search

A Python-based video semantic search prototype powered by Google's `google/embeddinggemma-2` model. Search a local video using natural-language descriptions and retrieve the three most semantically relevant timestamps.

Instead of searching for exact words or filenames, the system compares embeddings of a text query and sampled video frames to identify visually relevant moments.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Understanding the Results](#understanding-the-results)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Learning Outcomes](#learning-outcomes)

## Project Overview

Finding a specific event in a video can be time-consuming, especially when the video does not contain searchable text or metadata.

This project demonstrates how multimodal embeddings can make video content searchable using ordinary language.

For example, a user can enter:

`A person getting into a car`

The program samples frames from a local video, generates image embeddings, encodes the text query, calculates similarity scores, and displays the three highest-ranked timestamps.

**Project status:** Working command-line prototype.

**Model:** `google/embeddinggemma-2`

**Frame sampling interval:** 0.5 seconds.

**Search output:** Top three matching timestamps and similarity scores.

## Features

- Natural-language search over local video content.
- Automatic video frame extraction using OpenCV.
- Text and image embedding generation using EmbeddingGemma 2.
- Semantic similarity scoring between queries and frames.
- Ranking of frames based on similarity scores.
- Timestamp-based results for locating relevant moments.
- GPU-based model execution using CUDA-compatible PyTorch.
- Local video processing through a Python command-line interface.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Google EmbeddingGemma 2 | Generates text and image embeddings |
| Sentence Transformers | Loads the model and generates embeddings |
| PyTorch | Tensor operations and GPU execution |
| OpenCV | Reads videos and extracts frames |
| Pillow | Converts frames into image objects |
| FFmpeg and TorchCodec | Support for video decoding in the model's video-input workflow |
| Visual Studio Code | Development environment |
| Git and GitHub | Version control and project hosting |

## How It Works

The system uses the following pipeline:

```text
              Local Video
                  |
                  v
          Open video with OpenCV
                  |
                  v
       Extract frames every 0.5 seconds
                  |
                  v
       Convert frames to RGB images
                  |
                  v
       Generate image embeddings
                  |
                  | 
                  |             Text Query
                  |                 |
                  |                 v
                  |       Generate text embedding
                  |                 |
                  v                 v
              Compare embeddings
                     |
                     v
             Calculate similarity
                     |
                     v
             Rank matching frames
                     |
                     v
          Display the top 3 timestamps
```

### Step 1: Read the video

The program asks the user for the full path to a local video file. It checks whether the file exists before processing it.

### Step 2: Extract video frames

OpenCV reads the video's frame rate and total frame count to estimate its duration.

The program samples frames every 0.5 seconds. Each successfully extracted frame is associated with its sampling timestamp.

### Step 3: Generate image embeddings

Each frame is converted from OpenCV's BGR format to RGB and represented as a Pillow image.

The embedding model transforms the image into a numerical vector that represents its learned semantic information.

### Step 4: Generate the text embedding

The user enters a natural-language search query.

The model encodes the query using its `SearchQuery` prompt configuration. The resulting vector represents the query in the model's embedding space.

### Step 5: Calculate similarity

The query and image embeddings are normalized. The program then calculates their dot product.

For normalized vectors, this is equivalent to cosine similarity:

`similarity = query_embedding · frame_embedding`

Higher scores indicate a stronger semantic match according to the model.

### Step 6: Rank and display results

The program sorts the similarity scores in descending order and displays the three highest-ranked timestamps with their scores.

These timestamps help the user locate and inspect potentially relevant moments in the original video.

## Project Structure

The current project contains these files:

```text
embedding-video-search/
├── .git/
├── .venv/
├── .gitignore
├── test_model.py
└── video_search.py
```

Additional documentation and dependency files can be added as follows:

```text
embedding-video-search/
├── .gitignore
├── README.md
├── requirements.txt
├── test_model.py
└── video_search.py
```

The `.git/` directory stores local Git history and configuration. The `.venv/` directory contains the Python virtual environment. These folders are not normally committed to GitHub.

### `test_model.py`

Tests the embedding model and its text-embedding functionality.

### `video_search.py`

Implements the final video semantic search pipeline: video input, frame sampling, embedding generation, similarity calculation, and top-three result ranking.

### `requirements.txt`

Lists the Python packages required to recreate the project environment.

## Requirements

- Windows 11 or another compatible operating system.
- Python version compatible with the installed model and dependencies.
- Git.
- Visual Studio Code or another Python development environment.
- A compatible NVIDIA GPU and CUDA-enabled PyTorch installation for the current GPU execution configuration.
- Internet access for downloading model files during the initial model load.
- Sufficient memory and disk space for model execution.

**Note:** The current program explicitly selects CUDA. A CPU-only computer will require a code change to support CPU execution.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/vidyasagar55001-dot/embedding-video-search.git
cd embedding-video-search
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

If PowerShell blocks activation, use the environment's Python executable directly instead.

### 3. Install PyTorch

Install a PyTorch build compatible with your Python version and CUDA environment using the official selector:

https://pytorch.org/get-started/locally/

Verify GPU availability:

```powershell
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CUDA GPU unavailable')"
```

The current video-search script expects CUDA to be available.

### 4. Install Python dependencies

Install the packages used by the project:

```powershell
python -m pip install --upgrade pip
python -m pip install sentence-transformers transformers pillow opencv-python
```

PyTorch is required for tensor calculations and model execution. Install it separately as described above if it is not already installed correctly.

For workflows that use the model's native video-input functionality, TorchCodec, FFmpeg, and any additional audio/video dependencies required by that workflow may also be needed. The final `video_search.py` implementation described here extracts frames with OpenCV.

## Running the Project

Run commands from the repository root.

### 1. Test the model

```powershell
.\.venv\Scripts\python.exe test_model.py
```

This runs the model test script.

### 2. Start video semantic search

```powershell
.\.venv\Scripts\python.exe video_search.py
```

### 3. Enter the video path

When prompted, enter the full path to an existing local video file, for example:

`C:\Videos\sample.mp4`

Use the path to a video that exists on your computer. The example path is illustrative.

### 4. Enter a search query

For example:

`A person getting into a car`

### 5. Wait for processing

The program loads EmbeddingGemma 2, extracts frames, generates embeddings, compares the vectors, and ranks the results.

The first model load can take longer because model files may need to be downloaded.

### 6. Inspect the results

The program prints the three highest-ranked timestamps and their similarity scores.

Open the original video at these timestamps to verify whether the results match the requested event.

## Understanding the Results

Example output format:

```text
1. Timestamp: 2.0s | Similarity: 0.XXXX
2. Timestamp: 6.5s | Similarity: 0.XXXX
3. Timestamp: 9.0s | Similarity: 0.XXXX
```

The values above illustrate the output format only; actual timestamps and scores depend on the video and query.

- **Timestamp:** The time associated with the sampled frame.
- **Similarity score:** The calculated similarity between the text query and the image embedding.
- **Ranking:** Results are ordered from highest to lowest similarity.

A high similarity score does not guarantee that an event occurred. Always inspect the corresponding video moments.

## Limitations

- The system analyzes sampled frames, not every frame of the video.
- An event occurring between sampled frames may be missed.
- The program returns timestamps rather than playable video clips or thumbnails.
- Similarity ranking is not a factual verification system.
- Processing a large video can require substantial time and GPU memory.
- The current implementation handles one local video and one query at a time.
- The project currently provides a command-line interface rather than a web or mobile application.

## Future Improvements

- Display matching frame thumbnails alongside timestamps.
- Allow users to configure the frame-sampling interval.
- Cache frame embeddings to speed up repeated searches.
- Add a graphical interface for video selection and query input.
- Play the video directly from a selected result timestamp.
- Support searching across multiple videos.
- Add a vector index for faster retrieval over large video collections.
- Explore temporal and native video embeddings for understanding events across sequences of frames.

## Learning Outcomes

This project demonstrates practical applications of:

- Multimodal embeddings.
- Semantic search and information retrieval.
- Text and image representation.
- Cosine similarity and vector operations.
- Video processing using OpenCV.
- GPU-based model execution.
- Python environment management.
- Git version control and GitHub collaboration.

## Acknowledgements

- Google for the EmbeddingGemma 2 model.
- Sentence Transformers for model integration and embedding APIs.
- OpenCV and Pillow for video and image processing.
- PyTorch for tensor operations and GPU computation.

## License

This repository does not currently specify a project license. Add an appropriate license if you want to permit others to reuse, modify, or distribute your code. Check the model's license separately before redistributing model files or using the model commercially.
