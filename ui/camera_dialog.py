"""
Camera capture dialog using OpenCV with live preview and capture.
"""
import os
import time
from PyQt5.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor


class CameraThread(QThread):
    frame_ready = pyqtSignal(QImage)

    def __init__(self, device=0, parent=None):
        super().__init__(parent)
        self.device = device
        self._running = False
        self.cap = None

    def run(self):
        try:
            import cv2
        except Exception:
            self.frame_ready.emit(None)
            return

        # Use DirectShow backend on Windows for better compatibility
        try:
            backend = cv2.CAP_DSHOW if os.name == 'nt' else 0
            self.cap = cv2.VideoCapture(self.device, backend) if backend else cv2.VideoCapture(self.device)
        except Exception:
            self.cap = cv2.VideoCapture(self.device)

        self._running = True
        while self._running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            # Convert BGR to RGB
            rgb = frame[:, :, ::-1]
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.frame_ready.emit(qimg)
            self.msleep(30)

        try:
            if self.cap and self.cap.isOpened():
                self.cap.release()
        except Exception:
            pass

    def stop(self):
        self._running = False
        self.wait()


class CameraCaptureDialog(QDialog):
    """Dialog that shows live camera feed and allows capturing an image.

    on_capture callback: function(path) called when an image is captured
    """

    def __init__(self, on_capture=None, device=0, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Capture Receipt")
        self.setModal(True)
        self.on_capture = on_capture
        self.current_frame = None
        self.device = device

        self._init_ui()
        self._start_camera()

    def _init_ui(self):
        self.preview = QLabel()
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.preview.setStyleSheet("background-color: black; border-radius: 8px;")

        capture_btn = QPushButton("Capture")
        capture_btn.setMinimumHeight(48)
        capture_btn.clicked.connect(self.capture)

        close_btn = QPushButton("Close")
        close_btn.setMinimumHeight(48)
        close_btn.clicked.connect(self.close)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(capture_btn)
        btn_layout.addWidget(close_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.preview, 1)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.resize(800, 600)

    def _start_camera(self):
        try:
            import cv2
        except Exception:
            QMessageBox.critical(self, "Missing Dependency", "OpenCV (cv2) is not installed. Install opencv-python to use the camera.")
            return

        # Auto-detect camera if device is None or -1
        device_to_use = self.device if self.device is not None and self.device >= 0 else None
        if device_to_use is None:
            # Probe a few indices to find the first working camera
            found = None
            for idx in range(0, 4):
                try:
                    cap = cv2.VideoCapture(idx)
                    if cap is None or not cap.isOpened():
                        try:
                            cap.release()
                        except Exception:
                            pass
                        continue
                    ret, _ = cap.read()
                    if ret:
                        found = idx
                        try:
                            cap.release()
                        except Exception:
                            pass
                        break
                    try:
                        cap.release()
                    except Exception:
                        pass
                except Exception:
                    continue
            device_to_use = found if found is not None else 0

        # Start camera thread with chosen device
        self.thread = CameraThread(device=device_to_use)
        self.thread.frame_ready.connect(self._on_frame)
        self.thread.start()

    def _on_frame(self, qimg: QImage):
        if qimg is None:
            return
        # Store current frame
        self.current_frame = qimg

        # Draw animated scan frame overlay
        img = qimg.copy()
        painter = QPainter(img)
        painter.setRenderHint(QPainter.Antialiasing)
        pen_color = QColor(0, 168, 118, 200)
        painter.setPen(pen_color)
        # draw center rectangular guide
        w = img.width()
        h = img.height()
        rect_w = int(w * 0.8)
        rect_h = int(h * 0.6)
        rect_x = (w - rect_w) // 2
        rect_y = (h - rect_h) // 2
        painter.drawRoundedRect(rect_x, rect_y, rect_w, rect_h, 12, 12)
        painter.end()

        pix = QPixmap.fromImage(img)
        pix = pix.scaled(self.preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.preview.setPixmap(pix)

    def capture(self):
        if self.current_frame is None:
            QMessageBox.warning(self, "No Frame", "No camera frame available to capture.")
            return

        # Save current frame to a temporary file (let the receipt processor copy it into assets)
        import tempfile
        tmp_dir = tempfile.gettempdir()
        filename = f"receipt_capture_{int(time.time())}.png"
        dest_path = os.path.join(tmp_dir, filename)

        # Convert QImage to PNG
        self.current_frame.save(dest_path)

        # Call on_capture callback if provided
        if callable(self.on_capture):
            try:
                self.on_capture(dest_path)
            except Exception as e:
                QMessageBox.critical(self, "Processing Error", f"Failed to process captured image: {e}")

        # Close dialog after capture
        self.close()

    def closeEvent(self, event):
        try:
            if hasattr(self, 'thread') and self.thread is not None:
                self.thread.stop()
        except Exception:
            pass
        super().closeEvent(event)
