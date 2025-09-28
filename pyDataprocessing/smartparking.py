import paho.mqtt.client as mqtt
import cv2
import numpy as np
import torch
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import datetime
from PIL import Image
from ultralytics import YOLO
import re
from pymongo import MongoClient
import json


# ===== Connected MongoDB =====
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["vehicle_db"]
vehicle_collection = db["vehicles"]

# ===== YOLO and VietOCR =====
model = YOLO("best.pt")
config = Cfg.load_config_from_name('vgg_transformer')
config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'
detector = Predictor(config)

# ===== Hàm kiểm tra định dạng biển số Việt Nam =====
def is_valid_plate(plate_text):
    plate_text = plate_text.replace(" ", "").upper()
    pattern = r'^\d{2}[A-Z]{1,2}-\d{3,5}$|^\d{2}[A-Z]{1,2}-\d{3}\.\d{2}$|^\d{2}[A-Z]\d-\d{4,5}$'
    return bool(re.match(pattern, plate_text))

# ===== Tiền xử lý ảnh =====
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    processed_img = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    return Image.fromarray(processed_img)

# ===== MQTT Callbacks =====
def on_connect(client, userdata, flags, rc):
    print(f"Connected to HiveMQ Cloud, code: {rc}")
    client.subscribe("vehicle/image", qos=1)
    client.subscribe("vehicle/ir", qos=1)

def on_message(client, userdata, msg):
    if msg.topic == "vehicle/image":
        print(f"[MQTT] Received image from ESP32-CAM: {len(msg.payload)} bytes")
        nparr = np.frombuffer(msg.payload, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            print("[ERROR] Failed to decode image.")
            return

        results = model(img)
        detections = results[0].boxes.xyxy.cpu().numpy()
        confs = results[0].boxes.conf.cpu().numpy()

        plate_text = None
        plate_img = None

        for i, box in enumerate(detections):
            x1, y1, x2, y2 = map(int, box)
            if confs[i] > 0.5:
                plate_img = img[y1:y2, x1:x2]
                processed_img = preprocess_image(plate_img)
                plate_text = detector.predict(processed_img)
                print(f"[AI] Detected license plate: {plate_text}")
                break

        entry_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if plate_text and is_valid_plate(plate_text):
            entry = {
                "plate": plate_text,
                "valid": True,
                "entry_time": entry_time,
                "exit_time": None
            }
            vehicle_collection.insert_one(entry)
            print(f"[DB] Saved to MongoDB: {entry}")

            # Cập nhật file JSON
            data = list(vehicle_collection.find({}, {"_id": False}))
            with open("full_export.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("[JSON] Updated full_export.json file")

            client.publish("vehicle/plate", plate_text, qos=1)
            client.publish("vehicle/servo", "ACTIVATE", qos=1)
            print("[MQTT] Sent servo activation command for entry.")
        else:
            print("[INFO] Not saved due to invalid plate or no detection.")

        cv2.destroyAllWindows()

    elif msg.topic == "vehicle/ir":
        print(f"[MQTT] Received signal from IR sensor: {msg.payload.decode('utf-8')}")
        # Tìm bản ghi mới nhất chưa có exit_time
        vehicle = vehicle_collection.find_one(
            {"exit_time": None},
            sort=[("entry_time", -1)]
        )

        if vehicle:
            exit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            vehicle_collection.update_one(
                {"_id": vehicle["_id"]},
                {"$set": {"exit_time": exit_time}}
            )
            print(f"[DB] Updated exit_time for {vehicle['plate']}: {exit_time}")

            # Cập nhật file JSON
            data = list(vehicle_collection.find({}, {"_id": False}))
            with open("full_export.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            client.publish("vehicle/servo", "ACTIVATE", qos=1)
            print("[MQTT] Sent servo activation command for exit.")
        else:
            print("[INFO] No vehicle found without exit time.")

# ===== MQTT Client =====
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set()
client.username_pw_set("tuduchiep123", "Tuduchiep1405")

print("Connecting to HiveMQ Cloud...")
client.connect("e081335f47cb4fb78a222c0bca0ac487.s1.eu.hivemq.cloud", 8883, 60)
client.loop_forever()