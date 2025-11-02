AI PushUp – Dual Arm Tracker (OpenCV + MediaPipe)

AI PushUp is an intelligent, real-time push-up counter and posture analyzer built using OpenCV, MediaPipe, and Python.
It tracks both arms, counts reps automatically, checks your form accuracy, and provides instant feedback — making your workouts smarter and more effective.

🚀 Features

✅ AI-powered dual-arm tracking – Detects both arms to ensure balanced movement
✅ Automatic rep counter – Tracks each push-up in real-time using elbow joint angles
✅ Smart posture detection – Warns you when your back is not straight
✅ Real-time feedback overlay – Displays feedback, FPS, and total reps live
✅ Video recording – Saves your workout session automatically
✅ Angle smoothing – Uses a moving average to stabilize angle detection

🧠 How It Works

AI PushUp uses MediaPipe Pose Estimation to identify body landmarks and calculate:

Elbow Angles (Left & Right) – Determines if you’re in the “up” or “down” stage

Back Angle – Ensures proper posture and straight alignment

Stage Transition – Detects transitions between up/down to count a rep

Feedback Messages – Provides real-time guidance and motivation

🛠️ Installation

1️⃣ Clone the repository
git clone https://github.com/niranjan453/ai-pushup.git

cd ai-pushup

2️⃣ Install dependencies

Make sure you have Python 3.8+ installed:

pip install opencv-python mediapipe numpy

3️⃣ Run the program
python ai_pushup.py

🎥 Output

Real-time pose tracking with:

Pose landmarks

Elbow angles (L/R)

Rep count, FPS, and feedback

Output video automatically saved as:

ai_pushup_output.mp4

⚙️ Controls
Key	Action
q	Quit the application
📊 Parameters and Logic
Parameter	Description
down_threshold = 80	When elbow angle ≤ 80°, stage changes to “down”
up_threshold = 150	When elbow angle ≥ 150°, stage changes to “up”
back_angle < 150	Displays warning to correct posture

🧩 Dependencies
Library	Purpose
opencv-python	Webcam access, video recording, visualization
mediapipe	Pose detection and landmark tracking
numpy	Mathematical calculations (angles, smoothing)
collections.deque	Moving window for stable angle averaging
time	FPS calculation and frame timing

🧍 Feedback Messages
Message	Description
✅ Good rep!	Successfully completed one full push-up
⚠️ Keep your back straight!	Incorrect posture detected
Perfect form!	Excellent push-up technique
🧰 Future Upgrades

🔊 Voice feedback system (using pyttsx3)

📊 Performance tracking dashboard

📱 Mobile app integration

🧠 AI-based posture scoring

👨‍💻 Author

Niranjan Bhardwaj
💡 Passionate about AI, Computer Vision, and Human Activity Recognition
📧 Contact: niranjankumarnb45@.com

🌐 GitHub: niranjan453

📜 License

This project is licensed under the MIT License — you’re free to use, modify, and distribute.
