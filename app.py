from PyQt5 import QtWidgets
from stego_wav import Ui_MainWindow  # importing our generated file
import sys
from PyQt5.QtWidgets import QMessageBox

from audio import Audio

class UI(QtWidgets.QMainWindow):

  def __init__(self):

    super(UI, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ui.radioModeHide.toggled.connect(self.update_params)
    self.ui.radioModeRetrieve.toggled.connect(self.update_params)
    self.ui.radioEncryptionWith.toggled.connect(self.update_params)
    self.ui.radioEncryptionWithout.toggled.connect(self.update_params)
    self.ui.radioRandomWith.toggled.connect(self.update_params)
    self.ui.radioRandomWithout.toggled.connect(self.update_params)

    self.ui.radioModeHide.setChecked(True)
    self.ui.radioRandomWithout.setChecked(True)
    self.ui.radioEncryptionWithout.setChecked(True)

    self.ui.buttonInputAudio.clicked.connect(self.load_input_audio)
    self.ui.buttonOutputAudio.clicked.connect(self.load_output_audio)
    self.ui.buttonFileInput.clicked.connect(self.load_input_file)
    self.ui.buttonGo.clicked.connect(self.go)

    self.set_params()

    self.show()

  def load_input_audio(self):
    dialog = QtWidgets.QFileDialog()

    fname = dialog.getOpenFileName(None, "Window name", "", "Audio (*.wav)")
    self.audioInputPath = fname[0]
    self.ui.lineEditInputAudio.setText(self.audioInputPath)

  def load_input_file(self):
    dialog = QtWidgets.QFileDialog()

    fname = dialog.getOpenFileName(None, "Window name", "", "File (*.*)")
    self.fileInputPath = fname[0]
    self.ui.lineEditInputFile.setText(self.fileInputPath)

  def load_output_audio(self):
    dialog = QtWidgets.QFileDialog()

    fname = dialog.getOpenFileName(None, "Window name", "", "File (*.wav)")
    self.audioOutputPath = fname[0]
    self.ui.lineEditOutputAudio.setText(self.audioOutputPath)


  def set_params(self, mode="hide", with_encryption=False, with_random=False):
    self.mode = mode
    self.with_encryption = with_encryption
    self.with_random = with_random
    self.audioInputPath = ""
    self.fileInputPath = ""
    self.audioOutputPath = ""

  def print_params(self):
    print("Mode: {}".format(self.mode))
    print("With Encryption? {}".format(self.with_encryption))
    print("With Random? {}".format(self.with_random))
    print("-"*50)

  def update_params(self):
    if self.ui.radioModeHide.isChecked():
      self.ui.radioModeRetrieve.setChecked(False)
      self.mode = "hide"
      
      self.changeMode("hide")
    if self.ui.radioModeRetrieve.isChecked():
      self.ui.radioModeHide.setChecked(False)
      self.mode = "retrieve"
      
      self.changeMode("retrieve")
    if self.ui.radioEncryptionWithout.isChecked():
      self.ui.radioEncryptionWith.setChecked(False)
      self.with_encryption = False
    if self.ui.radioEncryptionWith.isChecked():
      self.ui.radioEncryptionWithout.setChecked(False)
      self.with_encryption = True
    if self.ui.radioRandomWithout.isChecked():
      self.ui.radioRandomWith.setChecked(False)
      self.with_random = False
    if self.ui.radioRandomWith.isChecked():
      self.ui.radioRandomWithout.setChecked(False)
      self.with_random = True

    self.print_params()

  def changeMode(self, mode):
    if mode == "hide":
      self.ui.lineEditInputAudioLabel.setText("Input Audio File (.wav)")
      self.ui.lineEditInputFileLabel.setText("Plaintext to hide")
      self.ui.lineEditOutputAudioLabel.show()
      self.ui.lineEditOutputAudio.show()
      self.ui.buttonOutputAudio.show()
    elif mode == "retrieve":
      self.ui.lineEditInputAudioLabel.setText("Input StegAudio (.wav)")
      self.ui.lineEditInputFileLabel.setText("Plaintext to show")
      self.ui.lineEditOutputAudioLabel.hide()
      self.ui.lineEditOutputAudio.hide()
      self.ui.buttonOutputAudio.hide()

  def go(self):

    if self.ui.lineEditKey.text() == "":
      print("Error")
      return

    self.key = self.ui.lineEditKey.text()

    if self.mode == "hide":
      self.hide()
    else:
      self.retrieve()

  def hide(self):
    audio = Audio(self.audioInputPath)
    audio.load_file_message(self.fileInputPath)
    audio.lsb(is_encrypted=self.with_encryption, key=self.key, is_random=self.with_random)
    audio.save_stego_audio(self.audioOutputPath)
    self.inform_successful()


  def retrieve(self):
    # audio_stego_path = input("Masukkan path ke audio cover: (format .wav): ")
    # audio_stego_path = output_path_tests[0]
    # Audio = Audio(audio_stego_path)
    audio = Audio(self.audioInputPath)
    audio.decode_lsb(self.fileInputPath, key=self.key)

    # output_path = input("Masukkan file yang ingin disimpan: ")
    # output_path = de_stego_path_tests[1]
    # Audio.decode_lsb(output_path, key="abc")
    pass

  def inform_successful(self):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Sukses")
    msg.setInformativeText("Penyisipan berhasil dilakukan")
    msg.setWindowTitle("-")
    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec_()
    print("value of pressed message box button:", retval)


if __name__ == "__main__":
  app = QtWidgets.QApplication([])
  application = UI()
  
  sys.exit(app.exec())