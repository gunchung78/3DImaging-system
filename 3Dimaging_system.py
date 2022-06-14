from cProfile import label
import cv2
import sys
import numpy as np
import timeit
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QAction, qApp, QInputDialog
from PyQt5.QtCore import Qt
from FPeplography_optim import FPE
from Night_Vision import photon

global NV_n 
global NV_np

NV_n = 8
NV_np = 100000


class ShowVideo(QtCore.QObject):

    flag_FPE = 0
    flag_PH = 0
    camera = cv2.VideoCapture(0)
    cnt=0
    frames_to_count = 0
    st = 0
    fps = 0

    ret, image = camera.read()
    height, width = image.shape[:2]

    Video_Img = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)
        self.label1 = 0

    @QtCore.pyqtSlot()
    def startVideo(self):
        global image
        run_video = True
        while run_video:
            start_t = timeit.default_timer()
            ret, image = self.camera.read()
            Video_Img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if self.flag_FPE or self.flag_PH == 0: self.label1.setText("Originl")
            
            if self.flag_FPE == 1:
                self.label1.setText("Peplography")
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
            if self.flag_PH == 1:
                self.label1.setText("Night Vision " + "N: " + str(NV_n) + " Np: " + str(NV_np))
                Video_Img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                Video_Img = photon(Video_Img, NV_n, NV_np, 0)
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
                                    QtGui.QImage.Format_Grayscale8)
            else:
                qt_image1 = QtGui.QImage(Video_Img.data,
                                    self.width,
                                    self.height,
                                    Video_Img.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.Video_Img.emit(qt_image1)
            terminate_t = timeit.default_timer()
            FPS = int(1./(terminate_t - start_t ))
            print(FPS)  
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()

    @QtCore.pyqtSlot()
    def FPE_Action(self):
        self.flag_FPE = 1 - self.flag_FPE
        if self.flag_FPE and self.flag_PH == 1: self.flag_PH = 0

    def PH_Action(self):
        self.flag_PH = 1 - self.flag_PH 
        if self.flag_FPE and self.flag_PH == 1: self.flag_FPE = 0 


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
        self.setWindowTitle('3Dimaging_system')

    def showDialog(self):
        text1, ok = QInputDialog.getText(self, 'Night Vision', 'Enter number of N:')
        text2, ok = QInputDialog.getText(self, 'Night Vision', 'Enter number of Np:')
        if ok:
            NV_n = text1
            NV_np = text2

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

    vid.Video_Img.connect(image_viewer.setImage)
    vid.label1 = QtWidgets.QLabel('No Camara...')
    font1 = vid.label1.font()
    vid.label1.setAlignment(Qt.AlignCenter)
    font1.setPointSize(11)
    vid.label1.setFont(font1)

    push_button1 = QtWidgets.QPushButton('Start')
    push_button1.clicked.connect(vid.startVideo)
    

    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    horizontal_layout.addWidget(image_viewer)
    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(vid.label1)
    vertical_layout.addWidget(push_button1)


    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)
    main_window = QtWidgets.QMainWindow()
    main_window.setGeometry(200, 200, 400, 200)           
    
    exitAction = QAction('&Exit')        
    exitAction.setShortcut('Ctrl+Q')
    exitAction.setStatusTip('Exit application')
    exitAction.triggered.connect(qApp.quit)

    FPEAction = QAction('&FPE')        
    FPEAction.setShortcut('Ctrl+1')
    FPEAction.setStatusTip('FPeplography')
    FPEAction.triggered.connect(vid.FPE_Action)

    PHAction = QAction('&PH')        
    PHAction.setShortcut('Ctrl+2')
    PHAction.setStatusTip('not ready')
    PHAction.triggered.connect(vid.PH_Action)

    PHchAction = QAction('&PHch')        
    PHchAction.setShortcut('Ctrl+3')
    PHchAction.setStatusTip('not ready')
    PHchAction.triggered.connect(image_viewer.showDialog)

    main_window.setWindowTitle('3Dimaging_system')
    main_window.statusBar()
    menubar = main_window.menuBar()
    fileMenu = menubar.addMenu('&File')
    fileMenu.addAction(exitAction)

    EditMenu = menubar.addMenu('&Edit')
    EditMenu.addAction(FPEAction)
    EditMenu.addAction(PHAction)
    EditMenu.addAction(PHchAction)
    
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())