from random import randint
from configs import constants as C



def card_vector(shape = 0, card = 0):
  crd, shp = C.CARDS[card], C.SHAPES[shape]
  return {
    'shape'     : shape,
    'card'      : card,
    'card_name' : crd,
    'shape_name': shp,
    'value'     : min(card + 1, 10),
    'name'      : f'{crd} of {shp}s',
    'file'      : f'{crd.lower()}_of_{shp.lower()}s.png',
  }


class Dealer:
  def __init__(self, config = None):
    self.deck  = []
    self.config = config
  
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
      min( abs(round(shape)) , C.SHAPE_LEN), 
      min( abs(round(card))  , C.CARD_LEN)
    ))

  def reset(self):
    self.deck = []
    for shape in range(C.SHAPE_LEN):
      for card in range(C.CARD_LEN):
        self.add_card(shape, card)
    self.shuffle()
  
  def compare(self, main:int, opp:int):
    if main == opp or (main > self.config.PLAY_TO and opp > self.config.PLAY_TO):
      return C.GAME_RESULTS.TIE
    elif (main > opp or opp > self.config.PLAY_TO) and main <= self.config.PLAY_TO:
      return C.GAME_RESULTS.WIN
    return C.GAME_RESULTS.LOSE

class Deck:
  def __init__(self, config = None):
    self.config = config or C.DEFAULTS
    self.deck = []

  def clear(self):
    self.deck = []
  
  def request_draw(self, dealer:Dealer, amt = 1):
    drawn = False
    for _ in range(amt):
      v = self.evaluate()
      if v < self.config.PLAY_TO:
        card = dealer.draw()
        if card:
          self.deck.append(card)
          drawn = True
    return drawn
  
  def evaluate(self):
    vals = self.value()
    closest = vals[0]
    for i in vals[1:]:
      if closest < i <= self.config.PLAY_TO:
        closest = i
    return closest
  

  def value(self):
    options = [0]
    for card in self.deck:
      size = len(options)
      for i in range(size):
        options[i] += max(1,card['value'])
      if card['card'] == 0:
        options *= 2
        for i in range(size, size * 2):
          options[i] += 11
      
    return tuple(options) # possiblities

