from datetime import datetime


from candidate import Candidate

class Results:
  

  def __init__(self):
    self.timestamp = datetime.now()
    self.democrat = Candidate()
    self.democrat.name = "Bill"
    self.republican = Candidate()
    self.republican.name = "Catalina"
    self.other = Candidate()
    self.other.name = "Other"
