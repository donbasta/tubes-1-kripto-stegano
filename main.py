from PyQt5 import QtWidgets, uic
import sys
import FileReader as fr
from FrameExtractor import FrameExtractor
from VideoLSB import VideoLSB, VideoUnLSB
from vigenere import Vigenere
import utils
import os
import shutil


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
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

        self.labelFrameCount = self.findChild(
            QtWidgets.QLabel, 'labelFrameCount')
        self.labelFilename = self.findChild(QtWidgets.QLabel, 'labelFilename')
        self.labelExt = self.findChild(QtWidgets.QLabel, 'labelExt')

        self.show()

    def getSelectedRadioButton(self, QButtonGroupObject: list):
        for item in QButtonGroupObject:
            if item.isChecked():
                return item.text()

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


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
