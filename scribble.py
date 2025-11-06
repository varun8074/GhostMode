import sys
import keyboard
from PyQt5 import QtCore, QtGui, QtWidgets

class AlwaysOnTopOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Always on top, frameless, transparent window
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_StaticContents, True)
        self.setAttribute(QtCore.Qt.WA_PaintOnScreen, False)
        self.showFullScreen()

        # Persistent QPixmap for drawings
        self.canvas = QtGui.QPixmap(self.size())
        self.canvas.fill(QtCore.Qt.transparent)

        # Drawing parameters
        self.last_point = None
        self.drawing = False
        self.drawing_enabled = False
        self.pen_color = QtGui.QColor(33, 43, 53)
        self.pen_width = 4

        # Keyboard hotkeys
        keyboard.add_hotkey("f8", self.toggle_drawing)
        keyboard.add_hotkey("c", self.clear_canvas)
        keyboard.add_hotkey("esc", self.close)

        print("✅ Overlay active")
        print("Press F8 to toggle draw/click-through, C to clear, Esc to exit.")

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

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        # Fill slight tint for visibility
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 10))
        painter.drawPixmap(0, 0, self.canvas)

    def mousePressEvent(self, event):
        if self.drawing_enabled and event.button() == QtCore.Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing and (event.buttons() & QtCore.Qt.LeftButton):
            painter = QtGui.QPainter(self.canvas)
            pen = QtGui.QPen(self.pen_color, self.pen_width, QtCore.Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drawing = False

    # Prevent losing drawings on focus or minimize
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            self.showFullScreen()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    overlay = AlwaysOnTopOverlay()
    overlay.show()
    sys.exit(app.exec_())
