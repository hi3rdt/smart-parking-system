#include "servo.h"

ServoManager::ServoManager(int pin) : pin(pin) {}

void ServoManager::init() {
    servo.attach(pin);
}

void ServoManager::activate() {
    servo.write(90);
    delay(1000);
    servo.write(0);
}
