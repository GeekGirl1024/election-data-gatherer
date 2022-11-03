"""
This is an application to get latest information from various counties
"""

import os
import io
import sys
import zipfile

import clarify
from numpy import append
import requests

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from bs4 import BeautifulSoup
from datetime import datetime
from election import Election
from county import County
from candidate import Candidate
from result import Result



class MyMainWindow(QMainWindow):
  requestHeaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
  election = Election()

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

    self.bill = Candidate()
    self.bill.name = "Bill"
    self.bill.votes = 0

    self.catalina = Candidate()
    self.catalina.name = "Catalina"
    self.catalina.votes = 0

    self.lakeCounty = County()
    self.lakeCounty.name = "Lake"
    self.lakeCounty.clarify = True
    
    self.election.counties.append(self.lakeCounty)

    self.dupageCounty = County()
    self.dupageCounty.name = "Dupage"
    self.dupageCounty.clarify = True
    
    
    self.election.counties.append(self.dupageCounty)

    self.willCounty = County()
    self.willCounty.name = "Will"
    self.willCounty.clarify = True
    
    self.election.counties.append(self.willCounty)

    self.mcHenryCounty = County()
    self.mcHenryCounty.name = "McHenry"
    self.mcHenryCounty.clarify = True
    
    self.election.counties.append(self.mcHenryCounty)

    self.cookCounty = County()
    self.cookCounty.name = "Cook"
    
    self.election.counties.append(self.cookCounty)

    self.kaneCounty = County()
    self.kaneCounty.name = "Kane"
    
    self.election.counties.append(self.kaneCounty)

    self.booneCounty = County()
    self.booneCounty.name = "Boone"
    
    self.election.counties.append(self.booneCounty)


    self.deKalbCounty = County()
    self.deKalbCounty.name = "DeKalb"
    
    self.election.counties.append(self.deKalbCounty)


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

    returnResult = Result()

    for candidate in candidates:

      voteNode = candidate.find_next_sibling("td")
      voteString = voteNode.text.replace("\"", "").strip()
      voteCount = int(voteString)

      candidateName = candidate.text.replace("\"", "").strip()
      output += candidateName + "\n"

      if "catalina" in candidateName.lower():
        returnResult.republican.votes = voteCount

      if "foster" in candidateName.lower():
        returnResult.democrat.votes = voteCount

    self.statusArea.insertPlainText(filePath+" Parsed\n")

    self.statusArea.insertPlainText(output + "\n")

    return returnResult

  def parseKaneCounty(self, filePath):
    returnResult = Result()
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
        result_rows = result_table.find_all(recursive=False)
        for result_row in result_rows :
          result_cols = result_row.find_all(recursive=False)
          
          candidateName = result_cols[1].text.replace("<b>", "").replace("</b>", "").strip()
          voteString = result_cols[2].find_all("b")[0].text.replace("<b>", "").replace("</b>", "").strip()
          voteint = int(voteString)
          if "catalina" in candidateName.lower() :
            returnResult.republican.votes = voteint
          if "foster" in candidateName.lower() :
            returnResult.democrat.votes = voteint
          output +=  candidateName + " " + voteString + "\n"
    

    #self.statusArea.insertPlainText(output + "\n\n\n")
    self.statusArea.insertPlainText(filePath+" Parsed\n")
    return returnResult

app = QApplication(sys.argv)
window = MyMainWindow()
window.load()
window.show()
sys.exit(app.exec())
