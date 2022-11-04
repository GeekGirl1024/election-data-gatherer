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


election = Election()

lakeCounty = County()
lakeCounty.name = "Lake"
lakeCounty.clarify = True
lakeCounty.url = "https://results.enr.clarityelections.com/IL/Lake/114135/300541/reports/detailxml.zip"
lakeCounty.contestName = "Representative in Congress Eleventh Congressional District"
  
election.counties.append(lakeCounty)

dupageCounty = County()
dupageCounty.name = "Dupage"
dupageCounty.clarify = True
dupageCounty.url = "https://www.dupageresults.gov//IL/DuPage/114213/300666/reports/detailxml.zip"
dupageCounty.contestName = "FOR REPRESENTATIVE IN CONGRESS 11TH CONGRESSIONAL DISTRICT"
  
  
election.counties.append(dupageCounty)

willCounty = County()
willCounty.name = "Will"
willCounty.clarify = True
willCounty.url = "https://results.enr.clarityelections.com//IL/Will/114217/300664/reports/detailxml.zip"
willCounty.contestName = "REPRESENTATIVE IN CONGRESS 11TH CONGRESSIONAL DISTRICT"
  
election.counties.append(willCounty)

mcHenryCounty = County()
mcHenryCounty.name = "McHenry"
mcHenryCounty.clarify = True
mcHenryCounty.url = "https://results.enr.clarityelections.com//IL/McHenry/115186/301334/reports/detailxml.zip"
mcHenryCounty.contestName = "REPRESENTATIVE IN CONGRESS 11th CONGRESSIONAL DISTRICT"

election.counties.append(mcHenryCounty)

cookCounty = County()
cookCounty.name = "Cook"
cookCounty.url = "https://results622.cookcountyclerkil.gov/Home/Detail?contestId=203"

  
election.counties.append(cookCounty)

kaneCounty = County()
kaneCounty.name = "Kane"
kaneCounty.url = "http://electionresults.countyofkane.org/Contests.aspx?Id=26"

  
election.counties.append(kaneCounty)

booneCounty = County()
booneCounty.name = "Boone"
booneCounty.url = "https://www.boonecountyil.gov/Departments/Clerk-Recorder/voting/2022_jun_28_il_boone_SOVC.pdf"

  
election.counties.append(booneCounty)


deKalbCounty = County()
deKalbCounty.name = "DeKalb"
deKalbCounty.url = "http://dekalb.il.clerkserve.com/wp-content/uploads/DeKalb-General-Primary-Election-Official-Results-06-28-2022-1.pdf"

  
election.counties.append(deKalbCounty)

app = QApplication(sys.argv)
window = MainWindow(election)

window.load()
window.show()
sys.exit(app.exec())
