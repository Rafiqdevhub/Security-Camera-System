# Security Camera System

A Python-based security camera application that uses advanced computer vision to detect and identify multiple types of objects in real-time, automatically recording when objects are detected.

## Features

- **Advanced Object Detection**: Uses YOLOv8 to detect and label a wide variety of objects (people, cars, animals, etc.) in the video feed.
- **Real-time Object Labeling**: Displays colored bounding boxes around detected objects with labels showing object type and confidence percentage.
- **Automatic Recording**: Starts recording automatically when any object is detected.
- **Manual Controls**: Press 's' to manually stop recording at any time.
- **Smart Recording Management**: Continues recording for 5 seconds after the last detection to avoid creating multiple short clips.
- **Visual Feedback**: Shows real-time information about detected objects and recording status.
- **Fallback Detection**: Uses Haar cascade for face detection as a fallback when YOLO doesn't detect objects.
- **Organized Storage**: Saves recordings with timestamped filenames in a dedicated folder.

## Requirements

- Python 3.6+
- OpenCV 4.5.5+
- Ultralytics 8.0+

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Rafiqdevhub/Security-Camera-System.git
   cd Security-Camera-System
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main script to start the security camera:

```
python main.py
```

- Press 's' to manually stop recording if it's in progress.
- Press 'q' to quit the application.
- Recordings are automatically saved in the 'recordings' folder.

## How it Works

The system continuously analyzes the webcam feed using the YOLOv8 object detection model:

1. When an object is detected:
   - Starts recording to an MP4 file with a timestamp-based filename
   - Draws colored bounding boxes around detected objects
   - Displays object names and confidence levels
   - Shows a "RECORDING" indicator with object count
   - Lists all detected object types

2. The recording continues until:
   - No objects are detected for 5 seconds (automatic stop)
   - User presses 's' key (manual stop)

3. If YOLO doesn't detect any objects, the system falls back to traditional face detection using Haar cascades (if available).

## Configuration

You can adjust the following parameters in the `main.py` file:

- `SECONDS_TO_RECORD_AFTER_DETECTION`: How long to keep recording after the last detection (default: 5 seconds)
- `color_map`: Customize colors for different types of objects
- Change the camera source by modifying the `VideoCapture` parameter (default: 0, which is usually the built-in webcam)

## License

This project is licensed under the MIT License - see the LICENSE file for details.