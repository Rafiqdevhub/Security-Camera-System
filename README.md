# Security Camera System

A Python-based security camera application that uses computer vision to detect faces and bodies, automatically recording when motion is detected.

## Features

- **Real-time Face and Body Detection**: Uses Haar cascade classifiers to detect faces and bodies in the video feed.
- **Automatic Recording**: Starts recording automatically when a person is detected.
- **Smart Recording Management**: Continues recording for 5 seconds after the last detection to avoid creating multiple short clips.
- **Visual Feedback**: Shows rectangles around detected faces and displays a "RECORDING" indicator when active.
- **Organized Storage**: Saves recordings with timestamped filenames in a dedicated folder.

## Requirements

- Python 3.6+
- OpenCV 4.5.5+

## Installation

1. Clone this repository:
   ```
   git clone 
   cd security-camera
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

- Press 'q' to quit the application.
- Recordings are automatically saved in the 'recordings' folder.

## How it Works

The system continuously analyzes the webcam feed for faces and bodies using OpenCV's Haar cascade classifiers. When a detection occurs, the system:

1. Starts recording to an MP4 file with a timestamp-based filename
2. Highlights detected faces with blue rectangles
3. Shows a "RECORDING" indicator in the corner of the display
4. Continues recording until no detection is made for 5 seconds
5. Automatically saves and closes the video file

## Configuration

You can adjust the following parameters in the `main.py` file:

- `SECONDS_TO_RECORD_AFTER_DETECTION`: How long to keep recording after the last detection (default: 5 seconds)
- Change the camera source by modifying the `VideoCapture` parameter (default: 0, which is usually the built-in webcam)

## License

This project is licensed under the MIT License - see the LICENSE file for details.