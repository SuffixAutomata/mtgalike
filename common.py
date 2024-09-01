from __future__ import annotations

import random

# Slots
# [Alice] 0 1 2 3
# [Bob]   3 2 1 0

class PlayerState():
  def __init__(self, name):
    self.drawDeck : list[Card] = []
    self.discardDeck : list[Card] = []
    self.hand : list[Card] = []
    self.board : list[Card | None] = [None, None, None, None]
    self.name : str = name
    self.hp : int = 0
    self.mana : int = 0
    self.winstate = 0
    self.opponent : PlayerState | None = None
  def remove(self, slot: int):
    # TODO: handle backdrop
    assert self.board[slot] is not None
    self.board[slot].resetStats()
    self.discardDeck.append(self.board[slot])
    self.board[slot] = None
  def deploy(self, slot: int, card: Card):
    assert self.board[slot] is None
    self.board[slot] = card
    self.board[slot].onDeploy(slot)
  def getAttacked(self, slot: int, dmg: int):
    slot = 3 - slot # swap
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
  def augmentDeck(self, cardTypes):
    for i in cardTypes:
      self.drawDeck.append(i(self))
    random.shuffle(self.drawDeck)
  def draw(self, cnt: int):
    assert cnt <= len(self.drawDeck)
    self.hand += self.drawDeck[:cnt]
    self.drawDeck = self.drawDeck[cnt:]
  def renderHand(self):
    self.output(f"hand: " + "; ".join(s.name for s in self.hand))
  def renderBoard(self):
    s = "board:\n"
    s += f"{self.opponent.name}: {';'.join(str(x) for x in self.opponent.board[::-1])}\n"
    s += f"sellf: {';'.join(str(x) for x in self.board)}"
    self.output(s)
  def reshuffleHand(self, cnt: int):
    self.drawDeck += self.hand
    self.hand = []
    random.shuffle(self.drawDeck)
    self.draw(cnt)
  def onGameStart(self, cards):
    deck = []
    while 1:
      v = self.prompt("add to deck: [card amnt | -1]")
      if v == "-1":
        break
      else:
        a, b = v.split()
        if a not in cards:
          self.output(f"{a} not a card")
        else:
          deck += [a] * int(b)
          self.output(f"added {b} copies of {a} into deck")
    self.augmentDeck([cards[i] for i in deck])
    self.draw(5)
    self.hp = 20
    self.mana = 1

class Card():
  def __init__(self, owner : PlayerState):
    self.hp : int = 0
    self.cost : int = 0
    self.strength : int = 0
    self.name = ""
    self.desc = ""
    self.ini = None
    
    self.owner : PlayerState = owner
    if owner is not None:
      self.opponent : PlayerState = self.owner.opponent
    self.slot = -1
    pass
  def __str__(self):
    return self.name
  def _stat(self, hp : int, cost : int, strength : int, name : str, desc : str):
    self.ini = (hp, cost, strength)
    self.hp, self.cost, self.strength, self.name, self.desc = hp, cost, strength, name, desc
  def resetStats(self):
    self.slot = -1
    self.hp, self.cost, self.strength = self.ini
  def canBePlayed(self, slot : int) -> bool:
    if self.slot != -1:
      return False
    if self.cost > self.owner.mana:
      return False
    if self.owner.board[slot] != None:
      return False
    return True
  def onDeploy(self, slot : int):
    assert self.slot == -1
    self.slot = slot
    self.owner.mana -= self.cost
  def onDestroy(self, reason: str):
    self.owner.remove(self.slot)
  def onDamage(self, dmg : int):
    self.hp -= dmg
    if self.hp <= 0:
      self.onDestroy("damage")
  def onPreMovePhase(self):
    pass
  def onAttackPhase(self):
    assert self.slot != -1
    self.opponent.getAttacked(self.slot, self.strength)
  def onTurnBegin(self):
    pass
  def onPlacementPhase(self):
    pass
  def onTurnEnd(self):
    pass