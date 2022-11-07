from datetime import datetime


from candidate import Candidate

class Result:
  def __init__(self):
    self.downloadTime = datetime.now()
    self.updateTime = ""
    self.hash = ""
    self.fileName = ""
    self.error = False
    self.democrat = Candidate()
    self.democrat.name = "Bill"
    self.republican = Candidate()
    self.republican.name = "Catalina"
    self.other = Candidate()
    self.other.name = "Other"
