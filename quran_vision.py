from flask import Flask, Response, send_from_directory, jsonify, request
import cv2
import mediapipe as mp
import math
import time

app = Flask(__name__)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

gesture = "none"
_last_raw_gesture = "none"
_last_raw_gesture_start = 0.0

overlay_message = ""
overlay_timer = 0.0

BACK_HOLD_SECONDS = 3.5
HOLD_TIMES = {
    "back": BACK_HOLD_SECONDS,
    "scroll_up": 0.4,
    "scroll_down": 0.4,
    "select": 0.7,
    "play": 0.5,
    "pause": 0.5,
    "volume_up": 0.35,
    "volume_down": 0.35,
    "speed_up": 0.35,
    "speed_down": 0.35,
    "none": 0.0
}

def count_fingers(handLms):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    if handLms.landmark[tips[0]].x < handLms.landmark[tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)
    for i in range(1, 5):
        if handLms.landmark[tips[i]].y < handLms.landmark[tips[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def detect_gesture(handLms_list):
    if len(handLms_list) == 2:
        return "back"
    handLms = handLms_list[0]
    fingers = count_fingers(handLms)
    total = fingers.count(1)

    if total == 5:
        return "scroll_down"
    if total == 4 and fingers[0] == 0 and all(fingers[1:]):
        return "scroll_up"
    if total == 1 and fingers[1] == 1 and fingers[0] == 0:
        return "select"
    thumb_tip = handLms.landmark[4]
    index_tip = handLms.landmark[8]
    dist = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
    if dist < 0.05:
        return "play"
    if total == 2 and fingers[1] == 1 and fingers[2] == 1:
        return "pause"
    if total == 0:
        return "volume_up"
    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[0] == 0 and fingers[4] == 0:
        return "volume_down"
    if fingers[0] == 1 and fingers[4] == 1 and sum(fingers[1:4]) == 0:
        return "speed_up"
    if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 1 and fingers[4] == 1:
        return "speed_down"
    return "none"

def gen_frames():
    global gesture, _last_raw_gesture, _last_raw_gesture_start, overlay_message, overlay_timer
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        raw_candidate = "none"
        if results.multi_hand_landmarks:
            raw_candidate = detect_gesture(results.multi_hand_landmarks)
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
        now = time.time()
        if raw_candidate != _last_raw_gesture:
            _last_raw_gesture = raw_candidate
            _last_raw_gesture_start = now
        else:
            elapsed = now - _last_raw_gesture_start
            needed = HOLD_TIMES.get(raw_candidate, 0.35)
            if raw_candidate == "back":
                needed = BACK_HOLD_SECONDS
            if elapsed >= needed:
                if gesture != raw_candidate:
                    gesture = raw_candidate
                    if gesture in ("volume_up", "volume_down"):
                        overlay_message = f"Volume: {gesture.replace('_', ' ').title()}"
                        overlay_timer = now + 1.6
                    if gesture in ("speed_up", "speed_down"):
                        overlay_message = f"Speed: {gesture.replace('_', ' ').title()}"
                        overlay_timer = now + 1.6
            else:
                if raw_candidate == "none":
                    gesture = "none"
        cv2.putText(frame, f"Gesture: {gesture}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        if overlay_message and time.time() < overlay_timer:
            cv2.putText(frame, overlay_message, (10, 95),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 200, 255), 3)
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gesture')
def get_gesture():
    return jsonify({"gesture": gesture})

@app.route('/display')
def display():
    global overlay_message, overlay_timer
    t = request.args.get("type", "")
    v = request.args.get("value", "")
    try:
        if t == "volume":
            overlay_message = f"Volume: {int(float(v))}%"
            overlay_timer = time.time() + 1.8
        elif t == "speed":
            overlay_message = f"Speed: {float(v):.2f}x"
            overlay_timer = time.time() + 1.8
        else:
            overlay_message = ""
    except Exception:
        overlay_message = ""
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(debug=True)
