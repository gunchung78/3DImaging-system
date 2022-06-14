import cv2
import sys
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from FPeplography_optim import FPE


class ShowVideo(QtCore.QObject):
    flag = 0
    camera = cv2.VideoCapture(0)
    ret, image = camera.read()
    height, width = image.shape[:2]
    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        global image
        run_video = True
        while run_video:
            ret, image = self.camera.read()
            Video_Img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if self.flag == 1:
                Video_Img = FPE(Video_Img)
                Video_Img = cv2.normalize(Video_Img, None, 
                                                    alpha = 0, 
                                                    beta = 255, 
                                                    norm_type = cv2.NORM_MINMAX, 
                                                    dtype = cv2.CV_32F)
                Video_Img = Video_Img.astype(np.uint8)
            
            qt_image1 = QtGui.QImage(Video_Img.data,
                                    self.width,
                                    self.height,
                                    Video_Img.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal.emit(qt_image1)
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()

    @QtCore.pyqtSlot()
    def canny(self):
        self.flag = 1 - self.flag


class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('3Dimaging-System Project')
        
    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)
    image_viewer = ImageViewer()
    
    vid.VideoSignal.connect(image_viewer.setImage)
    push_button1 = QtWidgets.QPushButton('Start')
    push_button2 = QtWidgets.QPushButton('Canny')
    push_button1.clicked.connect(vid.startVideo)
    push_button2.clicked.connect(vid.canny)
    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    horizontal_layout.addWidget(image_viewer)
    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(push_button1)
    vertical_layout.addWidget(push_button2)
    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)
    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())