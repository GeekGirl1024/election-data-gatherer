"""
This is an application to get latest information from various counties
"""


#import json
import json
import sys
import sched, time


from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt6 import uic, QtCore

from bs4 import BeautifulSoup
from datetime import datetime
from election import Election
from county import County
from candidate import Candidate
from result import Result

from mainWindow import MainWindow

def parseCookCounty(self, countyResult, contestName):
    output = ""
    contents = ""
    #countyResult.fileName = "Data/Cook/20221108-14-53-59.html"
    with open(countyResult.fileName, 'r') as f:
      contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')
    contests = soup.find_all("div", {"class": "panel contest"})

    

    #side = soup.find("div", {"id": "collapseOne"})
    updateTime = soup.find("div", {"id": "lblGeneratedTimeStamp"})

    countyResult.updateTime = updateTime.text.strip()

    for contest in contests:

      contestNameElement = contest.find("h5")

      if contestNameElement.text == contestName:

        headerInfo = contest.find("tr", { "class" : "headerInfo"})
        reportingElement = headerInfo.find("div", { "class": "container row"}).find_all("div")[1]

        reportingText = reportingElement.text
        reportingText = reportingText.replace("Precincts Reported","").strip()
        reportingOf = reportingText.split(" of ")
        countyResult.precinctsReported = int(reportingOf[0])
        countyResult.precinctsReporting = int(reportingOf[1])

        candidateRows = contest.find("tbody").find_all("tr")
        for candidateRow in candidateRows:
          candidateElement = candidateRow.find("td", {"colspan": "2"})
          voteNode = candidateElement.find_next_sibling("td")
          voteString = voteNode.text.replace("\"", "").strip()
          voteString = voteString.replace(",", "")
          voteCount = int(voteString)

          candidateName = candidateElement.text.replace("\"", "").strip()
          output += candidateName + "\n"

          if "catalina" in candidateName.lower():
            countyResult.republican.votes = voteCount

          if "foster" in candidateName.lower():
            countyResult.democrat.votes = voteCount

        break

      




    return countyResult


def parseKaneCounty(self, countyResult, contestName):
  
  output = ""
  contents = ""
  with open(countyResult.fileName, 'r') as f:
    contents = f.read()
  soup = BeautifulSoup(contents, 'html.parser')

  form = soup.find("form")

  countyResult.updateTime = form.find("small").text

  choices = soup.find_all("table", {"class": "choice"})

  for choice in choices:
    header2 = choice.find("h2")
    if ( header2 and (contestName in header2.text)):
      summary_table = choice.find_previous_sibling("table")
      reporting_cell = summary_table.find_all("td")[3]
      reporting_num = reporting_cell.find_all("b")
      countyResult.precinctsReported = int(reporting_num[0].text)
      countyResult.precinctsReporting = int(reporting_num[1].text)

      result_table = choice.find_next_sibling("table")
      result_rows = result_table.find_all(recursive=False)
      for result_row in result_rows :
        result_cols = result_row.find_all(recursive=False)
        
        candidateName = result_cols[1].text.replace("<b>", "").replace("</b>", "").strip()
        voteString = result_cols[2].find_all("b")[0].text.replace("<b>", "").replace("</b>", "").strip()
        voteint = int(voteString)
        if "catalina" in candidateName.lower() :
          countyResult.republican.votes = voteint
        if "foster" in candidateName.lower() :
          countyResult.democrat.votes = voteint
        output +=  candidateName + " " + voteString + "\n"

  return countyResult

def parseDeKalbCounty(self, countyResult, contestName):

  return countyResult

def parseBooneCounty(self, countyResult, contestName):

  output = ""
  contents = ""
  with open(countyResult.fileName, 'r') as f:
    contents = f.read()
  soup = BeautifulSoup(contents, 'html.parser')

  jsonString = soup.find_all("script")[4].text.split("\n")[2].strip()
  jsonStringStart = "var electionData = "
  if jsonString.startswith(jsonStringStart):
    jsonString = jsonString[len(jsonStringStart):]
    jsonString = jsonString[:-1]
    allData = json.loads(jsonString)
    
    #catalina total y["Races"][7]['Candidates'][0]['TotalVotesForCandidate']
    countyResult.republican.votes = allData["Races"][7]['Candidates'][0]['TotalVotesForCandidate']
    #bill total y["Races"][7]['Candidates'][0]['TotalVotesForCandidate']
    countyResult.democrat.votes = allData["Races"][7]['Candidates'][1]['TotalVotesForCandidate']
    #len(y["Races"][7]['Reporting'])
    #len(y["Races"][7]['NotReporting'])

    countyResult.updateTime = allData["Election"]["UpdateTime"]
    countyResult.precinctsReported = len(allData["Races"][7]['Reporting'])
    countyResult.precinctsReporting = len(allData["Races"][7]['NotReporting']) + len(allData["Races"][7]['Reporting'])


  return countyResult

election = Election()

lakeCounty = County()
lakeCounty.name = "Lake"
lakeCounty.clarify = True
lakeCounty.url = "https://results.enr.clarityelections.com/IL/Lake/115764/"
#lakeCounty.url = "https://results.enr.clarityelections.com//IL/Lake/115764/308024/reports/detailxml.zip"
lakeCounty.contestName = "Representative in Congress Eleventh Congressional District"
lakeCounty.projectedTotal = 8476
lakeCounty.election = election
  
election.counties.append(lakeCounty)

dupageCounty = County()
dupageCounty.name = "Dupage"
dupageCounty.clarify = True
dupageCounty.url = "https://www.dupageresults.gov/IL/DuPage/115972/"
#dupageCounty.url = "https://www.dupageresults.gov/IL/DuPage/115972/310392/json/sum.json"
#dupageCounty.url = "https://www.dupageresults.gov/IL/DuPage/115972/web.307039/#/detail/350"
#dupageCounty.url = "https://www.dupageresults.gov//IL/DuPage/115972/310045/reports/detailxml.zip"
dupageCounty.contestName = "FOR REPRESENTATIVE IN CONGRESS 11TH CONGRESSIONAL DISTRICT"
dupageCounty.projectedTotal = 90349
dupageCounty.election = election 
  
election.counties.append(dupageCounty)

willCounty = County()
willCounty.name = "Will"
willCounty.clarify = True
willCounty.url = "https://results.enr.clarityelections.com/IL/Will/116151/"
#willCounty.url = "https://results.enr.clarityelections.com//IL/Will/116151/310084/reports/detailxml.zip"
willCounty.contestName = "REPRESENTATIVE IN CONGRESS 11TH CONGRESSIONAL DISTRICT"
willCounty.projectedTotal = 29284
willCounty.election = election

election.counties.append(willCounty)

mcHenryCounty = County()
mcHenryCounty.name = "McHenry"
mcHenryCounty.clarify = True
mcHenryCounty.url = "https://results.enr.clarityelections.com/IL/McHenry/115977/"
#mcHenryCounty.url = "https://results.enr.clarityelections.com//IL/McHenry/115977/309238/reports/detailxml.zip"
mcHenryCounty.contestName = "REPRESENTATIVE IN CONGRESS 11th CONGRESSIONAL DISTRICT"
mcHenryCounty.projectedTotal = 66886
mcHenryCounty.election = election

election.counties.append(mcHenryCounty)

cookCounty = County()
cookCounty.name = "Cook"
cookCounty.url = "https://electionnight.cookcountyclerkil.gov/"
cookCounty.contestName = "U.S. Representative, 11th District - Vote For 1"

cookCounty.customParse = parseCookCounty
cookCounty.projectedTotal = 4480
cookCounty.election = election
  
election.counties.append(cookCounty)

kaneCounty = County()
kaneCounty.name = "Kane"
kaneCounty.url = "http://electionresults.countyofkane.org/Contests.aspx?Id=27"
kaneCounty.customParse = parseKaneCounty
kaneCounty.projectedTotal = 85980
kaneCounty.contestName = "FOR THE 11TH CONGRESSIONAL DISTRICT REPRESENTATIVE IN CONGRESS"
kaneCounty.election = election
  
election.counties.append(kaneCounty)

booneCounty = County()
booneCounty.name = "Boone"
booneCounty.url = "https://il-boone.pollresults.net/"
booneCounty.customParse = parseBooneCounty
booneCounty.projectedTotal = 7366
booneCounty.contestName = "CONGRESSIONAL 11TH DISTRICT REPRESENTATIVE"
booneCounty.election = election
  
election.counties.append(booneCounty)


deKalbCounty = County()
deKalbCounty.name = "DeKalb"
deKalbCounty.url = "https://platinumelectionresults.com/turnouts/county/66"
#deKalbCounty.url = "http://dekalb.il.clerkserve.com/?cat=49"
deKalbCounty.customParse = parseDeKalbCounty
deKalbCounty.projectedTotal = 3710
deKalbCounty.election = election
  
election.counties.append(deKalbCounty)

app = QApplication(sys.argv)
window = MainWindow(election)

window.load()

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print("Doing stuff...")
    for county in election.counties :
      county.buttonPress()
    sc.enter(120, 1, do_something, (sc,))

s.enter(120, 1, do_something, (s,))
#s.run()


def calculo():
    global time
    time = time.addSecs(15)
    print(time.toString("hh:mm:ss"))
    for county in election.counties :
      county.buttonPress()
    window.statusArea.setPlainText("Update: " + time.toString("hh:mm:ss") + "\n" + window.statusArea.toPlainText())
    


timer0 = QtCore.QTimer()
time = QtCore.QTime(0, 0, 0)
timer0.setInterval(15000)
timer0.timeout.connect(calculo)
timer0.start()

window.show()



sys.exit(app.exec())
