from services import deck
from configs import constants as C
from enum import Enum



# -- ALGORITHMS -- #

def normal(self:deck.Deck, plr:deck.Deck, play_to = 21): 
  # checks self if value is above or equal to 17 (80% of 21) to stay
  if self.evaluate() < round(play_to * 0.80):
    return C.DECISION.DRAW
  return C.DECISION.STAY



def hard(self:deck.Deck, plr:deck.Deck, play_to = 21):
  # +1 for vals 2-5, -1 for vals 8+ (including aces)
  count, value = 0, 0

  # loops through own cards
  for card in self.deck:
    val = card['value']
    value += val
    if 1 < val <= 5:
      count += 1
    elif val >= 8 or val == 1:
      count -= 1

  # loops every card BUT the first one
  for card in plr.deck[1:]:
    val = card['value']
    value += val
    if 1 < val <= 5:
      count += 1
    elif val >= 8 or val == 1:
      count -= 1

  # difference for self to win
  diff = play_to - self.evaluate()

  # Neutral values arn't counted
  # Won't risk anything less than 4
  if count == 0 or diff < 4:
    return C.DECISION.STAY

  if (diff <= 6 and count < 0) or (diff >= 10) or (diff >= 7 and count >= 0):
    return C.DECISION.DRAW

  # fail safe
  return C.DECISION.STAY




def haunting(*_):
  # card counts to guess other players card chances and evaluates self
  return C.DECISION.STAY




def paranoia(*_):
  return C.DECISION.STAY




# organizer
class BM(Enum):
  # algorithems
  NORMAL    = normal
  HARD      = hard
  HAUNTING  = haunting
  PARANOIA  = paranoia

  # for tabbing between them
  __modes__ = [NORMAL, HARD, HAUNTING, PARANOIA]
