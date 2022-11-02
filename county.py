from datetime import datetime
from candidate import Candidate
from results import Results
class County:
  timestamp = datetime.now()
  clarify = False
  name = ""
  contestName = ""
  results = []
  #results = [Results()]
  def __init__(self):
    self.timestamp = datetime.now()
    self.clarify = False
    self.name = ""
    self.contestName = ""
    self.results = []
