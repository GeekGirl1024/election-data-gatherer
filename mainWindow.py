
from bs4 import BeautifulSoup
from datetime import datetime
from election import Election
from county import County
from candidate import Candidate
from result import Result
import requests
import zipfile

import os
import io


from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPlainTextEdit, QLayout
from PyQt6 import uic

import clarify

class MainWindow(QMainWindow):
  requestHeaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
  

  """My Main Window Class"""
  def __init__(self, election):
    super(MainWindow, self).__init__()
    uic.loadUi('./ui-data/elections.ui', self)
    self.election = election
    self.election.window = self

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


    self.election.createUi(self)
    

    #self.centralWidget()
    


    self.bill = Candidate()
    self.bill.name = "Bill"
    self.bill.votes = 0

    self.catalina = Candidate()
    self.catalina.name = "Catalina"
    self.catalina.votes = 0

    
  def __getitem__(self, key):
    return getattr(self, key)
  
  def __setitem__(self, key, value):
    setattr(self, key, value)

  def getTimeString(self):
    now = datetime.now()
    dateString = now.strftime("%Y%m%d-%H-%M-%S")
    return dateString

  def download_button1_pressed(self):
    url = self.county1Url.toPlainText()
    countyName = self.county1Label.toPlainText()
    fileName = self.downloadFile(url, countyName)
    contestName = self.contestName1.toPlainText()
    myResult = self.processFile(fileName, contestName)
    county = self.election.counties[0]
    county.results.append(myResult)
    self.election.getCurrentState()

    self.resultsTextEdit.setPlainText("Dems:" + str(self.election.democratTotal) + "\n" + "GOP:" + str(self.election.republicanTotal) + "\n")

    
    self.resultText1.insertPlainText("Dems:" + str(myResult.democrat.votes) + "\n")
    self.resultText1.insertPlainText("GOP:" + str(myResult.republican.votes) + "\n")

  def download_button2_pressed(self):
    url = self.county2Url.toPlainText()
    countyName = self.county2Label.toPlainText()
    fileName = self.downloadFile(url, countyName)
    contestName = self.contestName2.toPlainText()
    myResult = self.processFile(fileName, contestName)
    self.election.counties[1].results.append(myResult)
    self.election.getCurrentState()

    self.resultsTextEdit.setPlainText("Dems:" + str(self.election.democratTotal) + "\n" + "GOP:" + str(self.election.republicanTotal) + "\n")

    self.resultText2.insertPlainText("Dems:" + str(myResult.democrat.votes) + "\n")
    self.resultText2.insertPlainText("GOP:" + str(myResult.republican.votes) + "\n")

  def download_button3_pressed(self):
    url = self.county3Url.toPlainText()
    countyName = self.county3Label.toPlainText()
    fileName = self.downloadFile(url, countyName)
    contestName = self.contestName3.toPlainText()
    myResult = self.processFile(fileName, contestName)
    self.election.counties[2].results.append(myResult)
    self.election.getCurrentState()

    self.resultsTextEdit.setPlainText("Dems:" + str(self.election.democratTotal) + "\n" + "GOP:" + str(self.election.republicanTotal) + "\n")

    self.resultText3.insertPlainText("Dems:" + str(myResult.democrat.votes) + "\n")
    self.resultText3.insertPlainText("GOP:" + str(myResult.republican.votes) + "\n")

  def download_button4_pressed(self):
    url = self.county4Url.toPlainText()
    countyName = self.county4Label.toPlainText()
    fileName = self.downloadFile(url, countyName)
    contestName = self.contestName4.toPlainText()
    myResult = self.processFile(fileName, contestName)
    self.election.counties[3].results.append(myResult)
    self.election.getCurrentState()

    self.resultsTextEdit.setPlainText("Dems:" + str(self.election.democratTotal) + "\n" + "GOP:" + str(self.election.republicanTotal) + "\n")

    self.resultText4.insertPlainText("Dems:" + str(myResult.democrat.votes) + "\n")
    self.resultText4.insertPlainText("GOP:" + str(myResult.republican.votes) + "\n")

  def download_button5_pressed(self):
    url = self.county5Url.toPlainText()
    countyName = self.county5Label.toPlainText()
    contestName = self.contestName5.toPlainText()
    fileName = self.downloadFile(url, countyName)
    myResult = self.parseCookCounty(fileName)

    self.election.counties[4].results.append(myResult)
    self.election.getCurrentState()

    self.resultsTextEdit.setPlainText("Dems:" + str(self.election.democratTotal) + "\n" + "GOP:" + str(self.election.republicanTotal) + "\n")

    self.resultText5.insertPlainText("Dems:" + str(myResult.democrat.votes) + "\n")
    self.resultText5.insertPlainText("GOP:" + str(myResult.republican.votes) + "\n")

  def download_button6_pressed(self):
    url = self.county6Url.toPlainText()
    countyName = self.county6Label.toPlainText()
    contestName = self.contestName6.toPlainText()
    fileName = self.downloadFile(url, countyName)
    myResult = self.parseKaneCounty(fileName)

    self.election.counties[5].results.append(myResult)
    self.election.getCurrentState()

    self.resultsTextEdit.setPlainText("Dems:" + str(self.election.democratTotal) + "\n" + "GOP:" + str(self.election.republicanTotal) + "\n")
    

    self.resultText6.insertPlainText("Dems:" + str(myResult.democrat.votes) + "\n")
    self.resultText6.insertPlainText("GOP:" + str(myResult.republican.votes) + "\n")

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

        candidateName = result.choice.text.lower()
        if candidateName not in choiceTotals:
          choiceTotals[candidateName] = 0
        
        choiceTotals[candidateName] += result.votes

        "Catalina Lauf"
        "Bill Foster"



    for k, v in choiceTotals.items():
      output += k + " | " + str(v) + "\n"

    countyResults = Result()
    if "catalina lauf" in choiceTotals:
      countyResults.republican.votes = choiceTotals["catalina lauf"]
    
    if "bill foster" in choiceTotals:
      countyResults.democrat.votes = choiceTotals["bill foster"]
    
    

    self.statusArea.insertPlainText(filePath+" Parsed\n")
    return countyResults

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
      elif (urlLastSegment == "pdf"):
        with open(outputFile, 'wb') as fd:
          for chunk in resp.iter_content(2000):
              fd.write(chunk)
      else:
        with open(outputFile, 'a+') as f:
          f.write(resp.text)
          self.statusArea.insertPlainText(outputFile+" Saved\n")
      
    return outputFile

  def showCurrentState(self):
    self.resultsTextEdit.setPlainText("Dems:" + str(self.election.democratTotal) + "\n" + "GOP:" + str(self.election.republicanTotal) + "\n")