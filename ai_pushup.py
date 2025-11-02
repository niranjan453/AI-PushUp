import cv2
import numpy as np
import mediapipe as mp
import time
from collections import deque

# ------------------------------------------------
# Calculate angle between 3 points
# ------------------------------------------------
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# ------------------------------------------------
# Setup webcam and video output
# ------------------------------------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("❌ Could not open webcam")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
output_path = 'pushup_dual_arm_tracker.mp4'

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# ------------------------------------------------
# Initialize variables
# ------------------------------------------------
counter = 0
stage = "up"
feedback = ""
angle_window_left = deque(maxlen=5)
angle_window_right = deque(maxlen=5)
prev_time = 0

print("🎥 Dual-arm push-up tracking started... Press 'q' to quit.")

# ------------------------------------------------
# Main loop
# ------------------------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Frame not captured.")
        break

    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark

        # Key joints (left and right sides)
        left_shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        right_shoulder = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        hip = [lm[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
               lm[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        ankle = [lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                 lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        # Calculate angles
        left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        back_angle = calculate_angle(right_shoulder, hip, ankle)

        # Smooth angles (reduce jitter)
        angle_window_left.append(left_elbow_angle)
        angle_window_right.append(right_elbow_angle)
        smooth_left = np.mean(angle_window_left)
        smooth_right = np.mean(angle_window_right)

        # ------------------------------
        # Push-up counting logic
        # ------------------------------
        down_threshold = 80
        up_threshold = 150

        if smooth_left <= down_threshold and smooth_right <= down_threshold and stage == "up":
            stage = "down"
            feedback = "Going down..."
        elif smooth_left >= up_threshold and smooth_right >= up_threshold and stage == "down":
            stage = "up"
            counter += 1
            feedback = "✅ Good rep!"

        # ------------------------------
        # Form accuracy check
        # ------------------------------
        if back_angle < 150:
            feedback = "⚠️ Keep your back straight!"
        elif 150 <= back_angle <= 180 and stage == "down":
            feedback = "Perfect form!"

        # ------------------------------
        # Draw angles on each elbow
        # ------------------------------
        left_elbow_coords = tuple(np.multiply(left_elbow, [frame_width, frame_height]).astype(int))
        right_elbow_coords = tuple(np.multiply(right_elbow, [frame_width, frame_height]).astype(int))

        cv2.putText(image, f"L:{int(smooth_left)}", left_elbow_coords,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(image, f"R:{int(smooth_right)}", right_elbow_coords,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # Draw pose landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # ------------------------------
    # FPS and top info bar
    # ------------------------------
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time

    # Top black bar
    cv2.rectangle(image, (0, 0), (frame_width, 60), (0, 0, 0), -1)
    cv2.putText(image, f"Reps: {counter} | Stage: {stage} | FPS: {int(fps)} | {feedback}",
                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    # Save and display
    out.write(image)
    cv2.imshow('Push-up Tracker (Dual Arm + Top Info Bar)', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Stopped.")
        break

cap.release()
out.release()
cv2.destroyAllWindows()
print(f"✅ Push-up video saved as '{output_path}'")
