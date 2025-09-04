from services import deck
from configs import constants as C
from enum import Enum



# -- ALGORITHMS -- #

def normal(self:deck.Deck, *_): 
  # checks self if value is above or equal to 17 to stay
  if self.evaluate() < 17:
    return C.DECISION.DRAW
  return C.DECISION.STAY



def hard(*_):
  # 
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

  __modes__ = [NORMAL, HARD, HAUNTING, PARANOIA]
