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

packs = ["maincard"]
print(load_packs(packs))

alice, bob = initialize_players("Alice", "Bob")