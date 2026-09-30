# LectureLens

**An offline, on-device AI classroom companion for Snapdragon®-powered HP PCs.**

LectureLens listens to a live lecture, reads the whiteboard or slides through the webcam, and turns both into structured bilingual notes, flashcards, a short quiz and an "ask your lecture" assistant. All AI inference runs locally on the Snapdragon Hexagon NPU through ONNX Runtime with the QNN Execution Provider, so it works fully offline and student data never leaves the laptop.

> Built for the **Snapdragon® AI Lab Build & Present Challenge 2026** by Durga Prasad S (VIT). Status: early prototype.

## Features

| Stage | What it does | Model |
|---|---|---|
| Listen | Live captions / transcript of the teacher | Whisper (Qualcomm AI Hub) |
| See | Detects the board region and extracts its text | YOLO + TrOCR/EasyOCR |
| Understand | Notes, summary, key terms, flashcards, quiz | Llama 3.2 3B / Phi-3.5-mini INT4 (Qualcomm AI Hub) |
| Translate | Notes in Tamil, Hindi and more | IndicTrans2 (AI4Bharat) |
| Ask | Q&A over the day's lecture | MiniLM embeddings + LLM |

## Architecture

```
Mic ──► ASR (Whisper) ─┐
                       ├─► Notes (LLM) ─► Translate ─► Lecture pack (SQLite + files)
Webcam ► Vision (YOLO+OCR)┘                                  │
Student question ─────────► Q&A (embeddings + LLM) ◄─────────┘
            All models: ONNX Runtime + QNN EP ──► Hexagon NPU (CPU fallback)
```

## Project structure

```
lecturelens/
  runtime.py     # ONNX Runtime session factory (QNN EP → NPU, CPU fallback)
  asr.py         # speech-to-text
  vision.py      # board capture + OCR
  notes.py       # notes, flashcards, quiz generation with a local LLM
  translate.py   # Indian-language translation
  qa.py          # semantic search + answers over a lecture
  store.py       # local lecture-pack storage (SQLite)
app.py           # desktop UI (Gradio, runs locally)
docs/            # pitch deck and project description
```

## Getting started (Windows on ARM, Snapdragon X-series)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Export NPU-optimized models from Qualcomm AI Hub (see https://aihub.qualcomm.com) into the `models/` folder, e.g.:

```powershell
pip install qai-hub-models
python -m qai_hub_models.models.whisper_base.export --target-runtime onnx
```

## Roadmap

- [ ] Phase 1 – live transcript, notes and quiz on the NPU
- [ ] Phase 2 – board OCR, Tamil/Hindi translation, lecture Q&A
- [ ] Phase 3 – accessibility (large text, TTS, captions), ARM64 installer, pilot at VIT
- [ ] Phase 4 – more languages, teacher dashboard, multi-college rollout

## License

MIT
