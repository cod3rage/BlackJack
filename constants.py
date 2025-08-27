from enum import Enum

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
PLAY_TO      = 21 # goal to get
CARDS        = ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King']
SHAPES       = ['Spade','Heart','Club','Diamond']

# dependent values
SCREEN_X, SCREEN_Y  = SCREEN_SIZE
HALF_X  , HALF_Y    = SCREEN_X/2, SCREEN_Y/2
# 
CARD_LEN, SHAPE_LEN = len(CARDS), len(SHAPES)


# enums
class GAME_RESULTS(Enum):
  LOSE, WIN, TIE =  0, 1, 2