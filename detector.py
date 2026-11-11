"""Ядро распознавания: загрузка моделей (OpenVINO, если есть) и детекция."""
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

from labels_ru import ru

ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "models"

# Доступные модели:
#   oiv7 — Open Images V7, ~600 классов (ручка, линейка, книга/тетрадь, ластик, ножницы...)
#   coco — COCO, 80 классов, точнее и быстрее на людях, машинах, животных
MODELS = {
    "oiv7": "yolov8s-oiv7.pt",
    "coco": "yolo11n.pt",
}

_cache = {}


def load_model(name: str = "oiv7") -> YOLO:
    """Загружает модель. Если рядом есть OpenVINO-версия — берёт её (в 2–3 раза быстрее на CPU)."""
    if name in _cache:
        return _cache[name]
    pt_file = MODELS_DIR / MODELS[name]
    ov_dir = MODELS_DIR / f"{pt_file.stem}_openvino_model"
    if ov_dir.exists():
        model = YOLO(str(ov_dir), task="detect")
    else:
        if not pt_file.exists():  # первый запуск: скачать веса в models/
            from ultralytics.utils.downloads import attempt_download_asset
            MODELS_DIR.mkdir(exist_ok=True)
            attempt_download_asset(pt_file)
        model = YOLO(str(pt_file))
    _cache[name] = model
    return model


def detect(image_bgr, model_name="oiv7", conf=0.25, only=None, imgsz=640, plot=True):
    """
    Распознаёт объекты на изображении (numpy BGR, как из cv2.imread).
    only — список английских названий классов для фильтра (например ["Pen", "Ruler"]).
    Возвращает (картинка_с_рамками_BGR, список_объектов).
    """
    model = load_model(model_name)
    # device="cpu" обязательно: иначе OpenVINO выбирает AUTO и пытается задействовать
    # встроенную графику Intel UHD 630, а её драйвер на этом ПК падает (0xC0000005).
    result = model.predict(image_bgr, conf=conf, imgsz=imgsz, device="cpu", verbose=False)[0]

    objects = []
    keep = []
    only_l = {c.strip().lower() for c in only} if only else None
    for i, box in enumerate(result.boxes):
        name = model.names[int(box.cls)]
        if only_l and name.lower() not in only_l:
            continue
        keep.append(i)
        x1, y1, x2, y2 = (int(v) for v in box.xyxy[0].tolist())
        objects.append({
            "class": name,
            "class_ru": ru(name),
            "conf": round(float(box.conf), 3),
            "box": [x1, y1, x2, y2],
        })

    if not plot:
        return None, objects
    if only_l is not None:
        result = result[keep]
    annotated = result.plot()  # BGR с рамками и подписями
    return annotated, objects


def imread(path):
    """cv2.imread не понимает кириллицу в пути на Windows — читаем через numpy."""
    data = np.fromfile(str(path), dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR) if data.size else None


def imwrite(path, img):
    ok, buf = cv2.imencode(Path(path).suffix or ".jpg", img)
    if ok:
        buf.tofile(str(path))
    return ok


def detect_file(path, out_dir=None, **kw):
    img = imread(path)
    if img is None:
        raise ValueError(f"Не удалось прочитать изображение: {path}")
    annotated, objects = detect(img, **kw)
    if out_dir:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        imwrite(out_dir / Path(path).name, annotated)
    return annotated, objects
