"""
This is a basic hello world application to show how to create a python gui
"""
from datetime import datetime
import os
import io
import sys

import urllib
import zipfile

import clarify
import requests

import tabula

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from bs4 import BeautifulSoup
from tomlkit import date

class MyMainWindow(QMainWindow):
  requestHeaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

  """My Main Window Class"""
  def __init__(self):
    super(MyMainWindow, self).__init__()
    uic.loadUi('./ui-data/elections.ui', self)

  def load(self):
    """function that loads events"""

    self.download1Button.clicked.connect(self.download_button1_pressed)
    self.download2Button.clicked.connect(self.download_button2_pressed)
    self.download3Button.clicked.connect(self.download_button3_pressed)
    self.download4Button.clicked.connect(self.download_button4_pressed)
    self.download5Button.clicked.connect(self.download_button5_pressed)
    self.download6Button.clicked.connect(self.download_button6_pressed)
    self.download7Button.clicked.connect(self.download_button7_pressed)
    self.download8Button.clicked.connect(self.download_button8_pressed)

  def getTimeString(self):
    now = datetime.now()
    dateString = now.strftime("%Y%m%d-%H-%M-%S")
    return dateString

  def download_button1_pressed(self):
    url = self.county1Url.toPlainText()
    countyName = self.county1Label.toPlainText()
    fileName = self.downloadFile(url, countyName)
    contestName = self.contestName1.toPlainText()
    self.processFile(fileName, contestName)

  def download_button2_pressed(self):
    url = self.county2Url.toPlainText()
    countyName = self.county2Label.toPlainText()
    fileName = self.downloadFile(url, countyName)
    contestName = self.contestName2.toPlainText()
    self.processFile(fileName, contestName)

  def download_button3_pressed(self):
    url = self.county3Url.toPlainText()
    countyName = self.county3Label.toPlainText()
    fileName = self.downloadFile(url, countyName)
    contestName = self.contestName3.toPlainText()
    self.processFile(fileName, contestName)

  def download_button4_pressed(self):
    url = self.county4Url.toPlainText()
    countyName = self.county4Label.toPlainText()
    fileName = self.downloadFile(url, countyName)
    contestName = self.contestName4.toPlainText()
    self.processFile(fileName, contestName)

  def download_button5_pressed(self):
    url = self.county5Url.toPlainText()
    countyName = self.county5Label.toPlainText()
    contestName = self.contestName5.toPlainText()
    fileName = self.downloadFile(url, countyName)
    self.parseCookCounty(fileName)

  def download_button6_pressed(self):
    url = self.county6Url.toPlainText()
    countyName = self.county6Label.toPlainText()
    contestName = self.contestName6.toPlainText()
    fileName = self.downloadFile(url, countyName)
    self.parseKaneCounty(fileName)

  def download_button7_pressed(self):
    url = self.county7Url.toPlainText()
    countyName = self.county7Label.toPlainText()
    contestName = self.contestName7.toPlainText()
    fileName = self.downloadFile(url, countyName)

  def download_button8_pressed(self):
    url = self.county8Url.toPlainText()
    countyName = self.county8Label.toPlainText()
    contestName = self.contestName8.toPlainText()
    fileName = self.downloadFile(url, countyName)

  def processFile(self, filePath, contestName) :
    p = clarify.Parser()
    
    p.parse(filePath)

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

    self.statusArea.insertPlainText(filePath+" Parsed\n")

  def downloadFile(self, url, countyName):
    
    dateString = self.getTimeString()
    urlSegments = url.split(".")
    fileExtension = "html"
    if (len(urlSegments) > 0):
      urlLastSegment = urlSegments[-1].lower()
      if (urlLastSegment == "xml"):
        fileExtension = "xml"
      elif (urlLastSegment == "pdf"):
        fileExtension = "pdf"
      elif (urlLastSegment == "zip"):
        fileExtension = "xml"

    outputFile = "Data/" + countyName+"/"+dateString+"."+fileExtension
    with requests.get(url, verify=False, headers=self.requestHeaders) as resp :
      self.statusArea.insertPlainText(countyName+" Downloaded\n")
      if (urlLastSegment == "zip") :
        with zipfile.ZipFile(io.BytesIO(resp.content)) as f:
          f.extractall("Data/"+countyName)
          os.rename("Data/"+countyName + "/detail.xml", outputFile)
          self.statusArea.insertPlainText(outputFile+" UnZipped and Saved\n")
      else :
        with open(outputFile, 'a+') as f:
          f.write(resp.text)
          self.statusArea.insertPlainText(outputFile+" Saved\n")
      
    return outputFile

  def parseCookCounty(self, filePath):
    output = ""
    contents = ""
    with open(filePath, 'r') as f:
      contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')
    candidates = soup.find_all("td", {"class": "candidate"})

    for candidate in candidates:
      output += candidate.text + "\n"

    self.statusArea.insertPlainText(filePath+" Parsed\n")

  def parseKaneCounty(self, filePath):
    output = ""
    contents = ""
    with open(filePath, 'r') as f:
      contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')
    choices = soup.find_all("table", {"class": "choice"})

    for choice in choices:
      header2 = choice.find("h2")
      if ( header2 and ("11TH CONGRESSIONAL DISTRICT REPRESENTATIVE IN CONGRESS" in header2.text)):
        result_table = choice.find_next_sibling("table")
        result_rows = result_table.find_all("tr")
        for result_row in result_rows :
          result_cols = result_row.find_all(recursive=False)
          output += result_cols[1].text + "\n"
        break

    #self.statusArea.insertPlainText(output + "\n\n\n")
    self.statusArea.insertPlainText(filePath+" Parsed\n")

app = QApplication(sys.argv)
window = MyMainWindow()
window.load()
window.show()
sys.exit(app.exec())
