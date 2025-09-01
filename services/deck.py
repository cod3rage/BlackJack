from random import randint
from configs.constants import *

def card_vector(shape = 0, card = 0):
  crd, shp = CARDS[card], SHAPES[shape]
  return {
    'shape'     : shape,
    'card'      : card,
    'card_name' : crd,
    'shape_name': shp,
    'value'     : min(card + 1, 10),
    'name'      : f'{crd} of {shp}s',
    'file'      : f'{crd.lower()}_of_{shp.lower()}s.png'
  }

def compare(main:int, opp:int) -> GAME_RESULTS:
  if main == opp or (main > DEFAULTS.PLAY_TO and opp > DEFAULTS.PLAY_TO):
    return GAME_RESULTS.TIE
  elif (main > opp or opp > DEFAULTS.PLAY_TO) and main <= DEFAULTS.PLAY_TO:
    return GAME_RESULTS.WIN
  return GAME_RESULTS.LOSE

class Dealer:
  def __init__(self):
    self.deck  = []
  
  def shuffle(self):
    size = len(self.deck)
    for i in range(size):
      randPos  = randint(0, size - 1)
      tempCard = self.deck[randPos]
      self.deck[randPos] = self.deck[i]
      self.deck[i] = tempCard

  def draw(self):
    size = len(self.deck)
    if size <= 0:
      return None
    #
    (shape, card) = self.deck[-1]
    self.deck.pop(-1)
    
    return card_vector(shape, card)

  def add_card(self, shape:int = 0, card:int = 0):
    self.deck.append((
      min( abs(round(shape)) , SHAPE_LEN), 
      min( abs(round(card))  , CARD_LEN)
    ))

  def reset(self):
    self.deck = []
    for shape in range(SHAPE_LEN):
      for card in range(CARD_LEN):
        self.add_card(shape, card)
    self.shuffle()

class Deck:
  def __init__(self):
    self.deck = []

  def clear(self):
    self.deck = []
  
  def request_draw(self, dealer:Dealer):
    v1, _ = self.value()
    if v1 < DEFAULTS.PLAY_TO:
      card = dealer.draw()
      if card:
        self.deck.append(card)
  
  def evaluate(self):
    v1, v2 = self.value()
    if v1 == DEFAULTS.PLAY_TO or v2 == DEFAULTS.PLAY_TO:
      return DEFAULTS.PLAY_TO
    elif v2 < DEFAULTS.PLAY_TO:
      return v2 
    return v1

  def value(self):
    val, i_val = 0, 0
    for card in self.deck:
      Cv = card['value']
      if Cv == 1:
        val   += 1
        i_val += 11
        continue
      val, i_val = val+Cv, i_val+Cv 
    return val, i_val # possiblities

