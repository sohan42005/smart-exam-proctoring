# REFERENCES

## 1. Official Documentation

[1] Python Software Foundation, "Python 3 Documentation," [Online]. Available: https://docs.python.org/3/

[2] Pallets Projects, "Flask Documentation," [Online]. Available: https://flask.palletsprojects.com/

[3] SQLite, "SQLite Official Documentation," [Online]. Available: https://www.sqlite.org/docs.html

[4] OpenCV, "OpenCV (Open Source Computer Vision Library) Documentation," [Online]. Available: https://docs.opencv.org/

[5] Ultralytics, "Ultralytics YOLOv8 Documentation," [Online]. Available: https://docs.ultralytics.com/

## 2. Browser APIs & Web Standards

[6] MDN Web Docs, "MediaDevices.getUserMedia() Web API," Mozilla. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia

[7] MDN Web Docs, "Fullscreen API," Mozilla. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Fullscreen_API

[8] MDN Web Docs, "Page Visibility API," Mozilla. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API

## 3. Academic & Research Papers

[9] P. Viola and M. Jones, "Rapid object detection using a boosted cascade of simple features," *Proceedings of the 2001 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)*, Kauai, HI, USA, 2001. (Reference for the OpenCV Haar Cascade face detection method used in the project).

[10] J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, "You Only Look Once: Unified, Real-Time Object Detection," *2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, Las Vegas, NV, USA, 2016. (Foundational reference for the YOLO object detection architecture).

---

# TECHNOLOGY TO SOURCE MAPPING

| Technology / Concept | Purpose in Project | Reference |
| :--- | :--- | :--- |
| **Python** | Backend language and AI processing logic | Official Python Documentation |
| **Flask** | Web application backend, routing, and session management | Official Flask Documentation |
| **SQLite** | Local relational database for students, questions, and attempts | Official SQLite Documentation |
| **OpenCV** | Image manipulation and Haar Cascade-based Face Detection | Official OpenCV Documentation |
| **YOLOv8 (Ultralytics)** | Deep learning object detection for identifying mobile phones | Official Ultralytics Documentation |
| **getUserMedia API** | Web browser access to user's webcam and microphone | MDN Web Docs |
| **Fullscreen API** | Forcing and monitoring the fullscreen examination mode | MDN Web Docs |
| **Page Visibility API** | Detecting tab switching and window blurring | MDN Web Docs |

*(Note: MediaPipe was intentionally removed from this project implementation in favor of robust OpenCV Haar Cascades for face detection to ensure broader cross-platform compatibility).*
