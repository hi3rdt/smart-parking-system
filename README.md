# Smart Parking System

A smart parking system integrating ESP32-CAM for image capture, MQTT for communication, and a Python backend for AI-based license plate recognition and database management.

## Project Overview
This project combines:
- **ESP32-CAM**: Captures images and controls a servo gate using IR sensors.
- **Python**: Processes images with YOLO and VietOCR, stores data in MongoDB, and provides a Flask API.
- **MQTT**: Facilitates real-time communication between ESP32 and the backend.

## Structure
- `esp32-cam/`: Contains Arduino code for ESP32-CAM (WiFi, MQTT, Camera, Servo, IR modules).
- `pyDataprocessing/`: Contains Python scripts (`smart_parking.py` for image processing and `app.py` for API).
- `docs/`: Includes demo videos and diagrams (architecture).

## Project Structure
The project is organized as follows:
├── pyDataprocessing/
│   ├── smartparking.py
│   └── app.py
├── esp32/
│   ├── platformio.ini
│   ├── src/
│   │   └── main.cpp
│   └── lib/
│       ├── wifi/
│       │   ├── wifi.h
│       │   └── wifi.cpp
│       ├── mqtt/
│       │   ├── mqtt.h
│       │   └── mqtt.cpp
│       ├── camera/
│       │   ├── camera.h
│       │   └── camera.cpp
│       ├── servo/
│       │   ├── servo.h
│       │   └── servo.cpp
│       └── ir/
│           ├── ir.h
│           └── ir.cpp
└── docs/
├── demo.mp4
├── architecture.jpg


- **`README.md`**: Project documentation and setup instructions.
- **`requirements.txt`**: List of Python dependencies.
- **`.gitignore`**: Files and folders to exclude from Git.
- **`platformio.ini`**: Configuration for ESP32-CAM build environment.
- **`pyDataprocessing/`**: Directory for Python source code.
- **`esp32-cam/`**: Directory for ESP32-CAM Arduino code and libraries.
- **`docs/`**: Directory for demo videos and diagrams.

## Installation

### ESP32 Setup
1. Install [PlatformIO](https://platformio.org/) in VSCode.
2. Open the `esp32-cam/` folder in PlatformIO.
3. Run `pio run` to build and `pio run -t upload` to flash the code to ESP32-CAM.
4. Open Serial Monitor (`pio device monitor`) to view logs.

### Python Backend Setup
1. Ensure Python 3.8+ is installed.
2. Install required libraries:
3. Run the image processing script:
4. Run the API server:

## Usage
- **ESP32-CAM**: Sends images via MQTT when IR sensors detect a vehicle.
- **Python Backend**: Recognizes license plates, stores data in MongoDB, and activates the servo via MQTT.
- **API**: Access the Flask API at `http://localhost:5000`.

## Demo
Watch the demo video:
![Demo Video](docs/demo.mp4)

## Documentation
### System Architecture
![Architecture Diagram](docs/architecture.png)

## Requirements
- **ESP32-CAM**: WiFi module, camera, servo, IR sensors.
- **Python Libraries**: Listed in `requirements.txt`.
- **MongoDB**: Running locally (`mongodb://localhost:27017/`).

## Contributors
- Hiep Tu Duc (tuduchiep123@gmail.com)

## Acknowledgments
- Thanks to the open-source communities for YOLO, VietOCR, and MQTT libraries.
