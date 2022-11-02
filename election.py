class Election:

  def __init__(self):
    self.name = ""
    self.counties = []
    self.democratTotal = 0
    self.republicanTotal = 0

  def getCurrentState(self):
    democrat = 0
    republican = 0
    for county in self.counties:
      resultsCount = len(county.results)
      if resultsCount > 0 :
        democrat += (county.results[resultsCount-1]).democrat.votes
        republican += (county.results[resultsCount-1]).republican.votes
    self.democratTotal = democrat
    self.republicanTotal = republican
