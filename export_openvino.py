"""Конвертирует модели в OpenVINO (ускорение на процессорах Intel). Запустить один раз."""
from ultralytics import YOLO

from detector import MODELS, MODELS_DIR

for name, file in MODELS.items():
    print(f"== {name}: {file}")
    YOLO(str(MODELS_DIR / file)).export(format="openvino", imgsz=640, half=False)
print("Готово. detector.py автоматически будет использовать OpenVINO-версии.")
