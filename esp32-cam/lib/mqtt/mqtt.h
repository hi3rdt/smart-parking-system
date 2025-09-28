#ifndef MQTT_H
#define MQTT_H

#include <Arduino.h>              // Bắt buộc phải có dòng này
#include <WiFi.h>                 // Thêm cả WiFi.h
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

class MQTTManager {
public:
    MQTTManager(const char* broker, int port);
    void connect();
    void publish(const char* topic, const char* message);
    void subscribe(const char* topic);

private:
    const char* broker;
    int port;
    WiFiClientSecure wifiClient;
    PubSubClient client;
};

#endif
