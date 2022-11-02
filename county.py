from datetime import datetime
from candidate import Candidate
from result import Result
class County:
  def __init__(self):
    self.timestamp = datetime.now()
    self.clarify = False
    self.name = ""
    self.contestName = ""
    self.results = []
  
  def getCurrentResults(self) :
    
    returnResult = Result()
    resultCount = len(self.results)
    if (resultCount != 0):
      latestResult = self.results[resultCount - 1]
      returnResult.democrat.votes = latestResult.democrat.votes
      returnResult.republican.votes = latestResult.republican.votes
      returnResult.other.votes = latestResult.other.votes

    return returnResult
