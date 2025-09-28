#include "mqtt.h"

MQTTManager::MQTTManager(const char* server, int port, const char* user, const char* password)
    : server(server), port(port), user(user), password(password), client(espClient) {}

void MQTTManager::setup() {
    client.setServer(server, port);
}

void MQTTManager::loop() {
    client.loop();
}

void MQTTManager::reconnect() {
    while (!client.connected()) {
        if (client.connect("ESP32Client", user, password)) {
            // Sub lại topic cần
        } else {
            delay(5000);
        }
    }
}

void MQTTManager::setCallback(MQTT_CALLBACK_SIGNATURE) {
    client.setCallback(callback);
}

bool MQTTManager::publish(const char* topic, const char* payload, bool retained) {
    return client.publish(topic, payload, retained);
}

bool MQTTManager::publish(const char* topic, const uint8_t* payload, unsigned int length, bool retained) {
    return client.publish(topic, payload, length, retained);
}

bool MQTTManager::subscribe(const char* topic, int qos) {
    return client.subscribe(topic, qos);
}

bool MQTTManager::isConnected() {
    return client.connected();
}
