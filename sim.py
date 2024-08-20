class PlayerState():
  def __init__(self, name):
    self.drawDeck : list[Card] = []
    self.discardDeck : list[Card] = []
    self.hand : list[Card] = []
    self.board : list[Card | None] = [None, None, None, None]
    self.name = name
    self.hp : int = 20
    self.mana : int = 0
    self.winstate = 0
  def remove(self, slot: int):
    # TODO: handle backdrop
    assert self.board[slot] is not None
    self.board[slot] = None
  def deploy(self, slot: int, card: Card):
    assert self.board[slot] is None
    self.board[slot] = card
    self.board[slot].onDeploy(slot)
  def attack(self, slot: int, dmg: int):
    if self.board[slot] is not None:
      self.board[slot].onDamage(dmg)
    else:
      self.hp -= dmg
      if self.hp <= 0:
        self.winstate = -1
  def prompt(self, v: str):
    return input(f"[{self.name}] {v} ")
  def output(self, v: str):
    print(f"[{self.name}] {v}")

class Card():
  def __init__(self, owner : PlayerState, opponent : PlayerState):
    self.hp : int = 0
    self.cost : int = 0
    self.strength : int = 0
    self.name = ""
    self.desc = ""
    
    self.owner : PlayerState = owner
    self.opponent : PlayerState = opponent
    self.slot = -1
    pass
  def _stat(self, hp : int, cost : int, strength : int, name : str, desc : str):
    self.hp, self.cost, self.strength, self.name, self.desc = hp, cost, strength, name, desc
  def canBePlayed(self) -> bool:
    if self.slot != -1:
      return False
    if self.cost > self.owner.mana:
      return False
    return True
  def onDeploy(self, slot : int):
    assert self.slot == -1
    self.slot = slot
    self.owner.mana -= self.cost
  def onDestroy(self):
    self.owner.remove(self.slot)
  def onDamage(self, dmg : int):
    self.hp -= dmg
    if self.hp <= 0:
      self.onDestroy()
  def onAttackPhase(self):
    assert self.slot != -1
    self.opponent.attack(self.slot, self.strength)
  def onTurnBegin(self):
    pass
  def onPlacementPhase(self):
    pass
  def onTurnEnd(self):
    pass

class BeeCard(Card):
  def __init__(self, owner : PlayerState, opponent : PlayerState):
    super().__init__(owner, opponent)
    self._stat(2, 1, 1, "Bee", "This card has no special rules.")

class RealCategoryTheoristCard(Card):
  def __init__(self, owner : PlayerState, opponent : PlayerState):
    super().__init__(owner, opponent)
    self._stat(4, 3, 1, "real category theorist", "If any card, including the owner's and excluding this one, has the word “set” in its text, it is immediately killed upon this card being played.")
  def onDeploy(self, slot: int):
    super().onDeploy(slot)
    for i in [self.owner, self.opponent]:
      for c in i.board:
        if c is not None and type(c) is not RealCategoryTheoristCard and "set" in c.desc:
          # kill