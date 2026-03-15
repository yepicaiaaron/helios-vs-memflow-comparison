# Helios vs Memflow/Rife Side-by-Side Comparison

This repository provides a side-by-side frontend comparison of two cutting-edge real-time video generation architectures.

## Architecture Context

1. **Main Application & Orchestration (`StoryMachineAI/story-machine-ai`)**
   - **Role:** Central hub housing the React/Next.js frontend and the standalone Python worker (`worker/main.py` & `worker/super_project_engine.py`).
   - **Worker:** Acts as the orchestrator. Receives prompts via LiveKit DataChannels, uses Gemini to expand them, generates audio via Gemini Voiceover and Lyria Music, connects to the GPU via WebRTC to pull video frames, and broadcasts the combined feed to the LiveKit room.

2. **GPU Backend - Daydream Scope (`yepicaiaaron/daydream-scope-webrtc-demo`)**
   - **Role:** Heavy-lifting PyTorch backend running on GCP A100/H100 instances.
   - **Function:** Exposes an API (port 8000) and WebRTC endpoint. Loads the `memflow` diffusion pipeline and `rife` interpolation models, accepts SDP offers from the Python worker, and streams raw video frames over WebRTC.

3. **WebRTC Proxy / Relay (`yepicaiaaron/daydream-scope-proxy`, branch: `feat-super-project`)**
   - **Role:** Lightweight proxy deployed on Render.
   - **Function:** Powers the standalone "Super Project Director UI" (`director.html`). Handles WebRTC SDP handshakes and CORS proxying when connecting directly from a browser.

### Integration Note
The end goal is to fully integrate the orchestration logic from the Python worker inside `StoryMachineAI/story-machine-ai` with the GPU backend (`yepicaiaaron/daydream-scope-webrtc-demo`), ensuring that the WebRTC DataChannels handle prompt delivery and cache clearing synchronously to avoid PyTorch tensor crashes!

## Usage
Run `pip install -r requirements.txt` and start the server with `python server.py`. It runs on port 8080 by default.
