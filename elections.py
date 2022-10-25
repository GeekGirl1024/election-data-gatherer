"""
This is a basic hello world application to show how to create a python gui
"""
import os
import io
import sys

import urllib
import zipfile

import clarify
import requests


from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

class MyMainWindow(QMainWindow):
  """My Main Window Class"""
  def __init__(self):
    super(MyMainWindow, self).__init__()
    uic.loadUi('./ui-data/elections.ui', self)

  def load(self):
    """function that loads events"""
    self.showData1Button.clicked.connect(self.download_button1_pressed)
    self.showData2Button.clicked.connect(self.download_button2_pressed)
    self.showData3Button.clicked.connect(self.download_button3_pressed)
    self.showData4Button.clicked.connect(self.download_button4_pressed)

    self.download1Button.clicked.connect(self.download_button1_pressed)
    self.download2Button.clicked.connect(self.download_button2_pressed)
    self.download3Button.clicked.connect(self.download_button3_pressed)
    self.download4Button.clicked.connect(self.download_button4_pressed)

  def download_button1_pressed(self):
    url = self.county1Url.text()
    self.downloadFile(url, 1)
  def download_button2_pressed(self):
    url = self.county2Url.text()
    self.downloadFile(url, 2)
  def download_button3_pressed(self):
    url = self.county3Url.text()
    self.downloadFile(url, 3)
  def download_button4_pressed(self):
    url = self.county4Url.text()
    self.downloadFile(url, 4)

  def download_button1_pressed(self):
    self.parseData("Representative in Congress Eleventh Congressional District", 1)
  def download_button2_pressed(self):
    self.parseData("FOR REPRESENTATIVE IN CONGRESS 11TH CONGRESSIONAL DISTRICT", 2)
  def download_button3_pressed(self):
    self.parseData("REPRESENTATIVE IN CONGRESS 11TH CONGRESSIONAL DISTRICT", 3)
  def download_button4_pressed(self):
    self.parseData("REPRESENTATIVE IN CONGRESS 11th CONGRESSIONAL DISTRICT", 4)

  def downloadFile(self, url, countyNumber):
    
    extract_dir = "data"
    countyNumberString = str(countyNumber)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    with open("zip/myzip"+countyNumberString+".zip", 'wb') as f:
      resp = requests.get(url, verify=False, headers=headers)
      f.write(resp.content)

    with zipfile.ZipFile("zip/myzip"+countyNumberString+".zip", "r") as f:
        f.extractall("data"+countyNumberString)

  def parseData(self, contestName, countyNumber):
    """callback function when button is clicked"""

    countyNumberString = str(countyNumber)

    p = clarify.Parser()
    p.parse("data"+countyNumberString+"/detail.xml")

    contest = p.get_contest(contestName)
    

    results = contest.results
    

    choiceTotals = {}

    output = contestName + " " + str(p.timestamp) + "\n"

    for result in results:
      if result.choice is not None:
        # if jurisdiction is none then it is a sum of all jurisdictions
        if result.jurisdiction is None:
          continue
        #output += result.choice.text + " | " + result.vote_type + " | " + str(result.votes) + "\n"

        if result.choice.text not in choiceTotals:
          choiceTotals[result.choice.text] = 0
        
        choiceTotals[result.choice.text] += result.votes



    for k, v in choiceTotals.items():
      output += k + " | " + str(v) + "\n"

    #self.statusArea.inser

    self.statusArea.insertPlainText(output + "\n\n\n")

app = QApplication(sys.argv)
window = MyMainWindow()
window.load()
window.show()
sys.exit(app.exec())
