#include <Arduino.h>
#include "wifi.h"
#include "mqtt.h"
#include "camera.h"
#include "servo.h"
#include "ir.h"

const char* ssid = "your-ssid";
const char* password = "your-password";
const char* mqtt_server = "broker.hivemq.com";
int mqtt_port = 1883;

WiFiManager wifi(ssid, password);
MQTTManager mqtt(mqtt_server, mqtt_port, "", "");
IRManager ir(32, 33, &mqtt);  // ví dụ chân GPIO
ServoManager servo(25);

void setup() {
    Serial.begin(115200);

    wifi.connect();
    mqtt.setup();
    ir.init();
    servo.init();
    CameraManager::setup();
}

void loop() {
    if (!mqtt.isConnected()) {
        mqtt.reconnect();
    }
    mqtt.loop();

    ir.handleEntry();
    ir.handleExit();
}
