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
  if len(p.hand) <= 2:
    p.draw(2)
  else:
    p.draw(1)
  p.mana += 1
  # place cards
  pmvcnt = 0
  p.output(f"mana: {p.mana}")
  p.renderHand()
  if int(p.prompt("reshuffle hand? [0|1]")):
    p.reshuffleHand(5)
    p.renderHand()
  while 1:
    possibleMoves = []
    if pmvcnt:
      p.renderHand()
    for idx, s in enumerate(p.hand):
      x = []
      for i in range(4):
        if s.canBePlayed(i):
          x += [i]
      if x:
        possibleMoves += [(idx, s, x)]
    if not possibleMoves:
      break
    pmvcnt += 1
    p.output("possible moves:\n" + "\n".join(f"[{i}] {j[1].name} to slots {' '.join(map(str,j[2]))}" for i,j in enumerate(possibleMoves)))
    i = int(p.prompt("move: (-1 to stop)"))
    if i == -1:
      break
    else:
      j = int(p.prompt(f"slot ({' '.join(map(str,possibleMoves[i][2]))})"))
      assert j in possibleMoves[i][2]
      p.deploy(j, possibleMoves[i][1])
      del p.hand[possibleMoves[i][0]]
  if pmvcnt == 0 and any(x is None for x in p.board):
    p.output("no moves & empty slot")
    p.mana += 1
  # get attacked by opponent
  for i in range(4):
    if p.opponent.board[i] is not None:
      p.opponent.board[i].onAttackPhase()
  p.output(f"new hp: {p.hp}")

def checkwinloss(alice : PlayerState, bob : PlayerState):
  if alice.winstate != 0 or bob.winstate != 0:
    if alice.winstate != 0:
      print(f"{alice.name} {'won' if alice.winstate==1 else 'lost'}")
    if bob.winstate != 0:
      print(f"{bob.name} {'won' if bob.winstate==1 else 'lost'}")
    exit(0)

def run(packs, n1, n2):
  cards = load_packs(packs)
  print("available cards:")
  for i in cards:
    print(i, (lambda k: f"{k.name} {k.hp} {k.cost} {k.strength}\n  {k.desc}")(cards[i](None)))
  alice, bob = initialize_players(n1, n2)
  alice.onGameStart(cards)
  bob.onGameStart(cards)
  while 1:
    move(alice)
    checkwinloss(alice, bob)
    move(bob)
    checkwinloss(alice,bob)

if __name__ == "__main__":
  a, b = input("player names: ").split()
  run(["maincard"], a, b)