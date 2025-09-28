#ifndef IR_H
#define IR_H

#include <Arduino.h>
#include "mqtt.h"
#include "camera.h"

class IRManager {
public:
    IRManager(int entryPin, int exitPin, MQTTManager* mqtt);
    void init();
    void handleEntry();
    void handleExit();
private:
    int entryPin;
    int exitPin;
    MQTTManager* mqtt;
};

#endif
