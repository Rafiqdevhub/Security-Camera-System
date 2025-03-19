import cv2
import time
import datetime
import os

# Initialize video capture
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Load cascade classifiers
try:
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    body_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_fullbody.xml")
except Exception as e:
    print(f"Error loading cascade classifiers: {e}")
    cap.release()
    exit()

# Create output directory if it doesn't exist
output_dir = "recordings"
os.makedirs(output_dir, exist_ok=True)

# Detection variables
detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

# Get video properties
frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = None

try:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture frame.")
            break
            
        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces and bodies
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        # Handle detection logic
        if len(faces) + len(bodies) > 0:
            if detection:
                timer_started = False
            else:
                detection = True
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                out = cv2.VideoWriter(
                    f"{output_dir}/{current_time}.mp4", fourcc, 20, frame_size)
                print(f"Started Recording! ({current_time}.mp4)")
        elif detection:
            if timer_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    detection = False
                    timer_started = False
                    out.release()
                    out = None
                    print('Stopped Recording!')
            else:
                timer_started = True
                detection_stopped_time = time.time()
        
        if detection and out is not None:
            out.write(frame)
            
            # Add recording indicator
            cv2.putText(frame, "RECORDING", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (0, 0, 255), 2)
        
        # Display the frame
        cv2.imshow("Security Camera", frame)
        
        # Break loop on 'q' press
        if cv2.waitKey(1) == ord('q'):
            break
            
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Clean up resources
    if out is not None:
        out.release()
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    print("Resources released and application closed.")