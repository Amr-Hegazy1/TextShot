import sys
from PyQt5 import QtWidgets, QtCore,QtGui
import pyscreenshot as ImageGrab
import pytesseract
import pyperclip
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30,30,600,400)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(255, 255, 255, 100))
        qp.setBrush(br)
        qp.drawRect(QtCore.QRect(self.begin, self.end))


    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

        self.x1 = int(self.begin.x())
        self.y1 = int(self.begin.y())

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()
        self.x2 = int(self.end.x())
        self.y2 = int(self.end.y())
        # QtWidgets.QApplication.quit()
        im = ImageGrab.grab(bbox=(self.x1, self.y1, self.x2, self.y2))
        im.save('screenshot.png')
        result = pytesseract.image_to_string(Image.open('screenshot.png'), timeout=2, lang='eng')
        pyperclip.copy(result)
        print(result)





app = QtWidgets.QApplication(sys.argv)
window = MyWidget()
window.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Dialog)
window.setStyleSheet('background-color: black')
window.showMaximized()
window.setWindowOpacity(0.5)
window.setWindowTitle('Image to Text')
window.show()
result = pytesseract.image_to_string(Image.open('screenshot.png'),timeout=2,lang='eng')
# pyperclip.copy(result)
print(result)
#app.aboutToQuit.connect(app.deleteLater)
sys.exit(app.exec_())