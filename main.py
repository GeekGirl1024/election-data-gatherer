"""
This is an application to get latest information from various counties
"""


import sys



from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt6 import uic

from bs4 import BeautifulSoup
from datetime import datetime
from election import Election
from county import County
from candidate import Candidate
from result import Result

from mainWindow import MainWindow

def parseCookCounty(self, countyResult):
    output = ""
    contents = ""
    with open(countyResult.fileName, 'r') as f:
      contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')
    candidates = soup.find_all("td", {"class": "candidate"})

    

    side = soup.find("div", {"id": "collapseOne"})
    updateTime = side.find("div", {"class": "text-center"})

    countyResult.updateTime = updateTime.text.strip()

    for candidate in candidates:

      voteNode = candidate.find_next_sibling("td")
      voteString = voteNode.text.replace("\"", "").strip()
      voteCount = int(voteString)

      candidateName = candidate.text.replace("\"", "").strip()
      output += candidateName + "\n"

      if "catalina" in candidateName.lower():
        countyResult.republican.votes = voteCount

      if "foster" in candidateName.lower():
        countyResult.democrat.votes = voteCount


    return countyResult


def parseKaneCounty(self, countyResult):
  
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
    if ( header2 and ("11TH CONGRESSIONAL DISTRICT REPRESENTATIVE IN CONGRESS" in header2.text)):
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



election = Election()

lakeCounty = County()
lakeCounty.name = "Lake"
lakeCounty.clarify = True
lakeCounty.url = "https://results.enr.clarityelections.com/IL/Lake/114135/300541/reports/detailxml.zip"
lakeCounty.contestName = "Representative in Congress Eleventh Congressional District"
lakeCounty.projectedTotal = 8476
lakeCounty.election = election
  
election.counties.append(lakeCounty)

dupageCounty = County()
dupageCounty.name = "Dupage"
dupageCounty.clarify = True
dupageCounty.url = "https://www.dupageresults.gov//IL/DuPage/114213/300666/reports/detailxml.zip"
dupageCounty.contestName = "FOR REPRESENTATIVE IN CONGRESS 11TH CONGRESSIONAL DISTRICT"
dupageCounty.projectedTotal = 90349
dupageCounty.election = election 
  
election.counties.append(dupageCounty)

willCounty = County()
willCounty.name = "Will"
willCounty.clarify = True
willCounty.url = "https://results.enr.clarityelections.com//IL/Will/114217/300664/reports/detailxml.zip"
willCounty.contestName = "REPRESENTATIVE IN CONGRESS 11TH CONGRESSIONAL DISTRICT"
willCounty.projectedTotal = 29284
willCounty.election = election

election.counties.append(willCounty)

mcHenryCounty = County()
mcHenryCounty.name = "McHenry"
mcHenryCounty.clarify = True
mcHenryCounty.url = "https://results.enr.clarityelections.com//IL/McHenry/115186/301334/reports/detailxml.zip"
mcHenryCounty.contestName = "REPRESENTATIVE IN CONGRESS 11th CONGRESSIONAL DISTRICT"
mcHenryCounty.projectedTotal = 66886
mcHenryCounty.election = election

election.counties.append(mcHenryCounty)

cookCounty = County()
cookCounty.name = "Cook"
cookCounty.url = "https://results622.cookcountyclerkil.gov/Home/Detail?contestId=203"

cookCounty.customParse = parseCookCounty
cookCounty.projectedTotal = 4480
cookCounty.election = election
  
election.counties.append(cookCounty)

kaneCounty = County()
kaneCounty.name = "Kane"
kaneCounty.url = "http://electionresults.countyofkane.org/Contests.aspx?Id=26"
kaneCounty.customParse = parseKaneCounty
kaneCounty.projectedTotal = 85980
kaneCounty.election = election
  
election.counties.append(kaneCounty)

booneCounty = County()
booneCounty.name = "Boone"
booneCounty.url = "https://www.boonecountyil.gov/Departments/Clerk-Recorder/voting/2022_jun_28_il_boone_SOVC.pdf"
booneCounty.pdf = True
booneCounty.projectedTotal = 7366
booneCounty.election = election
  
election.counties.append(booneCounty)


deKalbCounty = County()
deKalbCounty.name = "DeKalb"
deKalbCounty.url = "http://dekalb.il.clerkserve.com/wp-content/uploads/DeKalb-General-Primary-Election-Official-Results-06-28-2022-1.pdf"
deKalbCounty.pdf = True
deKalbCounty.projectedTotal = 3710
deKalbCounty.election = election
  
election.counties.append(deKalbCounty)

app = QApplication(sys.argv)
window = MainWindow(election)

window.load()
window.show()
sys.exit(app.exec())
