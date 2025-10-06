import cv2
import mediapipe as mp
import numpy as np
import math

class PoseDetector:
    """
    A class to detect pose landmarks using MediaPipe.
    """
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.complexity = complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode, self.complexity, self.smooth_landmarks,
                                      self.enable_segmentation, self.smooth_segmentation,
                                      self.detection_con, self.track_con)
        self.mp_draw = mp.solutions.drawing_utils

    def find_pose(self, img, draw=True):
        """Finds pose landmarks in an image."""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        if self.results.pose_landmarks and draw:
            self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return img

    def get_position(self, img):
        """Extracts the landmark positions."""
        self.lm_list = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
        return self.lm_list

    def find_angle(self, img, p1, p2, p3, draw=True):
        """Calculates and draws the angle between three points."""
        # Get the landmarks
        x1, y1 = self.lm_list[p1][1:]
        x2, y2 = self.lm_list[p2][1:]
        x3, y3 = self.lm_list[p3][1:]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

def main():
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()

    # Exercise state variables
    exercise = "Biceps"
    rep_count = 0
    stage = None # 'up' or 'down'
    feedback = ""

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.resize(img, (1280, 720))
        
        # --- UI and Drawing ---
        # Draw background elements for UI
        cv2.rectangle(img, (0, 0), (1280, 100), (24, 24, 24), -1) # Top bar
        cv2.rectangle(img, (20, 120), (320, 700), (24, 24, 24), -1) # Left sidebar
        
        # Title
        cv2.putText(img, "AI FITNESS TRAINER", (450, 65), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3, cv2.LINE_AA)
        
        # Sidebar info
        cv2.putText(img, "EXERCISE", (60, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Dropdown / Buttons for exercise selection
        # For simplicity, we'll use text as buttons. A real UI would be better.
        biceps_color = (0, 255, 0) if exercise == "Biceps" else (255, 255, 255)
        pushups_color = (0, 255, 0) if exercise == "Pushups" else (255, 255, 255)
        squats_color = (0, 255, 0) if exercise == "Squats" else (255, 255, 255)
        
        cv2.putText(img, "Biceps", (80, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, biceps_color, 2)
        cv2.putText(img, "Pushups", (80, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, pushups_color, 2)
        cv2.putText(img, "Squats", (80, 340), cv2.FONT_HERSHEY_SIMPLEX, 1, squats_color, 2)

        # Rep Counter Display
        cv2.putText(img, "REPS", (120, 420), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.rectangle(img, (70, 460), (270, 560), (0, 0, 0), -1)
        cv2.putText(img, str(rep_count), (110, 540), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
        
        # Feedback Display
        cv2.putText(img, "FEEDBACK", (80, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.rectangle(img, (30, 640), (310, 680), (0, 0, 0), -1)
        cv2.putText(img, feedback, (40, 670), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # Pose Detection on the main video feed area
        video_feed = img[:, 320:]
        video_feed = detector.find_pose(video_feed, draw=True)
        lm_list = detector.get_position(video_feed)

        if len(lm_list) != 0:
            # --- BICEP CURL LOGIC ---
            if exercise == "Biceps":
                # Use left arm for this example
                angle = detector.find_angle(video_feed, 11, 13, 15) # Shoulder, Elbow, Wrist
                
                # Check for correct form (e.g., elbow should not move too much)
                shoulder_y = lm_list[11][2]
                elbow_y = lm_list[13][2]
                
                form_ok = abs(shoulder_y - elbow_y) < 40 # Simple check for swinging
                
                if form_ok:
                    feedback = "Good Form"
                    # Rep counting logic
                    if angle > 160:
                        stage = "down"
                    if angle < 30 and stage == 'down':
                        stage = "up"
                        rep_count += 1
                        feedback = "Up"
                else:
                    feedback = "Fix Elbow"

            # --- PUSH-UP LOGIC ---
            elif exercise == "Pushups":
                # Use right arm and hip for this example
                angle = detector.find_angle(video_feed, 12, 14, 16) # Shoulder, Elbow, Wrist
                back_angle = detector.find_angle(video_feed, 12, 24, 26) # Shoulder, Hip, Knee
                
                # Check for correct form
                form_ok = back_angle > 150 # Check for straight back
                
                if form_ok:
                    feedback = "Good Form"
                    # Rep counting logic
                    if angle > 160:
                        stage = "up"
                    if angle < 90 and stage == 'up':
                        stage = "down"
                        rep_count += 1
                        feedback = "Down"
                else:
                    feedback = "Straighten Back"

            # --- SQUAT LOGIC ---
            elif exercise == "Squats":
                # Use left leg for this example
                angle = detector.find_angle(video_feed, 23, 25, 27) # Hip, Knee, Ankle
                
                # Rep counting logic
                if angle > 160:
                    stage = "up"
                    feedback = "Up"
                if angle < 90 and stage == 'up':
                    stage = "down"
                    rep_count += 1
                    feedback = "Good Squat!"


        # Display the final image
        cv2.imshow("AI Fitness Trainer", img)

        # Handle key presses for exercise selection
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('1'):
            exercise = "Biceps"
            rep_count = 0
            stage = None
        elif key == ord('2'):
            exercise = "Pushups"
            rep_count = 0
            stage = None
        elif key == ord('3'):
            exercise = "Squats"
            rep_count = 0
            stage = None


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
