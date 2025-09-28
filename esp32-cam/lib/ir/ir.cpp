#include "ir.h"

IRManager::IRManager(int entryPin, int exitPin, MQTTManager* mqtt)
    : entryPin(entryPin), exitPin(exitPin), mqtt(mqtt) {}

void IRManager::init() {
    pinMode(entryPin, INPUT);
    pinMode(exitPin, INPUT);
}

void IRManager::handleEntry() {
    if (digitalRead(entryPin) == HIGH) {
        mqtt->publish("parking/entry", "Car entered");
    }
}

void IRManager::handleExit() {
    if (digitalRead(exitPin) == HIGH) {
        mqtt->publish("parking/exit", "Car exited");
    }
}
