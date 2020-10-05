from PyQt5 import QtWidgets, QtCore
from mainUI import Ui_MainWindow  # importing our generated file

from Audio.app import AudioUI
from Citra.gui import CitraUI
from Video.main import VideoUI
import sys

class UI(QtWidgets.QMainWindow):

  to_audio = QtCore.pyqtSignal(str)
  to_video = QtCore.pyqtSignal(str)
  to_citra = QtCore.pyqtSignal(str)

  def __init__(self):

    super(UI, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ui.audioMenu.clicked.connect(self.run_audio)
    self.ui.citraMenu.clicked.connect(self.run_citra)
    self.ui.videoMenu.clicked.connect(self.run_video)

  def run_audio(self):
    self.to_audio.emit("audio")

  def run_citra(self):
    self.to_citra.emit("citra")

  def run_video(self):
    self.to_video.emit("video")

class Controller:

  def __init__(self):
    pass

  def showMainMenu(self):
    self.window = UI()
    self.window.show()
    self.window.to_audio.connect(self.showAudio)
    self.window.to_citra.connect(self.showCitra)
    self.window.to_video.connect(self.showVideo)

  def showAudio(self):
    self.audio_window = AudioUI()
    self.window.close()
    self.audio_window.show()

  def showCitra(self):
    self.citra_window = CitraUI()
    self.window.close()
    self.citra_window.show()

  def showVideo(self):
    self.video_window = VideoUI()
    self.window.close()
    self.video_window.show()

def main():
  app = QtWidgets.QApplication([])
  controller = Controller()
  controller.showMainMenu()
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
