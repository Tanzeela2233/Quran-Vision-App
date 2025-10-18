# 🌙 Quran Vision — AI-Powered Gesture-Controlled Quran Interaction

**Quran Vision** is an AI-based project that allows users to **interact with the Holy Quran using hand gestures** — no clicks, no keyboard.  
Using **MediaPipe**, **OpenCV**, and **Flask**, it recognizes your hand gestures through the webcam to **control Quran recitation, scroll Surahs, and manage playback** — creating a futuristic, touchless Quran experience.

---

## ✅ Features

- ✋ **Real-Time Hand Gesture Recognition**  
  Detects hand gestures via webcam using **MediaPipe Hands**.

- 🎧 **Gesture-Based Quran Control**
  - ☝️ **1 Finger → Select**
  - 🖐️ **5 Fingers → Scroll Down**
  - 🤚 **4 Fingers → Scroll Up**
  - ✊ **0 Fingers → Volume Up**
  - 🤞 **2 Fingers → Pause**
  - 👌 **Thumb + Index Touch → Play**
  - ✋✋ **Both Hands → Back / Exit**
  - 🤟 **Specific Gestures → Speed Up / Down**

- 📖 **Quran Integration (Quran.com API)**  
  Fetches and displays Surahs, translations, and recitations.

- ⚡ **Live Video Stream with Overlay Feedback**  
  Real-time gesture detection overlayed on webcam video.

- 🎨 **Interactive Frontend Interface**  
  Modern and responsive UI with smooth animations.

---

## 🧠 Tech Stack

| Category | Technologies Used |
|-----------|------------------|
| **Backend** | Flask (Python) |
| **Computer Vision** | MediaPipe, OpenCV |
| **Frontend** | HTML, CSS, JavaScript |
| **Data Source** | Quran.com API |
| **Others** | AJAX, JSON, RESTful Communication |

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally 👇

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/quran-vision.git
cd quran-vision
2️⃣ Install Dependencies
Make sure you have Python 3.x installed, then run:

bash
Copy code
pip install flask opencv-python mediapipe
3️⃣ Run the Flask Server
bash
Copy code
python app.py
4️⃣ Open in Browser
Visit:

cpp
Copy code
http://127.0.0.1:5000
Your webcam will start, and you can control the Quran recitation with your hand gestures 🌙

🧩 Gesture Reference Guide
Gesture	Action
✋ Open Hand (5 Fingers)	Scroll Down
🤚 4 Fingers	Scroll Up
☝️ Index Finger	Select
🤞 2 Fingers	Pause
👌 Thumb + Index Touch	Play
✊ Closed Fist	Volume Up
✋✋ Two Hands	Back
🤟 Thumb + Pinky	Speed Up
✌️ Specific Combo	Speed Down


💡 How It Works
Camera Feed → Captured by OpenCV and processed in real-time.

Hand Tracking → MediaPipe detects 21 key hand landmarks.

Gesture Recognition → Logic classifies gestures (play, pause, scroll, etc.).

Flask Backend → Streams live video and gesture data to the frontend.

Frontend JS → Updates Quran display or audio based on detected gestures.


📜 License
This project is open-source under the MIT License — free to use and modify with proper credit.











