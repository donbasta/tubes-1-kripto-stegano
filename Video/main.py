from PyQt5 import QtWidgets, uic
import sys
import Video.FileReader as fr
from Video.FrameExtractor import FrameExtractor
from Video.VideoLSB import VideoLSB, VideoUnLSB
from Video.vigenere import Vigenere
import Video.utils
import os
import shutil
import cv2
import numpy as np


class VideoUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(VideoUI, self).__init__()
        uic.loadUi('video-stegano.ui', self)

        self.lineEditInputFile = self.findChild(
            QtWidgets.QLineEdit, 'lineEditInputFile')

        self.lineEditInputVideo = self.findChild(
            QtWidgets.QLineEdit, 'lineEditInputVideo')

        self.lineEditOutputVideo = self.findChild(
            QtWidgets.QLineEdit, 'lineEditOutputVideo')

        self.lineEditKey = self.findChild(QtWidgets.QLineEdit, 'lineEditKey')

        self.comboBoxStoringMode = self.findChild(
            QtWidgets.QComboBox, 'comboBoxStoringMode')

        self.radioEncryptionWith = self.findChild(
            QtWidgets.QRadioButton, 'radioEncryptionWith')

        self.radioEncryptionWithout = self.findChild(
            QtWidgets.QRadioButton, 'radioEncryptionWithout')

        self.radioModeRetrieve = self.findChild(
            QtWidgets.QRadioButton, 'radioModeRetrieve')

        self.radioModeStore = self.findChild(
            QtWidgets.QRadioButton, 'radioModeStore')

        self.modeRadioGroup = QtWidgets.QButtonGroup()
        self.modeRadioGroup.addButton(self.radioModeStore)
        self.modeRadioGroup.addButton(self.radioModeRetrieve)

        self.encryptionRadioGroup = QtWidgets.QButtonGroup()
        self.encryptionRadioGroup.addButton(self.radioEncryptionWith)
        self.encryptionRadioGroup.addButton(self.radioEncryptionWithout)

        self.buttonProcess = self.findChild(
            QtWidgets.QPushButton, 'buttonProcess')
        self.buttonProcess.clicked.connect(self.process)

        self.buttonFileInput = self.findChild(
            QtWidgets.QPushButton, 'buttonFileInput')
        self.buttonFileInput.clicked.connect(
            self.openInputFileDialog)

        self.buttonInputVideo = self.findChild(
            QtWidgets.QPushButton, 'buttonInputVideo')
        self.buttonInputVideo.clicked.connect(self.openInputVideoDialog)

        self.buttonOutputVideo = self.findChild(
            QtWidgets.QPushButton, 'buttonOutputVideo')
        self.buttonOutputVideo.clicked.connect(self.saveFileDialog)

        self.buttonGetMetadata = self.findChild(
            QtWidgets.QPushButton, 'buttonGetMetadata')
        self.buttonGetMetadata.clicked.connect(self.getMetadata)

        self.buttonOpenInput = self.findChild(
            QtWidgets.QPushButton, 'buttonOpenInput')
        self.buttonOpenFile = self.findChild(
            QtWidgets.QPushButton, 'buttonOpenFile')
        self.buttonOpenOutput = self.findChild(
            QtWidgets.QPushButton, 'buttonOpenOutput')
        self.buttonOpenInput.clicked.connect(self.openInput)
        self.buttonOpenFile.clicked.connect(self.openFile)
        self.buttonOpenOutput.clicked.connect(self.openOutput)

        self.buttonPSNR = self.findChild(
            QtWidgets.QPushButton, 'buttonPSNR')
        self.buttonPSNR.clicked.connect(self.PSNR)

        self.labelFrameCount = self.findChild(
            QtWidgets.QLabel, 'labelFrameCount')
        self.labelFilename = self.findChild(QtWidgets.QLabel, 'labelFilename')
        self.labelExt = self.findChild(QtWidgets.QLabel, 'labelExt')
        self.labelPSNR = self.findChild(QtWidgets.QLabel, 'labelPSNR')

        self.show()

    def getSelectedRadioButton(self, QButtonGroupObject: list):
        for item in QButtonGroupObject:
            if item.isChecked():
                return item.text()

    def PSNR(self):
        path1 = self.lineEditInputVideo.text()
        path2 = self.lineEditOutputVideo.text()
        if path1 != '' and path2 != '':
            vid1 = cv2.VideoCapture(path1)
            vid2 = cv2.VideoCapture(path2)
            framecounter = 1
            psnrList = []
            while(vid1.isOpened() and vid2.isOpened()):
                try:
                    stat1, img1 = vid1.read()
                    stat2, img2 = vid2.read()
                    if stat1 and stat2:
                        psnr = cv2.PSNR(img1, img2)
                        psnrList.append(psnr)
                        framecounter += 1
                    else:
                        break
                except cv2.error:
                    self.labelPSNR.setText("Error on calculating PSNR")
                    return
            meanPSNR = round(np.mean(psnrList), 2)
            self.labelPSNR.setText(str(meanPSNR))

    def openInput(self):
        path = self.lineEditInputVideo.text()
        if path != '':
            os.startfile(path)

    def openFile(self):
        path = self.lineEditInputFile.text()
        if path != '':
            os.startfile(path)

    def openOutput(self):
        path = self.lineEditOutputVideo.text()
        if path != '':
            os.startfile(path)

    def openInputFileDialog(self, target):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select File", "", "All Files (*)", options=options)
        if filename:
            print(filename)
            buttonFileInput = self.findChild(
                QtWidgets.QLineEdit, 'lineEditInputFile')
            buttonFileInput.setText(filename)

    def openInputVideoDialog(self, target):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select File", "", "All Files (*)", options=options)
        if filename:
            print(filename)
            buttonFileInput = self.findChild(
                QtWidgets.QLineEdit, 'lineEditInputVideo')
            buttonFileInput.setText(filename)

    def saveFileDialog(self, target):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Select File", "", "All Files (*)", options=options)
        if filename:
            print(filename)
            buttonFileInput = self.findChild(
                QtWidgets.QLineEdit, 'lineEditOutputVideo')
            buttonFileInput.setText(filename)

    def getMetadata(self):
        mode = self.modeRadioGroup.checkedButton().text()
        if mode.startswith("Retrieve"):
            unlsb = VideoUnLSB(self.lineEditInputVideo.text())
            framecount, mode_bit, filename, ext = unlsb.get_stego_metadata()
            self.labelFrameCount.setText(str(framecount))
            self.labelFilename.setText(str(filename))
            self.labelExt.setText(str(ext))
            self.retrievalModeBit = mode_bit

    def process(self):
        print("Process is called")
        storingMode = self.comboBoxStoringMode.currentText()
        mode = self.modeRadioGroup.checkedButton().text()
        encrypt = self.encryptionRadioGroup.checkedButton().text()
        key = self.lineEditKey.text()
        if storingMode.startswith("1.1"):
            storingMode = [0, 0]
        elif storingMode.startswith("1.2"):
            storingMode = [0, 1]
        elif storingMode.startswith("2.1"):
            storingMode = [1, 0]
        else:
            storingMode = [1, 1]

        seed = 0
        for e in key:
            seed += ord(e)

        if mode.startswith("Store"):
            if encrypt.startswith("With (Vi"):
                # perform encryption
                if os.path.exists('temp'):
                    shutil.rmtree("temp")
                # just do it
                # print(self.lineEditInputFile.text())
                filepath = self.lineEditInputFile.text()
                filename = os.path.basename(filepath)
                filename = filename.split('.')
                print(filename[0], filename[1])
                if not os.path.exists('temp'):
                    os.makedirs('temp')

                binary_file = fr.ReadFileAsByteArray(
                    self.lineEditInputFile.text())

                vig = Vigenere()
                vig.input_key(self.lineEditKey.text())
                vig.set_auto(False)
                vig.set_full(False)
                vig.set_extended(True)
                encrypted = vig.encrypt(''.join([chr(i) for i in binary_file]))
                binary_file = bytes(encrypted)

                extractor = FrameExtractor(
                    self.lineEditInputVideo.text(), "temp")
                extractor.load()
                extractor.extract()
                print("Extracting done")
                lsb = VideoLSB(self.lineEditInputVideo.text(),
                               binary_file, self.lineEditOutputVideo.text(), storingMode)
                lsb.stego_data(filename[0], filename[1], storingMode, seed)
                lsb.makeVideo(self.lineEditOutputVideo.text())
                shutil.rmtree("temp")
            else:
                if os.path.exists('temp'):
                    shutil.rmtree("temp")
                # just do it
                # print(self.lineEditInputFile.text())
                filepath = self.lineEditInputFile.text()
                filename = os.path.basename(filepath)
                filename = filename.split('.')
                print(filename[0], filename[1])
                if not os.path.exists('temp'):
                    os.makedirs('temp')

                binary_file = fr.ReadFileAsByteArray(
                    self.lineEditInputFile.text())
                extractor = FrameExtractor(
                    self.lineEditInputVideo.text(), "temp")
                extractor.load()
                extractor.extract()
                print("Extracting done")
                lsb = VideoLSB(self.lineEditInputVideo.text(),
                               binary_file, self.lineEditOutputVideo.text(), storingMode)
                lsb.stego_data(filename[0], filename[1], storingMode, seed)
                lsb.makeVideo(self.lineEditOutputVideo.text())
                shutil.rmtree("temp")

        else:
            if encrypt.startswith("With (Vi"):
                # perform encryption
                shutil.rmtree("temp")
                # just do it
                # print(self.lineEditInputFile.text())
                filepath = self.lineEditInputVideo.text()
                filename = os.path.basename(filepath)
                filename = filename.split('.')

                print(filename[0], filename[1])
                if not os.path.exists('temp'):
                    os.makedirs('temp')
                extractor = FrameExtractor(
                    self.lineEditInputVideo.text(), "temp")
                extractor.load()
                extractor.extract()
                print("Extracting done")
                unlsb = VideoUnLSB(self.lineEditInputVideo.text())
                framecount, mode_bit, filename, ext = unlsb.get_stego_metadata()
                binary_string = unlsb.unstego_data(framecount, mode_bit, seed)
                binary_string = utils.BitsToRawString(binary_string)

                vig2 = Vigenere()
                vig2.input_key(self.lineEditKey.text())
                vig2.set_auto(False)
                vig2.set_full(False)
                vig2.set_extended(True)
                decrypted = vig2.decrypt(
                    ''.join([chr(i) for i in binary_string]))
                binary_string = bytes(decrypted)
                fr.SaveFileFromByteArray(
                    binary_string, self.lineEditOutputVideo.text())
                shutil.rmtree("temp")
            else:
                # just do it
                shutil.rmtree("temp")
                # just do it
                # print(self.lineEditInputFile.text())
                filepath = self.lineEditInputVideo.text()
                filename = os.path.basename(filepath)
                filename = filename.split('.')

                print(filename[0], filename[1])
                if not os.path.exists('temp'):
                    os.makedirs('temp')
                extractor = FrameExtractor(
                    self.lineEditInputVideo.text(), "temp")
                extractor.load()
                extractor.extract()
                print("Extracting done")
                unlsb = VideoUnLSB(self.lineEditInputVideo.text())
                framecount, mode_bit, filename, ext = unlsb.get_stego_metadata()
                binary_string = unlsb.unstego_data(framecount, mode_bit, seed)
                binary_string = utils.BitsToRawString(binary_string)
                fr.SaveFileFromByteArray(
                    binary_string, self.lineEditOutputVideo.text())
                shutil.rmtree("temp")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VideoUI()
    app.exec_()
