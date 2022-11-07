
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

    self.election.createUi(self)
    

    #self.centralWidget()
    


    self.bill = Candidate()
    self.bill.name = "Bill"
    self.bill.votes = 0

    self.catalina = Candidate()
    self.catalina.name = "Catalina"
    self.catalina.votes = 0


  def getTimeString(self):
    now = datetime.now()
    dateString = now.strftime("%Y%m%d-%H-%M-%S")
    return dateString



  def showCurrentState(self):
    self.resultsTextEdit.setPlainText("Dems:" + str(self.election.democratTotal) + "\n" + "GOP:" + str(self.election.republicanTotal) + "\n")
    