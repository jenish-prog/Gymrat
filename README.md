# AI Fitness Trainer - Workout Tracker

An intelligent fitness tracking application that uses computer vision and pose detection to monitor your workout form and count repetitions in real-time.

## 🚀 Features

- **Real-time Pose Detection**: Uses MediaPipe to detect and track body landmarks
- **Exercise Tracking**: Monitors form and counts reps for multiple exercises
- **Visual Feedback**: Provides real-time feedback on your form
- **Multiple Exercise Support**: Currently supports biceps curls, pushups, and squats
- **User-Friendly Interface**: Clean, intuitive interface with exercise selection

## 📋 Supported Exercises

1. **Biceps Curls** - Tracks arm angle and elbow stability
2. **Pushups** - Monitors back straightness and rep counting
3. **Squats** - Tracks leg angle and form

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+ (Python 3.13 not supported by MediaPipe)
- Webcam/Camera
- Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jenish-prog/Gymrat.git
   cd Gymrat
   ```

2. **Create Python 3.11 virtual environment:**
   ```bash
   python3.11 -m venv .venv311
   ```

3. **Install dependencies:**
   ```bash
   .venv311/bin/pip install opencv-python mediapipe numpy
   ```

4. **Run the application:**
   ```bash
   .venv311/bin/python workout_tracker.py
   ```

## 🎯 Usage

1. **Start the application** using the command above
2. **Allow camera access** when prompted
3. **Select exercise** by pressing:
   - `1` for Biceps Curls
   - `2` for Pushups
   - `3` for Squats
4. **Position yourself** in front of the camera
5. **Follow the visual guides** and maintain proper form
6. **View real-time feedback** and rep counting
7. **Press `q`** to quit the application

## 🔧 Technical Details

### Technologies Used
- **OpenCV**: Computer vision for camera input and image processing
- **MediaPipe**: Google's pose detection framework for body landmark identification
- **NumPy**: Numerical operations for angle calculations and data processing

### How It Works

1. **Pose Detection**: MediaPipe's pose solution detects 33 body landmarks
2. **Angle Calculation**: Calculates joint angles using coordinate geometry
3. **Form Analysis**: Compares angles against ideal form parameters
4. **Rep Counting**: Tracks movement through different stages (up/down)
5. **Visual Feedback**: Draws landmarks, angles, and form indicators on video feed

## 🎨 Interface

The application features:
- **Top bar**: Exercise selection and app title
- **Left sidebar**: Exercise options, rep counter, and feedback display
- **Main area**: Live camera feed with pose detection overlay
- **Real-time feedback**: Form corrections and exercise guidance

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**: Ensure you're using Python 3.11 and have installed all dependencies
2. **Camera not working**: Check camera permissions and ensure no other apps are using the camera
3. **Poor pose detection**: Ensure good lighting and stand within camera frame
4. **Inaccurate rep counting**: Maintain proper form and stay within the detection area

## 📝 Requirements

- Python 3.11+
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- NumPy (`numpy`)
- Webcam or external camera

## 🔮 Future Enhancements

- [ ] Additional exercise types (deadlifts, lunges, etc.)
- [ ] Progress tracking and history
- [ ] Mobile app version
- [ ] Cloud synchronization
- [ ] Advanced form analysis

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created by jenish-prog

---

**Note**: This application uses AI-powered pose detection. For best results, ensure you're in a well-lit area and follow the on-screen guidance for proper form.
