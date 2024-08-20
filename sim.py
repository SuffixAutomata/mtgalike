class PlayerState():
  def __init__(self):
    self.drawDeck : list[Card] = []
    self.discardDeck : list[Card] = []
    self.hand : list[Card] = []
    self.hand : list[Card] = []

class Card:
  def __init__(self):
    pass
  def canBePlayed(self) -> bool:
    return True
  def onTurnBegin(self):
    pass
  def onTurnEnd(self):
    pass