#ifndef CAMERA_H
#define CAMERA_H

#include "esp_camera.h"

class CameraManager {
public:
    static bool setup();
    static bool capture(camera_fb_t **fb);
};

#endif
