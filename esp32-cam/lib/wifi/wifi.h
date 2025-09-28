#ifndef WIFI_H
#define WIFI_H

#include <WiFi.h>

class WiFiManager {
public:
    WiFiManager(const char* ssid, const char* password);
    void connect();
private:
    const char* ssid;
    const char* password;
};

#endif
