from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import threading

app = Flask(__name__)

# Kết nối MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["vehicle_db"]
vehicle_collection = db["vehicles"]

# API để lấy danh sách xe hợp lệ
@app.route('/api/valid_vehicles', methods=['GET'])
def get_valid_vehicles():
    vehicles = list(vehicle_collection.find({"valid": True}, {"_id": False, "plate": 1, "entry_time": 1, "exit_time": 1}))
    print(f"Dữ liệu từ MongoDB: {vehicles}")  # Log để debug
    return jsonify(vehicles)

# API để thêm xe
@app.route('/api/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    vehicle = {
        "plate": data.get("plate"),
        "valid": True,
        "entry_time": data.get("entry_time"),
        "exit_time": data.get("exit_time")
    }
    vehicle_collection.insert_one(vehicle)
    return jsonify({"status": "success"}), 200

# API để xóa xe
@app.route('/api/delete_vehicles', methods=['POST'])
def delete_vehicles():
    data = request.get_json()
    plates = data.get("plates", [])
    vehicle_collection.delete_many({"plate": {"$in": plates}})
    return jsonify({"status": "success"}), 200

# Route để render trang HTML
@app.route('/')
def index():
    return render_template('index.html')

# Hàm chạy Flask trong thread
def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()