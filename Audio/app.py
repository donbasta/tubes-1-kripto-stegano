from PyQt5 import QtWidgets, QtCore, QtMultimedia
from Audio.stego_wav_1 import Ui_MainWindow  # importing our generated file
import sys
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from Audio.audio import calc_psnr

from Audio.audio import Audio

class AudioUI(QtWidgets.QMainWindow):

  def __init__(self):

    super(AudioUI, self).__init__()
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
    self.ui.buttonFileInput.clicked.connect(self.io_file)
    self.ui.buttonGo.clicked.connect(self.go)

    self.set_params()

    self.resize(1400, 900)

    self.show()

  def load_input_audio(self):
    dialog = QtWidgets.QFileDialog()

    fname = dialog.getOpenFileName(None, "Window name", "", "Audio (*.wav)")
    self.audioInputPath = fname[0]
    self.ui.lineEditInputAudio.setText(self.audioInputPath)

  def load_input_file(self):
    dialog = QtWidgets.QFileDialog()

    fname = dialog.getOpenFileName(None, "Window name", "", "All Files (*)")
    self.fileInputPath = fname[0]
    self.ui.lineEditInputFile.setText(self.fileInputPath)

  def load_output_audio(self):
    dialog = QtWidgets.QFileDialog()

    fname = dialog.getOpenFileName(None, "Window name", "", "File (*.wav)")
    self.audioOutputPath = fname[0]
    self.ui.lineEditOutputAudio.setText(self.audioOutputPath)

  def save_output_file(self):
    dialog = QtWidgets.QFileDialog()

    fname = dialog.getSaveFileName(None, "Window name", "", "All Files (*)")
    self.fileInputPath = fname[0]
    self.ui.lineEditInputFile.setText(self.fileInputPath)

  def io_file(self):
    if self.mode == "hide":
      self.load_input_file()
    elif self.mode =="retrieve":
      self.save_output_file()

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
    try:
      audio = Audio(self.audioInputPath)
      psnr_i = audio.get_amplitude()
      audio.load_file_message(self.fileInputPath)
      audio.lsb(is_encrypted=self.with_encryption, key=self.key, is_random=self.with_random)
      audio.save_stego_audio(self.audioOutputPath)
      psnr_f = Audio(self.audioOutputPath).get_amplitude()
      psnr = calc_psnr(psnr_i, psnr_f)
      self.inform_successful(psnr)
    except Exception as e:
      self.inform_unsuccessful(str(e))


  def retrieve(self):
    audio = Audio(self.audioInputPath)
    audio.decode_lsb(self.fileInputPath, key=self.key)

  def inform_successful(self, psnr):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Sukses")
    msg.setInformativeText("Penyisipan berhasil dilakukan")
    msg.setWindowTitle("Penyisipan sukses")
    msg.setDetailedText("Nilai dari PSMR (Kualitas Audio) adalah: {}".format(psnr))
    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec_()

  def inform_unsuccessful(self, er):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Gagal")
    msg.setInformativeText(er)
    msg.setWindowTitle("Penyisipan gagal")
    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec_()


if __name__ == "__main__":
  app = QtWidgets.QApplication([])
  application = AudioUI()
  
  sys.exit(app.exec())