import sys
import keyboard
from PyQt5 import QtCore, QtGui, QtWidgets


class AlwaysOnTopOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Always-on-top, frameless, transparent window
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_StaticContents, True)
        self.setAttribute(QtCore.Qt.WA_PaintOnScreen, False)
        self.showFullScreen()

        # Canvas
        self.canvas = QtGui.QPixmap(self.size())
        self.canvas.fill(QtCore.Qt.transparent)

        # Drawing parameters
        self.last_point = None
        self.temp_line_end = None
        self.drawing = False
        self.drawing_enabled = False
        self.mode = "draw"  # draw, line, erase
        self.pen_color = QtGui.QColor(33, 43, 53)
        self.pen_width = 4

        # Hotkeys
        keyboard.add_hotkey("f8", self.toggle_drawing)
        keyboard.add_hotkey("c", self.clear_canvas)
        keyboard.add_hotkey("d", lambda: self.change_mode("draw"))
        keyboard.add_hotkey("l", lambda: self.change_mode("line"))
        keyboard.add_hotkey("e", lambda: self.change_mode("erase"))
        keyboard.add_hotkey("+", self.increase_thickness)
        keyboard.add_hotkey("-", self.decrease_thickness)
        keyboard.add_hotkey("esc", self.close)

        print("✅ Overlay active")
        print("Press F8 toggle draw/click-through")
        print("Modes: [D]raw, [L]ine, [E]rase, [C]lear, [+]/[-] Thickness, [Esc] Exit")

    # --- Mode Management ---
    def change_mode(self, mode):
        self.mode = mode
        print(f"✏️ Mode changed to: {mode.upper()}")

    def toggle_drawing(self):
        """Toggle drawing and click-through mode"""
        self.drawing_enabled = not self.drawing_enabled
        if self.drawing_enabled:
            print("🖊️ Drawing mode ON")
            self.setWindowFlag(QtCore.Qt.WindowTransparentForInput, False)
        else:
            print("🖱️ Click-through mode ON")
            self.setWindowFlag(QtCore.Qt.WindowTransparentForInput, True)
        self.show()

    def clear_canvas(self):
        self.canvas.fill(QtCore.Qt.transparent)
        self.update()
        print("🧹 Canvas cleared")

    # --- Thickness Adjustment ---
    def increase_thickness(self):
        self.pen_width = min(self.pen_width + 1, 50)
        print(f"⬆️ Thickness: {self.pen_width}px")

    def decrease_thickness(self):
        self.pen_width = max(self.pen_width - 1, 1)
        print(f"⬇️ Thickness: {self.pen_width}px")

    # --- Painting Events ---
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 10))  # Slight tint
        painter.drawPixmap(0, 0, self.canvas)

        # Line preview
        if self.mode == "line" and self.drawing and self.temp_line_end:
            preview_pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 150), self.pen_width, QtCore.Qt.DashLine)
            painter.setPen(preview_pen)
            painter.drawLine(self.last_point, self.temp_line_end)

    # --- Mouse Events ---
    def mousePressEvent(self, event):
        if self.drawing_enabled and event.button() == QtCore.Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            self.temp_line_end = None

    def mouseMoveEvent(self, event):
        if self.drawing_enabled and self.drawing:
            if self.mode == "draw":
                painter = QtGui.QPainter(self.canvas)
                pen = QtGui.QPen(self.pen_color, self.pen_width, QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(self.last_point, event.pos())
                self.last_point = event.pos()
                self.update()

            elif self.mode == "erase":
                painter = QtGui.QPainter(self.canvas)
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
                eraser_rect = QtCore.QRectF(
                    event.pos().x() - self.pen_width / 2,
                    event.pos().y() - self.pen_width / 2,
                    self.pen_width,
                    self.pen_width
                )
                painter.eraseRect(eraser_rect)
                self.last_point = event.pos()
                self.update()

            elif self.mode == "line":
                self.temp_line_end = event.pos()
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.drawing_enabled:
            if self.mode == "line" and self.last_point and self.temp_line_end:
                painter = QtGui.QPainter(self.canvas)
                pen = QtGui.QPen(self.pen_color, self.pen_width, QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(self.last_point, self.temp_line_end)
            self.drawing = False
            self.temp_line_end = None
            self.update()

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            self.showFullScreen()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    overlay = AlwaysOnTopOverlay()
    overlay.show()
    sys.exit(app.exec_())
