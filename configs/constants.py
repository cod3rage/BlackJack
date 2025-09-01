from enum import Enum
from configs import bots


# misc
SECOND_INCREMENT = 30

# window settings
SCREEN_SIZE = (800, 600)
FRAME_RATE  = 60
APP_NAME    = 'BlackJack'


# camera settings
SCROLL_AMT       = 67
SHAKE_STRENGTH   = 1.3


# binding
DOUBLE_CLICK = 0.4 # seconds for double click

# cards
CARDS        = ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King']
SHAPES       = ['Spade','Heart','Club','Diamond']

# dependent values
SCREEN_X, SCREEN_Y  = SCREEN_SIZE
HALF_X  , HALF_Y    = SCREEN_X/2, SCREEN_Y/2
# 
CARD_LEN, SHAPE_LEN = len(CARDS), len(SHAPES)

# game settings
MAX_TIMER_LENGTH = 240
MAX_LIVES   = 5
MAX_PLAY_TO = 27
MIN_PLAY_TO = 17
#
ENTITY_PAUSE_TIME  = 4
STAY_STREAK_TO_END = 3


# enums
class GAME_RESULTS(Enum):
  LOSE, WIN, TIE =  0, 1, 2

class BM(Enum):
  # algorithems
  NORMAL    = bots.normal
  HARD      = bots.hard
  HAUNTING  = bots.haunting
  PARANOIA  = bots.paranoia

  __modes__ = [NORMAL, HARD, HAUNTING, PARANOIA]


class DEFAULTS(): # default match settings
  TIMER   = 90     # 1m30s
  PLAY_TO = 21     # cards to play to
  LIVES   = 3      # 3 lives...
  MODE    = BM.NORMAL # int 0
  # Incremented selections
  PLAYTO_SEL = [21, 17, 24, 27]
  LIVES_SEL  = [3, 4, 5, 1, 2]
  TIMER_SEL  = [90, 120, 150, 180, 30, 60]
  # sets default
  LIVES_INC = MODE_INC = PLAYTO_INC = TIMER_INC = 0
  # update
  def __call__(self):
    self.LIVES   = self.LIVES_SEL[self.LIVES_INC]
    self.MODE    = BM.__modes__[self.MODE_INC]
    self.PLAY_TO = self.PLAYTO_SEL[self.PLAYTO_INC]
    self.TIMER   = self.TIMER_SEL[self.TIMER_INC]
    #

