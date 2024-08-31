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

defined = ["BeeCard", "RealCategoryTheoristCard"]