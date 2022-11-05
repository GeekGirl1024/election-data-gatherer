
from re import X
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPlainTextEdit, QPushButton

class Election:

  def __init__(self):
    self.name = ""
    self.counties = []
    self.democratTotal = 0
    self.republicanTotal = 0

  def getCurrentState(self):
    democrat = 0
    republican = 0
    for county in self.counties:
      resultsCount = len(county.results)
      if resultsCount > 0 :
        democrat += (county.results[resultsCount-1]).democrat.votes
        republican += (county.results[resultsCount-1]).republican.votes
    self.democratTotal = democrat
    self.republicanTotal = republican

    self.window.showCurrentState()

  def createUi(self, window):
    i = 0
    layout = window.layout()

    for county in self.counties:
      x = 10
      y = 10 + (i)*60
      label = QPlainTextEdit()
      label.move(x, y)
      label.resize(100, 50)
      
      label.setPlainText(county.name)

      county.label = label
      layout.addWidget(label)


      urlBox = QPlainTextEdit()
      urlBox.resize(280, 50)
      urlBox.move(x + 110, y)
      urlBox.setPlainText(county.url)

      county.urlBox = urlBox
      layout.addWidget(urlBox)

      contestNameBox = QPlainTextEdit()
      contestNameBox.resize(250,50)
      contestNameBox.move(x + 400, y)
      contestNameBox.setPlainText(county.contestName)

      county.contestNameBox = contestNameBox
      layout.addWidget(contestNameBox)

      resultBox = QPlainTextEdit()
      resultBox.resize(220, 50)
      resultBox.move(660 + x, y)
      layout.addWidget(resultBox)
      county.resultBox = resultBox


      downloadButton = QPushButton()
      downloadButton.resize(120,30)
      downloadButton.move(890 + x, y)
      downloadButton.setStyleSheet("background:blue")
      downloadButton.text = "Download"
      downloadButton.clicked.connect(county.buttonPress)

      
      county.downloadButton = downloadButton
      layout.addWidget(downloadButton)
      
      
      i += 1
    

