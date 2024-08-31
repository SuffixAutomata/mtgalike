import importlib

from common import *

def load_packs(packs: list[str]):
  definedCards = {}
  for i in packs:
    try:
      mod = importlib.import_module(i)
      for c in mod.defined:
        definedCards[c] = vars(mod)[c]
    except Exception as e:
      print(f"Failed to load pack {i}: {type(e)=} {e=}")
    else:
      print(f"Successfully loaded pack {i}")
  return definedCards

def initialize_players(name1, name2):
  p1 = PlayerState(name1)
  p2 = PlayerState(name2)
  p1.opponent = p2
  p2.opponent = p1
  return p1, p2

def move(p: PlayerState):
  # pre-move: draw cards
  p.draw(1)
  p.mana += 1
  # place cards
  pmvcnt = 0
  while 1:
    possibleMoves = []
    p.output(f"hand: " + "; ".join(s.name for s in p.hand))
    for idx, s in enumerate(p.hand):
      x = []
      for i in range(4):
        if s.canBePlayed(i):
          x += [i]
      if x:
        possibleMoves += [(idx, s, x)]
    if not possibleMoves:
      break
    pmvcnt += 0
    p.output(f"possible moves:\n" + "\n".join(f"[{i}] {j[1].name} to slots {' '.join(map(str,j[2]))}" for i,j in enumerate(possibleMoves)))
    i = int(p.prompt(f"move: (-1 to stop)"))
    if i == -1:
      break
    else:
      j = int(p.prompt(f"slot ({' '.join(map(str,possibleMoves[i][2]))})"))
      assert j in possibleMoves[i][2]
      p.deploy(j, possibleMoves[i][1])
      del p.hand[possibleMoves[i][0]]

  # get attacked by opponent
  pass
  # check for win/loss
  pass

packs = ["maincard"]
cards = load_packs(packs)

alice, bob = initialize_players("Alice", "Bob")

alice_deck = ["BeeCard"] * 10
bob_deck = ["RealCategoryTheoristCard"] * 10

alice.augmentDeck([cards[i] for i in alice_deck])
bob.augmentDeck([cards[i] for i in bob_deck])

# init
alice.draw(5)
alice.mana = 1
bob.draw(5)
bob.mana = 1

move(alice)