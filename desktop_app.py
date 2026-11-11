"""Десктопное приложение: распознавание объектов на фото (PySide6 / Qt)."""
import ctypes
import queue
import sys
import threading
import time
from pathlib import Path

import cv2
import numpy as np
from PySide6.QtCore import QObject, QPoint, QPointF, QRect, QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import (QColor, QFont, QFontMetrics, QGuiApplication, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPainterPath, QPen, QPixmap, QShortcut)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFileDialog, QFrame, QHBoxLayout, QLabel, QLayout,
                               QMainWindow, QMessageBox, QPushButton, QScrollArea, QSizePolicy, QSlider, QVBoxLayout,
                               QWidget)

from detector import ROOT, detect, imread, imwrite, load_model

# ---------- палитра ----------
BG = "#141414"
SURFACE = "#1b1b1b"
RAISED = "#252525"
LINE = "#2e2e2e"
TEXT = "#ece9e4"
MUTED = "#8b8781"
ACCENT = "#e8b04b"
# приглушённые цвета классов — различимы, но не кислотные
CLASS_COLORS = ["#e8b04b", "#7fb8a8", "#d68a7c", "#8fa8d6", "#b89ad6", "#a3c47f",
                "#d68fb3", "#6fb6cf", "#c9a27e", "#b0aca6"]

MIN_CONF = 0.05          # модель запускается один раз с низким порогом,
DEFAULT_THRESHOLD = 25   # а ползунок фильтрует результат мгновенно
MODELS = [("Open Images", "oiv7"), ("COCO", "coco")]
IMG_FILTER = "Изображения (*.jpg *.jpeg *.png *.bmp *.webp)"


def plural(n, one, few, many):
    n10, n100 = n % 10, n % 100
    if n10 == 1 and n100 != 11:
        return one
    if 2 <= n10 <= 4 and not 12 <= n100 <= 14:
        return few
    return many


def bgr_to_qimage(bgr):
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]
    return QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888).copy()


def qimage_to_bgr(img: QImage):
    img = img.convertToFormat(QImage.Format_RGB888)
    w, h, bpl = img.width(), img.height(), img.bytesPerLine()
    arr = np.frombuffer(img.constBits(), np.uint8).reshape(h, bpl)[:, : w * 3].reshape(h, w, 3)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def make_thumb(bgr, box, size=96):
    """Квадратная миниатюра объекта с небольшим запасом вокруг рамки."""
    h, w = bgr.shape[:2]
    x1, y1, x2, y2 = box
    side = max(x2 - x1, y2 - y1) * 1.15
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    a, b = int(max(0, cx - side / 2)), int(max(0, cy - side / 2))
    c, d = int(min(w, cx + side / 2)), int(min(h, cy + side / 2))
    crop = bgr[b:d, a:c]
    if crop.size == 0:
        crop = bgr
    ch, cw = crop.shape[:2]
    s = max(ch, cw)
    canvas = np.full((s, s, 3), 27, np.uint8)
    canvas[(s - ch) // 2:(s - ch) // 2 + ch, (s - cw) // 2:(s - cw) // 2 + cw] = crop
    canvas = cv2.resize(canvas, (size, size), interpolation=cv2.INTER_AREA)
    return QPixmap.fromImage(bgr_to_qimage(canvas))


def paint_overlay(p: QPainter, objs, idxs, colors, to_rect, focus=None, s=1.0, clip=None):
    """Рамки-видоискатели и подписи. Используется и в окне, и при сохранении файла."""
    p.setRenderHint(QPainter.Antialiasing)
    if focus is not None and clip is not None:
        outside = QPainterPath()
        outside.addRect(clip)
        hole = QPainterPath()
        hole.addRoundedRect(to_rect(objs[focus]["box"]), 3 * s, 3 * s)
        p.fillPath(outside.subtracted(hole), QColor(0, 0, 0, 150))

    font = QFont("Segoe UI Variable Text", 9)
    font.setPixelSize(max(11, int(12 * s)))
    font.setWeight(QFont.DemiBold)
    p.setFont(font)
    fm = QFontMetrics(font)
    placed = []  # уже нарисованные подписи — чтобы не налезали друг на друга

    for i in idxs:
        o = objs[i]
        r = to_rect(o["box"])
        col = QColor(colors[o["class"]])
        faded = focus is not None and i != focus

        thin = QColor(col)
        thin.setAlpha(35 if faded else 110)
        p.setPen(QPen(thin, 1 * s))
        p.setBrush(Qt.NoBrush)
        p.drawRect(r)
        if faded:
            continue

        # уголки
        L = min(18 * s, r.width() / 3, r.height() / 3)
        pen = QPen(col, (3 if i == focus else 2.2) * s)
        pen.setCapStyle(Qt.SquareCap)
        p.setPen(pen)
        for cx, cy, dx, dy in ((r.left(), r.top(), 1, 1), (r.right(), r.top(), -1, 1),
                               (r.left(), r.bottom(), 1, -1), (r.right(), r.bottom(), -1, -1)):
            p.drawLine(QPointF(cx, cy), QPointF(cx + dx * L, cy))
            p.drawLine(QPointF(cx, cy), QPointF(cx, cy + dy * L))

        # подпись
        text = o["class_ru"] + (f"  {o['conf']:.2f}" if i == focus or focus is None and s > 1 else "")
        tw, th = fm.horizontalAdvance(text) + 12 * s, fm.height() + 4 * s
        top = r.top() - th - 4 * s
        if clip is not None and top < clip.top():
            top = r.top() + 4 * s
        pill = QRectF(r.left(), top, tw, th)
        if i != focus and any(pill.intersects(q) for q in placed):
            continue  # объекты идут по убыванию уверенности — подпись получает более уверенный
        placed.append(pill.adjusted(-2, -2, 2, 2))
        p.setPen(Qt.NoPen)
        p.setBrush(col)
        p.drawRoundedRect(pill, th / 2, th / 2)
        p.setPen(QColor(BG))
        p.drawText(pill, Qt.AlignCenter, text)


# ---------- фоновый поток для модели ----------
class Worker(QObject):
    finished = Signal(object, object, object)  # callback, result, error

    def __init__(self):
        super().__init__()
        self.tasks = queue.Queue()
        self.finished.connect(lambda cb, r, e: cb(r, e))
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while True:
            fn, args, cb = self.tasks.get()
            try:
                res, err = fn(*args), None
            except Exception as e:  # noqa: BLE001
                res, err = None, e
            self.finished.emit(cb, res, err)

    def submit(self, fn, args, cb):
        self.tasks.put((fn, args, cb))


# ---------- область просмотра ----------
class ImageView(QWidget):
    hoverChanged = Signal(object)
    clicked = Signal(object)

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setMinimumSize(400, 300)
        self.pix = None
        self.objs, self.idxs, self.colors = [], [], {}
        self.hovered = self.selected = None
        self.drag_over = False
        self.busy = False
        self._phase = 0.0
        self._timer = QTimer(self, interval=16, timeout=self._tick)

    def set_image(self, qimg):
        self.pix = QPixmap.fromImage(qimg) if qimg is not None else None
        self.objs, self.idxs = [], []
        self.hovered = self.selected = None
        self.update()

    def set_objects(self, objs, idxs, colors):
        self.objs, self.idxs, self.colors = objs, idxs, colors
        if self.selected not in idxs:
            self.selected = None
        if self.hovered not in idxs:
            self.hovered = None
        self.update()

    def set_busy(self, busy):
        self.busy = busy
        self._timer.start() if busy else self._timer.stop()
        self.update()

    def _tick(self):
        self._phase = (self._phase + 0.012) % 2.0
        self.update()

    # геометрия
    def _img_rect(self):
        m = 28
        aw, ah = self.width() - 2 * m, self.height() - 2 * m
        pw, ph = self.pix.width(), self.pix.height()
        k = min(aw / pw, ah / ph, 1.0) if not (aw < 1 or ah < 1) else 1.0
        w, h = pw * k, ph * k
        return QRectF((self.width() - w) / 2, (self.height() - h) / 2, w, h), k

    def _to_view(self, box):
        r, k = self._img_rect()
        x1, y1, x2, y2 = box
        return QRectF(r.left() + x1 * k, r.top() + y1 * k, (x2 - x1) * k, (y2 - y1) * k)

    def _hit(self, pos):
        best, area = None, float("inf")
        for i in self.idxs:
            r = self._to_view(self.objs[i]["box"])
            if r.contains(pos) and r.width() * r.height() < area:
                best, area = i, r.width() * r.height()
        return best

    # события
    def mouseMoveEvent(self, e):
        if self.pix is None:
            return
        h = self._hit(e.position())
        if h != self.hovered:
            self.hovered = h
            self.setCursor(Qt.PointingHandCursor if h is not None else Qt.ArrowCursor)
            self.hoverChanged.emit(h)
            self.update()

    def leaveEvent(self, e):
        if self.hovered is not None:
            self.hovered = None
            self.hoverChanged.emit(None)
            self.update()

    def mousePressEvent(self, e):
        if self.pix is None:
            self.clicked.emit("open")
            return
        h = self._hit(e.position())
        self.selected = None if h == self.selected else h
        self.clicked.emit(self.selected)
        self.update()

    def focus(self):
        return self.hovered if self.hovered is not None else self.selected

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.fillRect(self.rect(), QColor(BG))

        if self.pix is None:
            self._paint_empty(p)
            return

        r, _ = self._img_rect()
        p.drawPixmap(r, self.pix, QRectF(self.pix.rect()))
        paint_overlay(p, self.objs, self.idxs, self.colors, self._to_view, self.focus(), 1.0, r)

        if self.busy:
            # линия сканирования ходит вверх-вниз, за ней тянется мягкий шлейф
            down = self._phase <= 1
            t = self._phase if down else 2 - self._phase
            y = r.top() + t * r.height()
            tail = y - 60 if down else y + 60
            g = QLinearGradient(0, tail, 0, y)
            c0, c1 = QColor(ACCENT), QColor(ACCENT)
            c0.setAlpha(0)
            c1.setAlpha(40)
            g.setColorAt(0, c0)
            g.setColorAt(1, c1)
            band = QRectF(r.left(), min(y, tail), r.width(), 60).intersected(r)
            p.fillRect(band, g)
            p.setPen(QPen(QColor(ACCENT), 1))
            p.drawLine(QPointF(r.left(), y), QPointF(r.right(), y))
        if self.drag_over:
            p.setPen(QPen(QColor(ACCENT), 2))
            p.setBrush(Qt.NoBrush)
            p.drawRoundedRect(QRectF(self.rect()).adjusted(10, 10, -10, -10), 14, 14)

    def _paint_empty(self, p):
        box = QRectF(0, 0, 440, 230)
        box.moveCenter(QPointF(self.rect().center()))
        pen = QPen(QColor(ACCENT if self.drag_over else "#3a3a3a"), 1.5, Qt.DashLine)
        pen.setDashPattern([5, 5])
        p.setPen(pen)
        p.setBrush(QColor(SURFACE) if not self.drag_over else QColor(30, 27, 20))
        p.drawRoundedRect(box, 16, 16)

        # рамка-видоискатель как иконка
        ic = QRectF(0, 0, 44, 34)
        ic.moveCenter(QPointF(box.center().x(), box.top() + 70))
        p.setPen(QPen(QColor(ACCENT), 2.2, Qt.SolidLine, Qt.SquareCap))
        L = 10
        for cx, cy, dx, dy in ((ic.left(), ic.top(), 1, 1), (ic.right(), ic.top(), -1, 1),
                               (ic.left(), ic.bottom(), 1, -1), (ic.right(), ic.bottom(), -1, -1)):
            p.drawLine(QPointF(cx, cy), QPointF(cx + dx * L, cy))
            p.drawLine(QPointF(cx, cy), QPointF(cx, cy + dy * L))

        f = QFont("Segoe UI Variable Display", 13)
        f.setWeight(QFont.DemiBold)
        p.setFont(f)
        p.setPen(QColor(TEXT))
        p.drawText(QRectF(box.left(), box.top() + 112, box.width(), 30), Qt.AlignCenter,
                   "Перетащите фото сюда")
        p.setFont(QFont("Segoe UI Variable Text", 10))
        p.setPen(QColor(MUTED))
        p.drawText(QRectF(box.left(), box.top() + 146, box.width(), 24), Qt.AlignCenter,
                   "или нажмите, чтобы выбрать  ·  Ctrl+V — из буфера")


# ---------- элементы правой панели ----------
class Chip(QWidget):
    toggled = Signal(str, bool)

    def __init__(self, key, text, count, color, on=True):
        super().__init__()
        self.key, self.text, self.count, self.color, self.on = key, text, count, color, on
        self.hover = False
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("Segoe UI Variable Text", 9))
        fm = QFontMetrics(self.font())
        w = 12 + 8 + 8 + fm.horizontalAdvance(text) + 8 + fm.horizontalAdvance(str(count)) + 12
        self.setFixedSize(w, 28)

    def enterEvent(self, e):
        self.hover = True
        self.update()

    def leaveEvent(self, e):
        self.hover = False
        self.update()

    def mousePressEvent(self, e):
        self.on = not self.on
        self.update()
        self.toggled.emit(self.key, self.on)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        p.setPen(QPen(QColor("#3a3a3a" if self.hover else LINE), 1))
        p.setBrush(QColor(RAISED) if self.on else Qt.NoBrush)
        p.drawRoundedRect(r, 14, 14)
        col = QColor(self.color)
        if self.on:
            p.setPen(Qt.NoPen)
            p.setBrush(col)
        else:
            p.setPen(QPen(col, 1.2))
            p.setBrush(Qt.NoBrush)
        p.drawEllipse(QPointF(16, 14), 4, 4)
        fm = QFontMetrics(self.font())
        f = QFont(self.font())
        f.setStrikeOut(not self.on)
        p.setFont(f)
        p.setPen(QColor(TEXT if self.on else "#66625d"))
        p.drawText(QRectF(28, 0, 400, 28), Qt.AlignVCenter | Qt.AlignLeft, self.text)
        p.setFont(self.font())
        p.setPen(QColor(MUTED if self.on else "#4f4c48"))
        p.drawText(QRectF(28 + fm.horizontalAdvance(self.text) + 8, 0, 100, 28),
                   Qt.AlignVCenter | Qt.AlignLeft, str(self.count))


class ObjectCard(QWidget):
    hovered = Signal(object)
    clicked = Signal(int)

    def __init__(self, idx, obj, thumb, color):
        super().__init__()
        self.idx, self.obj, self.thumb, self.color = idx, obj, thumb, color
        self.hover = self.selected = self.linked = False
        self.setFixedHeight(64)
        self.setCursor(Qt.PointingHandCursor)

    def enterEvent(self, e):
        self.hover = True
        self.hovered.emit(self.idx)
        self.update()

    def leaveEvent(self, e):
        self.hover = False
        self.hovered.emit(None)
        self.update()

    def mousePressEvent(self, e):
        self.clicked.emit(self.idx)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        r = QRectF(self.rect()).adjusted(0, 2, 0, -2)
        if self.hover or self.linked or self.selected:
            p.setPen(QPen(QColor(self.color), 1) if self.selected else Qt.NoPen)
            p.setBrush(QColor(RAISED))
            p.drawRoundedRect(r.adjusted(0.5, 0.5, -0.5, -0.5), 10, 10)

        tr = QRectF(10, r.top() + 6, 48, 48)
        clip = QPainterPath()
        clip.addRoundedRect(tr, 8, 8)
        p.save()
        p.setClipPath(clip)
        p.drawPixmap(tr, self.thumb, QRectF(self.thumb.rect()))
        p.restore()
        p.setPen(QPen(QColor(self.color), 1.5))
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(tr, 8, 8)

        conf = self.obj["conf"]
        right = self.width() - 14
        f = QFont("Segoe UI Variable Text", 10)
        f.setWeight(QFont.DemiBold)
        p.setFont(f)
        p.setPen(QColor(TEXT))
        p.drawText(QRectF(70, r.top() + 10, right - 70 - 60, 22), Qt.AlignLeft | Qt.AlignVCenter,
                   self.obj["class_ru"])
        p.setFont(QFont("Segoe UI Variable Text", 9))
        p.setPen(QColor(MUTED))
        x1, y1, x2, y2 = self.obj["box"]
        p.drawText(QRectF(70, r.top() + 32, right - 70 - 60, 18), Qt.AlignLeft | Qt.AlignVCenter,
                   f"{x2 - x1}×{y2 - y1} px")

        # уверенность: число и тонкая шкала
        p.setPen(QColor(TEXT))
        p.drawText(QRectF(right - 52, r.top() + 10, 52, 22), Qt.AlignRight | Qt.AlignVCenter, f"{conf:.2f}")
        bar = QRectF(right - 52, r.top() + 38, 52, 3)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(LINE))
        p.drawRoundedRect(bar, 1.5, 1.5)
        p.setBrush(QColor(self.color))
        p.drawRoundedRect(QRectF(bar.left(), bar.top(), bar.width() * conf, bar.height()), 1.5, 1.5)


class FlowLayout(QLayout):
    def __init__(self, parent=None, spacing=6):
        super().__init__(parent)
        self.items = []
        self.setSpacing(spacing)
        self.setContentsMargins(0, 0, 0, 0)

    def addItem(self, item):
        self.items.append(item)

    def count(self):
        return len(self.items)

    def itemAt(self, i):
        return self.items[i] if 0 <= i < len(self.items) else None

    def takeAt(self, i):
        return self.items.pop(i) if 0 <= i < len(self.items) else None

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, w):
        return self._do(QRect(0, 0, w, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        s = QSize()
        for it in self.items:
            s = s.expandedTo(it.minimumSize())
        return s

    def _do(self, rect, test):
        x, y, line_h, sp = rect.x(), rect.y(), 0, self.spacing()
        for it in self.items:
            w, h = it.sizeHint().width(), it.sizeHint().height()
            if x + w > rect.right() + 1 and line_h > 0:
                x, y, line_h = rect.x(), y + line_h + sp, 0
            if not test:
                it.setGeometry(QRect(QPoint(x, y), it.sizeHint()))
            x += w + sp
            line_h = max(line_h, h)
        return y + line_h - rect.y()


def clear_layout(layout):
    while layout.count():
        it = layout.takeAt(0)
        if it.widget():
            it.widget().deleteLater()


# ---------- главное окно ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Распознавание")
        self.resize(1360, 860)
        self.setMinimumSize(1000, 640)
        self.setAcceptDrops(True)

        self.worker = Worker()
        self.bgr = None
        self.path = None
        self.objs, self.thumbs, self.colors = [], [], {}
        self.hidden = set()
        self.cards = {}
        self.busy = False
        self.pending = False
        self.last_ms = 0

        root = QWidget(objectName="root")
        self.setCentralWidget(root)
        v = QVBoxLayout(root)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)
        v.addWidget(self._topbar())
        body = QHBoxLayout()
        body.setSpacing(0)
        v.addLayout(body, 1)

        center = QVBoxLayout()
        center.setSpacing(0)
        self.view = ImageView()
        self.view.hoverChanged.connect(self._on_view_hover)
        self.view.clicked.connect(self._on_view_click)
        center.addWidget(self.view, 1)
        center.addWidget(self._bottombar())
        body.addLayout(center, 1)
        body.addWidget(self._panel())

        for key, fn in ((QKeySequence.Open, self.open_dialog), (QKeySequence.Save, self.save_result),
                        (QKeySequence.Paste, self.paste),
                        (QKeySequence(Qt.Key_Escape), lambda: self._on_view_click(None, from_view=False))):
            QShortcut(key, self).activated.connect(fn)

        self._status("Загружаю модель…")
        self.worker.submit(load_model, ("oiv7",), lambda r, e: self._status(
            f"Ошибка модели: {e}" if e else "Готово"))
        self._refresh()

    # --- построение интерфейса ---
    def _topbar(self):
        bar = QFrame(objectName="topbar")
        bar.setFixedHeight(56)
        h = QHBoxLayout(bar)
        h.setContentsMargins(20, 0, 16, 0)
        h.setSpacing(10)

        title = QLabel("Распознавание", objectName="title")
        self.file_label = QLabel("", objectName="muted")
        h.addWidget(title)
        h.addWidget(self.file_label)
        h.addStretch(1)

        seg = QFrame(objectName="segment")
        seg.setFixedHeight(36)
        sh = QHBoxLayout(seg)
        sh.setContentsMargins(3, 3, 3, 3)
        sh.setSpacing(2)
        self.model_group = QButtonGroup(self)
        for i, (name, key) in enumerate(MODELS):
            b = QPushButton(name, objectName="seg", checkable=True)
            b.setCursor(Qt.PointingHandCursor)
            b.setProperty("key", key)
            b.setChecked(i == 0)
            self.model_group.addButton(b)
            sh.addWidget(b)
        self.model_group.buttonClicked.connect(lambda _: self.run_detect())
        h.addWidget(seg)
        h.addStretch(1)

        open_btn = QPushButton("Открыть", objectName="ghost")
        open_btn.setCursor(Qt.PointingHandCursor)
        open_btn.clicked.connect(self.open_dialog)
        self.save_btn = QPushButton("Сохранить", objectName="primary")
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_result)
        h.addWidget(open_btn)
        h.addWidget(self.save_btn)
        return bar

    def _bottombar(self):
        bar = QFrame(objectName="bottombar")
        bar.setFixedHeight(48)
        h = QHBoxLayout(bar)
        h.setContentsMargins(28, 0, 28, 0)
        h.setSpacing(12)
        h.addWidget(QLabel("Порог", objectName="muted"))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(int(MIN_CONF * 100), 90)
        self.slider.setValue(DEFAULT_THRESHOLD)
        self.slider.setFixedWidth(200)
        self.slider.setCursor(Qt.PointingHandCursor)
        self.slider.valueChanged.connect(self._on_threshold)
        h.addWidget(self.slider)
        self.thr_label = QLabel(f"{DEFAULT_THRESHOLD / 100:.2f}", objectName="value")
        self.thr_label.setFixedWidth(36)
        h.addWidget(self.thr_label)
        h.addStretch(1)
        self.status_label = QLabel("", objectName="muted")
        h.addWidget(self.status_label)
        return bar

    def _panel(self):
        panel = QFrame(objectName="panel")
        panel.setFixedWidth(360)
        v = QVBoxLayout(panel)
        v.setContentsMargins(20, 20, 12, 12)
        v.setSpacing(0)

        head = QHBoxLayout()
        head.setSpacing(10)
        self.count_label = QLabel("0", objectName="count")
        self.count_word = QLabel("объектов", objectName="muted")
        head.addWidget(self.count_label, 0, Qt.AlignBottom)
        head.addWidget(self.count_word, 0, Qt.AlignBottom)
        head.addStretch(1)
        v.addLayout(head)
        v.addSpacing(16)

        self.chips_box = QWidget()
        self.chips = FlowLayout(self.chips_box)
        v.addWidget(self.chips_box)
        v.addSpacing(14)

        sep = QFrame(objectName="sep")
        sep.setFixedHeight(1)
        v.addWidget(sep)
        v.addSpacing(6)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        holder = QWidget(objectName="list")
        self.list = QVBoxLayout(holder)
        self.list.setContentsMargins(0, 0, 8, 0)
        self.list.setSpacing(0)
        self.list.addStretch(1)
        self.scroll.setWidget(holder)
        v.addWidget(self.scroll, 1)

        self.empty_hint = QLabel("Здесь появится список\nнайденных объектов", objectName="hint")
        self.empty_hint.setAlignment(Qt.AlignCenter)
        v.addWidget(self.empty_hint, 1)
        return panel

    # --- загрузка фото ---
    def open_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите фото", str(ROOT / "images"), IMG_FILTER)
        if path:
            self.load_path(path)

    def load_path(self, path):
        img = imread(path)
        if img is None:
            QMessageBox.warning(self, "Не удалось открыть", f"Файл не похож на изображение:\n{path}")
            return
        self.path = Path(path)
        self.set_image(img)

    def paste(self):
        cb = QGuiApplication.clipboard()
        md = cb.mimeData()
        if md.hasUrls() and md.urls()[0].isLocalFile():
            self.load_path(md.urls()[0].toLocalFile())
        elif md.hasImage():
            self.path = None
            self.set_image(qimage_to_bgr(cb.image()))
        else:
            self._status("В буфере нет изображения")

    def set_image(self, bgr):
        self.bgr = bgr
        self.objs, self.thumbs = [], []
        self.hidden.clear()
        self.file_label.setText(self.path.name if self.path else "из буфера")
        self.view.set_image(bgr_to_qimage(bgr))
        self._refresh()
        self.run_detect()

    # --- распознавание ---
    def model_key(self):
        return self.model_group.checkedButton().property("key")

    def run_detect(self):
        if self.bgr is None:
            return
        if self.busy:
            self.pending = True
            return
        self.busy = True
        self.view.set_busy(True)
        self._status("Распознаю…")
        bgr, key = self.bgr, self.model_key()

        def job():
            t = time.perf_counter()
            _, objs = detect(bgr, model_name=key, conf=MIN_CONF, plot=False)
            objs.sort(key=lambda o: -o["conf"])
            thumbs = [make_thumb(bgr, o["box"]) for o in objs]
            return objs, thumbs, (time.perf_counter() - t) * 1000

        self.worker.submit(job, (), self._on_detected)

    def _on_detected(self, res, err):
        self.busy = False
        if self.pending:
            self.pending = False
            self.run_detect()
            return
        self.view.set_busy(False)
        if err:
            self._status("Ошибка распознавания")
            QMessageBox.critical(self, "Ошибка", str(err))
            return
        self.objs, self.thumbs, self.last_ms = res
        # цвета по классам: самые частые получают первые цвета палитры
        counts = {}
        for o in self.objs:
            counts[o["class"]] = counts.get(o["class"], 0) + 1
        order = sorted(counts, key=lambda c: -counts[c])
        self.colors = {c: CLASS_COLORS[i % len(CLASS_COLORS)] for i, c in enumerate(order)}
        self._build_cards()
        self._refresh()
        self._status(f"{self.last_ms:.0f} мс")

    # --- фильтрация и отображение ---
    def threshold(self):
        return self.slider.value() / 100

    def _above(self):
        return [i for i, o in enumerate(self.objs) if o["conf"] >= self.threshold()]

    def _build_cards(self):
        clear_layout(self.list)
        self.cards = {}
        for i, o in enumerate(self.objs):
            card = ObjectCard(i, o, self.thumbs[i], self.colors[o["class"]])
            card.hovered.connect(self._on_card_hover)
            card.clicked.connect(self._on_card_click)
            self.cards[i] = card
            self.list.addWidget(card)
        self.list.addStretch(1)

    def _refresh(self):
        above = self._above()
        visible = [i for i in above if self.objs[i]["class"] not in self.hidden]

        for i, card in self.cards.items():
            card.setVisible(i in visible)
        self.view.set_objects(self.objs, visible, self.colors)

        n = len(visible)
        self.count_label.setText(str(n))
        self.count_word.setText(plural(n, "объект", "объекта", "объектов"))

        clear_layout(self.chips)
        counts, names = {}, {}
        for i in above:
            c = self.objs[i]["class"]
            counts[c] = counts.get(c, 0) + 1
            names[c] = self.objs[i]["class_ru"]
        for c in sorted(counts, key=lambda k: -counts[k]):
            chip = Chip(c, names[c], counts[c], self.colors[c], c not in self.hidden)
            chip.toggled.connect(self._on_chip)
            self.chips.addWidget(chip)
        self.chips_box.setVisible(bool(counts))

        has = self.bgr is not None and bool(self.objs)
        self.scroll.setVisible(has)
        self.empty_hint.setVisible(not has)
        if self.bgr is not None and not self.busy and self.objs and not above:
            self.empty_hint.setText("Ничего не найдено.\nПопробуйте понизить порог.")
        elif self.bgr is not None and not self.objs and not self.busy:
            self.empty_hint.setText("Ничего не найдено")
        else:
            self.empty_hint.setText("Здесь появится список\nнайденных объектов")
        if self.bgr is not None and self.objs and not above:
            self.scroll.setVisible(False)
            self.empty_hint.setVisible(True)
        self.save_btn.setEnabled(self.bgr is not None)

    def _on_threshold(self, v):
        self.thr_label.setText(f"{v / 100:.2f}")
        self._refresh()

    def _on_chip(self, key, on):
        (self.hidden.discard if on else self.hidden.add)(key)
        self._refresh()

    # --- связь списка и картинки ---
    def _on_view_hover(self, idx):
        for i, c in self.cards.items():
            linked = i == idx
            if c.linked != linked:
                c.linked = linked
                c.update()
        if idx is not None and idx in self.cards:
            self.scroll.ensureWidgetVisible(self.cards[idx], 0, 40)

    def _on_view_click(self, idx, from_view=True):
        if idx == "open":
            self.open_dialog()
            return
        if not from_view:
            self.view.selected = None
            self.view.update()
        for i, c in self.cards.items():
            c.selected = i == idx
            c.update()

    def _on_card_hover(self, idx):
        self.view.hovered = idx
        self.view.update()

    def _on_card_click(self, idx):
        self.view.selected = None if self.view.selected == idx else idx
        self.view.update()
        self._on_view_click(self.view.selected)

    # --- сохранение ---
    def save_result(self):
        if self.bgr is None:
            return
        name = f"{self.path.stem}_result.jpg" if self.path else "result.jpg"
        (ROOT / "results").mkdir(exist_ok=True)
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить результат", str(ROOT / "results" / name),
                                              "JPEG (*.jpg);;PNG (*.png)")
        if not path:
            return
        img = bgr_to_qimage(self.bgr).convertToFormat(QImage.Format_RGB32)
        s = max(1.0, img.width() / 900)
        p = QPainter(img)
        to_rect = lambda b: QRectF(b[0], b[1], b[2] - b[0], b[3] - b[1])  # noqa: E731
        paint_overlay(p, self.objs, self.view.idxs, self.colors, to_rect, None, s, QRectF(img.rect()))
        p.end()
        if imwrite(path, qimage_to_bgr(img)):
            self._status(f"Сохранено: {Path(path).name}")

    # --- перетаскивание файлов ---
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls() or e.mimeData().hasImage():
            e.acceptProposedAction()
            self.view.drag_over = True
            self.view.update()

    def dragLeaveEvent(self, e):
        self.view.drag_over = False
        self.view.update()

    def dropEvent(self, e):
        self.view.drag_over = False
        md = e.mimeData()
        if md.hasUrls() and md.urls()[0].isLocalFile():
            self.load_path(md.urls()[0].toLocalFile())
        elif md.hasImage():
            self.path = None
            self.set_image(qimage_to_bgr(QImage(md.imageData())))

    def _status(self, text):
        self.status_label.setText(text)


STYLE = f"""
QWidget#root {{ background: {BG}; }}
QFrame#topbar {{ background: {BG}; border-bottom: 1px solid {LINE}; }}
QFrame#bottombar {{ background: {BG}; }}
QFrame#panel {{ background: {SURFACE}; border-left: 1px solid {LINE}; }}
QFrame#sep {{ background: {LINE}; }}
QWidget#list {{ background: {SURFACE}; }}
QLabel {{ color: {TEXT}; font-size: 10pt; }}
QLabel#title {{ font-size: 11pt; font-weight: 600; }}
QLabel#muted {{ color: {MUTED}; }}
QLabel#value {{ color: {TEXT}; }}
QLabel#hint {{ color: {MUTED}; }}
QLabel#count {{ font-family: "Segoe UI Variable Display"; font-size: 30pt; font-weight: 300; }}
QPushButton {{ font-size: 10pt; }}
QPushButton#ghost {{ color: {TEXT}; background: transparent; border: 1px solid {LINE};
                     border-radius: 8px; padding: 6px 16px; }}
QPushButton#ghost:hover {{ background: {RAISED}; border-color: #3a3a3a; }}
QPushButton#primary {{ color: {BG}; background: {TEXT}; border: none; border-radius: 8px;
                       padding: 7px 16px; font-weight: 600; }}
QPushButton#primary:hover {{ background: #ffffff; }}
QPushButton#primary:disabled {{ background: {RAISED}; color: {MUTED}; }}
QFrame#segment {{ background: {SURFACE}; border: 1px solid {LINE}; border-radius: 10px; }}
QPushButton#seg {{ color: {MUTED}; background: transparent; border: none; border-radius: 7px;
                   padding: 5px 16px; }}
QPushButton#seg:hover {{ color: {TEXT}; }}
QPushButton#seg:checked {{ color: {TEXT}; background: {RAISED}; }}
QSlider::groove:horizontal {{ height: 2px; background: {LINE}; border-radius: 1px; }}
QSlider::sub-page:horizontal {{ height: 2px; background: {ACCENT}; border-radius: 1px; }}
QSlider::handle:horizontal {{ background: {TEXT}; width: 14px; height: 14px; margin: -6px 0;
                              border-radius: 7px; }}
QScrollArea {{ border: none; background: transparent; }}
QScrollArea > QWidget > QWidget {{ background: transparent; }}
QScrollBar:vertical {{ background: transparent; width: 6px; margin: 0; }}
QScrollBar::handle:vertical {{ background: #3a3a3a; border-radius: 3px; min-height: 30px; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
QToolTip {{ color: {TEXT}; background: {RAISED}; border: 1px solid {LINE}; }}
"""


def dark_title_bar(win):
    """Тёмная системная шапка окна в Windows 10/11."""
    try:
        hwnd = int(win.winId())
        dwm = ctypes.windll.dwmapi
        dwm.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(1)), 4)
        bg = QColor(BG)
        colorref = ctypes.c_int(bg.red() | bg.green() << 8 | bg.blue() << 16)
        dwm.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(colorref), 4)  # цвет шапки (Win11)
    except Exception:  # noqa: BLE001
        pass


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI Variable Text", 10))
    app.setStyleSheet(STYLE)
    win = MainWindow()
    dark_title_bar(win)
    win.show()
    if len(sys.argv) > 1:
        win.load_path(sys.argv[1])
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
