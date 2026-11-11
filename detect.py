"""
Распознавание из командной строки.

Примеры:
  python detect.py images\\photo.jpg
  python detect.py images                      # вся папка
  python detect.py images --model coco         # модель COCO (люди, машины)
  python detect.py images --only Pen Ruler Book --conf 0.15
"""
import argparse
import json
import time
from pathlib import Path

from detector import ROOT, detect_file

EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def main():
    p = argparse.ArgumentParser(description="Распознавание объектов на фото")
    p.add_argument("source", help="файл или папка с изображениями")
    p.add_argument("--model", choices=["oiv7", "coco"], default="oiv7")
    p.add_argument("--conf", type=float, default=0.25, help="порог уверенности 0..1")
    p.add_argument("--only", nargs="*", help="оставить только эти классы (англ.)")
    p.add_argument("--out", default=str(ROOT / "results"), help="куда сохранять результаты")
    a = p.parse_args()

    src = Path(a.source)
    files = sorted(f for f in src.iterdir() if f.suffix.lower() in EXT) if src.is_dir() else [src]
    if not files:
        print("Изображения не найдены.")
        return

    report = {}
    for f in files:
        t = time.perf_counter()
        _, objs = detect_file(f, out_dir=a.out, model_name=a.model, conf=a.conf, only=a.only)
        ms = (time.perf_counter() - t) * 1000
        print(f"\n{f.name}: найдено {len(objs)} ({ms:.0f} мс)")
        for o in sorted(objs, key=lambda o: -o["conf"]):
            print(f"  {o['class_ru']:<22} {o['conf']:.2f}  {o['box']}")
        report[f.name] = objs

    out = Path(a.out)
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nКартинки с рамками и report.json сохранены в: {out}")


if __name__ == "__main__":
    main()
