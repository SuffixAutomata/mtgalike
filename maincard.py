from common import *

class BeeCard(Card):
  def __init__(self, owner : PlayerState):
    super().__init__(owner)
    self._stat(2, 1, 1, "Bee", "This card has no special rules.")

class RealCategoryTheoristCard(Card):
  def __init__(self, owner : PlayerState):
    super().__init__(owner)
    self._stat(4, 3, 1, "real category theorist", "If any card, including the owner's and excluding this one, has the word “set” in its text, it is immediately killed upon this card being played.")
  def onDeploy(self, slot: int):
    super().onDeploy(slot)
    for i in [self.owner, self.opponent]:
      for idx, c in enumerate(i.board):
        if c is not None and type(c) is not RealCategoryTheoristCard and "set" in c.desc:
          # sanity check
          assert c.slot == idx
          c.onDestroy()

#  | 0 | | BACK-PAS | Farm | At the beginning of your turn, if this card is on the board, you gain one mana. This card will not produce mana if there is a card on top of it.

class FarmCard(Card):
  def __init__(self, owner: PlayerState):
    super().__init__(owner)
    raise NotImplementedError

# 1 | 2 | | TOX1 | Jar of Poison |

class JarOfPoisonCard(Card):
  def __init__(self, owner: PlayerState):
    super().__init__(owner)
    self._stat(1, 2, 0, "Jar of Poison", "(TOX1)")
  def onDestroy(self, reason: str):
    if reason == "damage":
      self.opponent.getAttacked(self.slot, 1) #TOX1
    self.owner.remove(self.slot)

# 1 | 2 | 1 | 2FUR | extremely pointy grass

class ExtremelyPointyGrassCard(Card):
  def __init__(self, owner: PlayerState):
    super().__init__(owner)
    self._stat(1, 2, 1, "extremely pointy grass", "(2FUR)")
  def onAttackPhase(self):
    assert self.slot != -1
    self.opponent.getAttacked((self.slot-1)%4, self.strength)
    self.opponent.getAttacked((self.slot+1)%4, self.strength)

class TankCard(Card):
  def __init__(self, owner: PlayerState):
    super().__init__(owner)
    self._stat(6, 4, 2, "Tank", "Get it? It's like, a tank, and it has high HP, which is kind of like the thing,")

defined = ["BeeCard", "RealCategoryTheoristCard", "JarOfPoisonCard", "ExtremelyPointyGrassCard", "TankCard"]