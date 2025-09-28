#ifndef SERVO_H
#define SERVO_H

#include <Arduino.h>
#include <ESP32Servo.h>

extern const int servoPin;
extern Servo myServo;

void setupServo();

#endif