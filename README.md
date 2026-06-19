---
title: Remove Background
emoji: ✂️
colorFrom: gray
colorTo: green
sdk: streamlit
app_file: app.py
pinned: false
---

# Remove Background

A minimal web app that removes the background from images using AI
([rembg](https://github.com/danielgatis/rembg) with the U²-Net model).
Upload an image and get a clean, transparent PNG instantly.

## Features

- 🖼️ Drag-and-drop upload (JPG, JPEG, PNG, WEBP)
- ✂️ One-click AI background removal — no manual masking
- 🔍 Side-by-side **before / after** preview
- ⬇️ Download the result as a **transparent PNG**
- 🌗 Light / dark theme toggle
- 🌐 English / Spanish interface toggle

## Tech stack

- [Streamlit](https://streamlit.io) — web UI
- [rembg](https://github.com/danielgatis/rembg) — background removal (U²-Net, ONNX)
- [Pillow](https://python-pillow.org) — image I/O
- [onnxruntime](https://onnxruntime.ai) — model inference (CPU)

## Run locally

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

The app opens at <http://localhost:8501>. On the first run, rembg downloads
the U²-Net model (~176 MB) and caches it locally; later runs are fast.

## Deploy

This repo is ready to deploy on free hosts:

- **Streamlit Community Cloud** — point [share.streamlit.io](https://share.streamlit.io) at this repo and pick `app.py`.
- **Hugging Face Spaces** — create a Streamlit Space; the YAML header above configures it automatically.
