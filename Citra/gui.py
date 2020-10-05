import os
import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QErrorMessage, QMessageBox
from PyQt5.QtGui import QPixmap
from Citra.citra_lsb import CitraLSB
from Citra.citra_bpcs import CitraBPCS

class CitraUI(QMainWindow):
    def __init__(self):
        super(CitraUI, self).__init__()
        loadUi('citra.ui', self)

        self.img_encode_path = ''
        self.msg_encode_path = ''
        self.img_decode_path = ''
        self.imgEncodeButton.clicked.connect(self.load_image_encode)
        self.imgDecodeButton.clicked.connect(self.load_image_decode)
        self.messageButton.clicked.connect(self.load_message_encode)
        # self.inputFileEncode.clicked.connect(self.load_image_encode)
        self.startEncode.clicked.connect(self.encode)
        self.startDecode.clicked.connect(self.decode)

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

    def load_image_decode(self):
        dialog = QFileDialog()
        fname = dialog.getOpenFileName(None, "Window name", "", "Image (*.bmp *.png)")
        self.img_decode_path = fname[0]
        self.inputFileDecode.setText(self.img_decode_path)
        # show msg
        pix = QPixmap(self.img_decode_path)
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

        if (self.lsbEncode.isChecked()):
            print("lsb")
            if self.encryptedEncode.isChecked() or self.randomizedEncode.isChecked():
                if self.keyEncode.text() == '':
                    msg.setInformativeText("Masukkan kunci terlebih dahulu.")
                    msg.exec_()
                    return
            if self.img_msg_input_encode_validation():return

            #eksekusi LSB
            try:
                lsb = CitraLSB(self.img_encode_path)
                lsb.load_file_message(self.msg_encode_path)
                lsb.encode_lsb(key=self.keyEncode.text(),is_random=self.randomizedEncode.isChecked(), is_encrypted=self.encryptedEncode.isChecked())
                name = QFileDialog.getSaveFileName(self, 'Save File')
                lsb.save_stego_image(name[0])
                self.pnsr.setText(str(lsb.get_pnsr()))
            except Exception as e:
                self.show_error(str(e))
                return

        elif (self.bpcsEncode.isChecked()):
            if self.validate_treshold(self.tresholdEncode.text()):return
            if self.encryptedEncode.isChecked() or self.randomizedEncode.isChecked():
                if self.keyEncode.text() == '':
                    msg.setInformativeText("Masukkan kunci terlebih dahulu.")
                    msg.exec_()
                    return
            if self.img_msg_input_encode_validation():return
            
            #eksekusi BPCS
            try:
                bpcs = CitraBPCS(self.img_encode_path)
                bpcs.encode_bpcs(self.msg_encode_path, self.treshold, self.randomizedEncode.isChecked(), self.keyEncode.text(),self.encryptedEncode.isChecked())
                name = QFileDialog.getSaveFileName(self, 'Save File')
                bpcs.save_stego_image(name[0])
                self.pnsr.setText(str(bpcs.get_pnsr()))
            except Exception as e:
                self.show_error(str(e))
                return

        else:
            msg.setInformativeText("Pilih metode lsb/bpcs.")
            msg.exec_()
            return

    def decode(self):
        try:
            if (self.lsbDecode.isChecked()):
                if self.img_input_decode_validation():return
                lsb = CitraLSB(self.img_decode_path)
                name = QFileDialog.getSaveFileName(self, 'Save File')
                lsb.decode_lsb(name[0], self.keyDecode.text())
                
            elif self.bpcsDecode.isChecked():
                if self.img_input_decode_validation():return
                if self.validate_treshold(self.tresholdDecode.text()):return
                bpcs = CitraBPCS(self.img_decode_path)
                name = QFileDialog.getSaveFileName(self, 'Save File')
                bpcs.decode_bpcs(name[0], self.treshold, self.keyDecode.text())
                print("bpcs")
            else:
                self.warning_wrong_input("Pilih metode lsb/bpcs")
        except Exception as e:
            self.show_error(str(e), False)
            return

    def validate_treshold(self, obj):
        try:
            if (obj == ''):
                self.treshold = 0.3
            else:
                if (float(obj) < 1 and float(obj) > 0 ):
                    self.treshold = float(obj)
                else :
                    raise Exception()
        except:
            self.warning_wrong_input("Masukkan treshod yang valid.")
            return True
        return False

    def warning_wrong_input(self, msg):
        temp = msg
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Input Salah!")
        msg.setInformativeText(temp)
        msg.exec_()
    
    def img_input_decode_validation(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Input Salah!")
        if (self.img_decode_path == ''):
            msg.setInformativeText("Masukkan gambar yang akan diekstrak.")
            msg.exec_()
            return True
        return False

    def img_msg_input_encode_validation(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Input Salah!")
        if (self.img_encode_path == ''):
            msg.setInformativeText("Masukkan gambar yang akan disisipkan.")
            msg.exec_()
            return True
        elif (self.msg_encode_path == ''):
            msg.setInformativeText("Masukkan pesan yang akan disisipkan.")
            msg.exec_()
            return True
        return False

    def show_error(self, msg, sisip=True):
        cek = msg
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        if sisip:
            msg.setText("Gagal Sisipkan Pesan!")
        else:
            msg.setText("Gagal ekstrak Pesan!")
        msg.setInformativeText(cek)
        msg.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CitraUI()
    mainWindow.show()
    sys.exit(app.exec())