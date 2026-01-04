# Hand-Gesture-canvas

Finger Canvas is a real-time hand gesture–based drawing application built with **Python**, **MediaPipe**, and **OpenCV**.  
You can draw on the screen using **only your index finger**, just like an invisible pen in the air 🎨.

---

## Features

- Real-time webcam hand tracking
- Draw **only when the index finger is up**
- Automatically stops drawing when other fingers are raised
- Smooth continuous drawing on a virtual canvas
- Gesture logic separated into clean, reusable code
- Supports up to **2 hands** (uses Hand 0 for drawing)

---

## Gesture Logic

Drawing is enabled **only if**:
- Index finger is **up**
- Middle, Ring, and Pinky fingers are **down**
- Thumb is ignored

This ensures accurate and intentional drawing.

---


## Requirements

Install all dependencies before running:

```bash
pip install opencv-python mediapipe numpy
