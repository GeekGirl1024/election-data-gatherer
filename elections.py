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

from bs4 import BeautifulSoup

class MyMainWindow(QMainWindow):
  """My Main Window Class"""
  def __init__(self):
    super(MyMainWindow, self).__init__()
    uic.loadUi('./ui-data/elections.ui', self)

  def load(self):
    """function that loads events"""
    self.showData1Button.clicked.connect(self.showData_button1_pressed)
    self.showData2Button.clicked.connect(self.showData_button2_pressed)
    self.showData3Button.clicked.connect(self.showData_button3_pressed)
    self.showData4Button.clicked.connect(self.showData_button4_pressed)
    self.showData5Button.clicked.connect(self.showData_button5_pressed)
    self.showData6Button.clicked.connect(self.showData_button6_pressed)
    self.showData7Button.clicked.connect(self.showData_button7_pressed)
    self.showData8Button.clicked.connect(self.showData_button8_pressed)

    self.download1Button.clicked.connect(self.download_button1_pressed)
    self.download2Button.clicked.connect(self.download_button2_pressed)
    self.download3Button.clicked.connect(self.download_button3_pressed)
    self.download4Button.clicked.connect(self.download_button4_pressed)
    self.download5Button.clicked.connect(self.download_button5_pressed)
    self.download6Button.clicked.connect(self.download_button6_pressed)
    self.download7Button.clicked.connect(self.download_button7_pressed)
    self.download8Button.clicked.connect(self.download_button8_pressed)

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

  def download_button5_pressed(self):
    self.downloadCookCounty()

  def download_button6_pressed(self):
    self.downloadKaneCounty()

  def download_button7_pressed(self):
    url = self.county7Url.text()

  def download_button8_pressed(self):
    url = self.county8Url.text()

  def showData_button1_pressed(self):
    self.parseData("Representative in Congress Eleventh Congressional District", 1)

  def showData_button2_pressed(self):
    self.parseData("FOR REPRESENTATIVE IN CONGRESS 11TH CONGRESSIONAL DISTRICT", 2)

  def showData_button3_pressed(self):
    self.parseData("REPRESENTATIVE IN CONGRESS 11TH CONGRESSIONAL DISTRICT", 3)

  def showData_button4_pressed(self):
    self.parseData("REPRESENTATIVE IN CONGRESS 11th CONGRESSIONAL DISTRICT", 4)
  
  def showData_button5_pressed(self):
    self.parseCookCounty()

  def showData_button6_pressed(self):
    self.parseKaneCounty()
    self.statusArea.insertPlainText("Button Pressed6\n\n\n")

  def showData_button7_pressed(self):
    self.statusArea.insertPlainText("Button Pressed7\n\n\n")

  def showData_button8_pressed(self):
    self.statusArea.insertPlainText("Button Pressed8\n\n\n")

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

  def downloadCookCounty(self):
    url = self.county5Url.text()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    with open("cookCountyData.html", 'a+') as f:
      resp = requests.get(url, verify=False, headers=headers)
      f.write(resp.text)

  def parseCookCounty(self):
    output = ""
    contents = ""
    with open("cookCountyData.html", 'r') as f:
      contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')
    candidates = soup.find_all("td", {"class": "candidate"})

    for candidate in candidates:
      output += candidate.text + "\n"


    self.statusArea.insertPlainText(output + "\n\n\n")


  def downloadKaneCounty(self):
    url = self.county6Url.text()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    with open("kaneCountyData.html", 'a+') as f:
      resp = requests.get(url, verify=False, headers=headers)
      f.write(resp.text)
  
  def parseKaneCounty(self):
    output = ""
    contents = ""
    with open("kaneCountyData.html", 'r') as f:
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

    self.statusArea.insertPlainText(output + "\n\n\n")
    


app = QApplication(sys.argv)
window = MyMainWindow()
window.load()
window.show()
sys.exit(app.exec())
