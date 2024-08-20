class PlayerState():
  def __init__(self, name):
    self.drawDeck : list[Card] = []
    self.discardDeck : list[Card] = []
    self.hand : list[Card] = []
    self.board : list[Card] = []
    self.name = name
  def prompt(self, v: str):
    return input(f"[{self.name}] {v} ")
  def output(self, v: str):
    print(f"[{self.name}] {v}")

class Card:
  def __init__(self):
    pass
  def canBePlayed(self) -> bool:
    return True
  def onTurnBegin(self):
    pass
  def onTurnEnd(self):
    pass