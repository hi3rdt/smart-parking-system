#include "camera.h"

bool CameraManager::setup() {
    // cấu hình camera
    return true;
}

bool CameraManager::capture(camera_fb_t **fb) {
    *fb = esp_camera_fb_get();
    return (*fb != nullptr);
}
