this project aims to simulate a MTG-like card game my friends made

with modding.

with a lot of modding.

---

Sigils:
EPH: This card can be played in occupied spaces. After the events specified in the text have occurred, or immediately if there are none, this card is to be discarded. It is assumed by default that the events specified in the text occur immediately when the card is played.
LETH: An attack from a card with this will always kill a card, regardless of its health or the damage dealt.
PIRC: An attack from a card will still hit the opponent after hitting any cards that would otherwise block it
SHLD: If this card would for any reason die, remove Shielded from it instead. If the attack resulting in this depleted health from this card, said health is restored.
IMMR: This card cannot die, for any reason, superseding all card text where possible.
STUN: When a card with this sigil is placed on the board, the card opposite to it (if present) is prevented from attacking this turn.
BACK: One (non-backdrop) card can be placed on top of this card however a card normally would be. This card will not be attacked or attack itself if it has a card on top of it.
PAS: This card does not attack and is ignored for the purpose of attack targeting.
TOXn: If this card is killed by a normal attack from another card, the attacker takes n damage. If n is ∞, the attacker dies immediately.
2FUR: This card will not attack the opposite card. When it attacks, it will attack the opposite card's two neighbouring spaces, first the left one and then the right one (from the opponent's POV). If these spots are empty the opponent will be struck instead, as usual.
3FUR: Like the above, but it will also hit the opposite space after the left neighbour.
4FUR: This one hits all four spaces on the board from left to right (opponent's POV).
FRA: If this card has health, any incoming damage to this card will be amplified to its current health, no matter what.
2STR: This card will attack twice consecutively where it would otherwise attack once.
ARMR: If incoming normal attack damage is less than 2, it is reduced to 0. This overrides Fragile.

attributes to take care of:
visibly human, visibly male, visibly rock, visibly paper