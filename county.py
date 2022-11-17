import io
import json
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
from datetime import datetime
from candidate import Candidate
from result import Result
from bs4 import BeautifulSoup
import zipfile

import clarify
import requests
import hashlib

class County:
  requestHeaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

  def getTimeString(self):
      now = datetime.now()
      dateString = now.strftime("%Y%m%d-%H-%M-%S")
      return dateString

  def __init__(self):
    self.timestamp = datetime.now()
    self.clarify = False
    self.pdf = False
    self.name = ""
    self.contestName = ""
    self.results = []
    self.url = ""
    self.gopOverRide = 0
    self.demOverRide = 0
    self.projectedTotal = 0
    
  
  def getCurrentResults(self) :
    
    returnResult = Result()
    resultCount = len(self.results)
    if (resultCount != 0):
      latestResult = self.results[resultCount - 1]
      returnResult.democrat.votes = latestResult.democrat.votes
      returnResult.republican.votes = latestResult.republican.votes
      returnResult.other.votes = latestResult.other.votes
      returnResult.precinctsReported = latestResult.precinctsReported
      returnResult.precinctsReporting = latestResult.precinctsReporting

    return returnResult

  def demOverrideChanged(self):
    demOverrideString = self.demOverRideBox.text().strip()
    try:
      demOverride = int(demOverrideString)
      self.demOverRide = demOverride
    except:
      self.demOverRide = 0
    self.election.getCurrentState()

  def gopOverrideChanged(self):
    gopOverrideString = self.gopOverRideBox.text().strip()
    try:
      gopOverride = int(gopOverrideString)
      self.gopOverRide = gopOverride
    except:
      self.gopOverRide = 0
    self.election.getCurrentState()

  def buttonPress(self):

      url = self.urlBox.toPlainText()

      if self.clarify:

        with requests.get(url+"current_ver.txt", verify=False, headers=self.requestHeaders) as resp :
          
            url = url + resp.text + "/reports/detailxml.zip"



      countyName = self.label.toPlainText()
      contestName = self.contestNameBox.toPlainText()
      myResult = self.downloadFile(url, countyName)
      if (myResult.error):
        pass
      elif self.pdf :
        pass
      elif hasattr(self, 'customParse') :
        myResult = self.customParse(self, myResult, contestName)
      else :
        
        myResult = self.processFile(myResult, contestName)

      myResult.hash = self.getHash(myResult.fileName)
      
      

      self.filePathBox.setText(myResult.fileName)

      self.updateTimeBox.setText(myResult.updateTime)

      self.hashBox.setText(myResult.hash)

      self.countyInfoBox.setPlainText("Reporting: " + str(myResult.precinctsReported) + " / "+str(myResult.precinctsReporting) )

      self.results.append(myResult)
      
      output = ""
      
      if myResult.error:
        output += "Error Occured\n"
      elif self.pdf:
        output += "Processed\n"
      else:
        output += "DEM " + str(myResult.democrat.votes) + "\n" + "GOP " + str(myResult.republican.votes)
        
      
      self.resultBox.setPlainText(output)

      self.election.getCurrentState()

  def getHash(self, filePath):
    file_hash = hashlib.sha256()
    with open(filePath, 'rb') as file:
      fileBuffer = file.read(5000)
      while len(fileBuffer) > 0:
          file_hash.update(fileBuffer)
          fileBuffer = file.read(5000)

    return file_hash.hexdigest()

  def processFile2(self, countyResults, contestName) :
    contents = ""
    with open(countyResults.fileName, 'r') as f:
      contents = f.read()
    
    allData = json.loads(contents)

    allData

  def processFile(self, countyResults, contestName) :

    p = clarify.Parser()
    
    p.parse(countyResults.fileName)

    contest = p.get_contest(contestName)
    countyResults.precinctsReported = contest.precincts_reported
    countyResults.precinctsReporting = contest.precincts_reporting
    

    results = contest.results
    

    demName = "foster"
    gopName = "lauf"
    choiceTotals = { demName: 0, gopName: 0}

    countyResults.updateTime = str(p.timestamp)
    

    output = contestName + " " + str(p.timestamp) + "\n"

    for result in results:
      if result.choice is not None:
        # if jurisdiction is none then it is a sum of all jurisdictions
        if result.jurisdiction is not None:
          continue
        #output += result.choice.text + " | " + result.vote_type + " | " + str(result.votes) + "\n"

        candidateName = result.choice.text.lower()
        if (demName in candidateName):
          choiceTotals[demName] += result.votes

        if (gopName in candidateName):
          choiceTotals[gopName] += result.votes


    for k, v in choiceTotals.items():
      output += k + " | " + str(v) + "\n"


    countyResults.republican.votes = choiceTotals[gopName]
    
    countyResults.democrat.votes = choiceTotals[demName]
    
    return countyResults
      
  def downloadFile(self, url, countyName):
    
    dateString = self.getTimeString()
    urlSegments = url.split(".")
    fileExtension = "html"

    fileResult = Result()
    if (len(urlSegments) > 0):
      urlLastSegment = urlSegments[-1].lower()
      if (urlLastSegment == "xml"):
        fileExtension = "xml"
      elif (urlLastSegment == "pdf"):
        fileExtension = "pdf"
      elif (urlLastSegment == "zip"):
        fileExtension = "xml"
      elif (urlLastSegment == "json"):
        fileExtension = "json"

    outputFile = "Data/" + countyName+"/"+dateString+"."+fileExtension
    

    with requests.get(url, verify=False, headers=self.requestHeaders) as resp :
      
      #self.statusArea.insertPlainText(countyName+" Downloaded\n")
      if resp.status_code != 200:
        outputFile = "Data/" + countyName+"/"+dateString+".html"
        fileResult.error = True
        with open(outputFile, 'wb') as fd:
          for chunk in resp.iter_content(5000):
              fd.write(chunk)
        
      elif (urlLastSegment == "zip") :
        with zipfile.ZipFile(io.BytesIO(resp.content)) as f:
          f.extractall("Data/"+countyName)
          os.rename("Data/"+countyName + "/detail.xml", outputFile)
          #self.statusArea.insertPlainText(outputFile+" UnZipped and Saved\n")
      elif (urlLastSegment == "pdf"):
        with open(outputFile, 'wb') as fd:
          for chunk in resp.iter_content(5000):
              fd.write(chunk)
      else :
        with open(outputFile, 'a+') as f:
          f.write(resp.text)
          #self.statusArea.insertPlainText(outputFile+" Saved\n")
    
    fileResult.fileName = outputFile

    return fileResult
