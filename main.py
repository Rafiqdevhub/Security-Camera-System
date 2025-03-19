import cv2
import time
import datetime
import os
from ultralytics import YOLO

# Initialize video capture
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Load YOLO model for object detection
try:
    # Load a pre-trained YOLOv8 model
    model = YOLO("yolov8n.pt")  # This will download the model if not already present
    print("YOLO model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    cap.release()
    exit()

# We'll use a simpler approach for face cascade since cv2.data path might not be accessible
face_cascade = None
try:
    # Try several common paths for Haar cascades
    haar_paths = [
        "haarcascade_frontalface_default.xml",  # Check in current directory
        os.path.join(cv2.__path__[0], "data", "haarcascade_frontalface_default.xml"),  # OpenCV path
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "haarcascade_frontalface_default.xml")  # Current file directory
    ]
    
    for path in haar_paths:
        if os.path.exists(path):
            face_cascade = cv2.CascadeClassifier(path)
            if not face_cascade.empty():
                print(f"Face cascade classifier loaded successfully from {path}")
                break
    
    if face_cascade is None or face_cascade.empty():
        print("Warning: Could not load face classifier. Face detection will be unavailable.")
        face_cascade = None
except Exception as e:
    print(f"Warning: Could not load face classifier: {e}")
    print("Face detection will be unavailable. Only YOLO detection will be used.")
    face_cascade = None

# Create output directory if it doesn't exist
output_dir = "recordings"
os.makedirs(output_dir, exist_ok=True)

# Detection variables
detection = False
detection_stopped_time = 0  # Initialize with a default value
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

# Get video properties
frame_size = (int(cap.get(3)), int(cap.get(4)))
# Define fourcc explicitly instead of using VideoWriter_fourcc
fourcc = 0x7634706d  # This is 'mp4v' in hex
out = None

# Define color map for different objects (BGR format)
color_map = {
    'person': (0, 0, 255),     # Red
    'car': (0, 255, 255),      # Yellow
    'dog': (255, 0, 0),        # Blue
    'cat': (255, 0, 255),      # Magenta
    'bicycle': (0, 255, 0),    # Green
    'default': (255, 255, 0)   # Cyan (for other objects)
}

# Print instructions
print("\nINSTRUCTIONS:")
print("- Press 'q' to exit the application")
print("- Press 's' to manually stop recording")
print("- Recording will start automatically when objects are detected")
print("- Recording will stop automatically if no objects are detected for 5 seconds\n")

try:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        # Make a copy of the frame for displaying results
        display_frame = frame.copy()
        
        # Process detection results
        detected_objects = []
        
        # Run YOLO detection
        results = model(frame)
        
        # Extract and visualize YOLO detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                # Get class and confidence
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Get class name
                class_name = result.names[cls]
                detected_objects.append(class_name)
                
                # Choose color based on class
                color = color_map.get(class_name, color_map['default'])
                
                # Draw bounding box
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                
                # Create label with class name and confidence
                label = f"{class_name} {conf:.2f}"
                
                # Calculate label position
                label_size, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                y1 = max(y1, label_size[1])
                
                # Draw label background
                cv2.rectangle(display_frame, 
                              (x1, y1 - label_size[1] - 10), 
                              (x1 + label_size[0], y1),
                              color, 
                              -1)
                
                # Draw label text
                cv2.putText(display_frame, 
                           label, 
                           (x1, y1 - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, 
                           (255, 255, 255), 
                           2)
        
        # If no YOLO objects were detected and face cascade is available, try face detection as fallback
        if not detected_objects and face_cascade is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(display_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(display_frame, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                detected_objects.append("face")
        
        # Handle detection logic
        if detected_objects:
            if detection:
                timer_started = False
            else:
                detection = True
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                out = cv2.VideoWriter(
                    f"{output_dir}/{current_time}.mp4", fourcc, 20, frame_size)
                print(f"Started Recording! ({current_time}.mp4)")
                # Log detected objects
                print(f"Detected: {', '.join(detected_objects)}")
        elif detection:
            if timer_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    detection = False
                    timer_started = False
                    if out is not None:
                        out.release()
                        out = None
                    print('Stopped Recording! (No objects detected for 5 seconds)')
            else:
                timer_started = True
                detection_stopped_time = time.time()
        
        if detection and out is not None:
            # Write the frame with detection boxes to video
            out.write(display_frame)
            
            # Add recording indicator and object count
            recording_text = f"RECORDING - Objects: {len(detected_objects)}"
            cv2.putText(display_frame, recording_text, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Add object names in corner
            if detected_objects:
                unique_objects = list(set(detected_objects))
                objects_text = f"Detected: {', '.join(unique_objects)}"
                cv2.putText(display_frame, objects_text, (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Add instructions on screen
        cv2.putText(display_frame, "Press 's' to stop recording", (10, frame_size[1] - 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(display_frame, "Press 'q' to quit", (10, frame_size[1] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Display the frame
        cv2.imshow("Security Camera", display_frame)
        
        # Check for key presses
        key = cv2.waitKey(1)
        if key == ord('q'):
            # Exit the application
            break
        elif key == ord('s'):
            # Manually stop recording if currently recording
            if detection and out is not None:
                detection = False
                timer_started = False
                out.release()
                out = None
                print('Recording stopped manually!')
            
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