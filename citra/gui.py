import os
import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QErrorMessage, QMessageBox
from PyQt5.QtGui import QPixmap
from citra_lsb import CitraLSB

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('citra.ui', self)

        self.img_encode_path = ''
        self.msg_encode_path = ''
        self.imgEncodeButton.clicked.connect(self.load_image_encode)
        self.messageButton.clicked.connect(self.load_message_encode)
        # self.inputFileEncode.clicked.connect(self.load_image_encode)
        self.startEncode.clicked.connect(self.encode)

    def load_image_encode(self):
        dialog = QFileDialog()

        fname = dialog.getOpenFileName(None, "Window name", "", "Image (*.bmp *.png)")
        self.img_encode_path = fname[0]
        self.inputFileEncode.setText(self.img_encode_path)
        # show msg
        pix = QPixmap(self.img_encode_path)
        pix.scaledToHeight(10)
        item = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene(self)
        scene.addItem(item)
        self.imagePreview.setScene(scene)
    
    def load_message_encode(self):
        dialog = QFileDialog()
        fname = dialog.getOpenFileName(None, "Window name", "", "Image (*.*)")
        self.msg_encode_path = fname[0]
        self.inputFileMessage.setText(self.msg_encode_path)
         
    def encode(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Input Salah!")
        msg.setInformativeText("Jika memilih enkripsi, key tidak boleh kosong")
        # msg.setWindowTitle("MessageBox demo")
        # msg.setDetailedText("The details are as follows:")
        msg.exec_()
        print("encoding...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())