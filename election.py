
from re import X
from PyQt6.QtWidgets import QStyleOptionButton, QApplication, QMainWindow, QLineEdit, QPlainTextEdit, QPushButton
from PyQt6.QtCore import Qt

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
      
      if county.demOverRide > 0:
        democrat += county.demOverRide
      elif resultsCount > 0 :
        democrat += (county.results[resultsCount-1]).democrat.votes

      if county.gopOverRide > 0:
        republican += county.gopOverRide
      elif resultsCount > 0 :
        republican += (county.results[resultsCount-1]).republican.votes
      
    
    self.democratTotal = democrat
    self.republicanTotal = republican

    self.window.showCurrentState()

  def createUi(self, window):
    i = 0
    layout = window.layout()
    margin = 10

    

    for county in self.counties:
      x = 10
      y = 10 + i * 70

      xNow = x
      
      width = 70
      label = QPlainTextEdit()
      label.move(xNow, y)
      label.resize(width, 60)
      label.setStyleSheet("font-size: 10px; overflow:hidden; ")
      label.setPlainText(county.name)
      county.label = label
      layout.addWidget(label)
      xNow += width + margin

      width = 200
      urlBox = QPlainTextEdit()
      urlBox.resize(width, 60)
      urlBox.move(xNow, y)
      urlBox.setStyleSheet("font-size: 10px; overflow:hidden; ")
      urlBox.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
      urlBox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
      urlBox.setPlainText(county.url)
      county.urlBox = urlBox
      layout.addWidget(urlBox)
      xNow += width + margin

      width = 150
      contestNameBox = QPlainTextEdit()
      contestNameBox.resize(width, 60)
      contestNameBox.move(xNow, y)
      contestNameBox.setStyleSheet("font-size: 10px; overflow:hidden; ")
      contestNameBox.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
      contestNameBox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
      contestNameBox.setPlainText(county.contestName)
      county.contestNameBox = contestNameBox
      layout.addWidget(contestNameBox)
      xNow += width + margin

      width = 400
      filePathBox = QLineEdit()
      filePathBox.setReadOnly(True)
      filePathBox.setStyleSheet("font-size: 10px; overflow:hidden; ")
      
      
      filePathBox.resize(width,20)
      filePathBox.move(xNow, y)
      layout.addWidget(filePathBox)
      county.filePathBox = filePathBox

      hashBox = QLineEdit()
      hashBox.setReadOnly(True)
      hashBox.setStyleSheet("font-size: 10px; overflow:hidden; ")
      
      
      hashBox.resize(width,20)
      hashBox.move(xNow, y + 22)
      layout.addWidget(hashBox)
      county.hashBox = hashBox

      updateTimeBox = QLineEdit()
      updateTimeBox.setReadOnly(True)
      updateTimeBox.setStyleSheet("font-size: 10px; overflow:hidden; ")
      
      
      updateTimeBox.resize(width,20)
      updateTimeBox.move(xNow, y + 44)
      layout.addWidget(updateTimeBox)
      county.updateTimeBox = updateTimeBox
      xNow += width + margin

      width = 100
      resultBox = QPlainTextEdit()
      resultBox.resize(width, 60)
      resultBox.move(xNow, y)
      layout.addWidget(resultBox)
      county.resultBox = resultBox
      xNow += width + margin

      width = 100
      countyInfoBox = QPlainTextEdit()
      countyInfoBox.resize(width, 60)
      countyInfoBox.move(xNow, y)
      layout.addWidget(countyInfoBox)
      county.countyInfoBox = countyInfoBox
      xNow += width + margin

      width = 70
      demOverRideBox = QLineEdit()
      demOverRideBox.resize(width, 30)
      demOverRideBox.move(xNow, y)
      demOverRideBox.textChanged.connect(county.demOverrideChanged)
      layout.addWidget(demOverRideBox)
      county.demOverRideBox = demOverRideBox

      gopOverRideBox = QLineEdit()
      gopOverRideBox.resize(width, 30)
      gopOverRideBox.move(xNow, y + 35)
      gopOverRideBox.textChanged.connect(county.gopOverrideChanged)
      layout.addWidget(gopOverRideBox)
      county.gopOverRideBox = gopOverRideBox
      xNow += width + margin

      
      width = 120
      downloadButton = QPushButton()
      downloadButton.resize(width,30)
      downloadButton.move(xNow, y)
      downloadButton.setStyleSheet("background:lightblue; border:grey; border-style: solid; border-width: 5px;")
      downloadButton.text = "Download"
      downloadButton.clicked.connect(county.buttonPress)

      
      county.downloadButton = downloadButton
      layout.addWidget(downloadButton)
      xNow += width + margin
      
      
      i += 1
    

