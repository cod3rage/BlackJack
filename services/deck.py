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
    if main == opp or (main > C.DEFAULTS.PLAY_TO and opp > C.DEFAULTS.PLAY_TO):
      return C.GAME_RESULTS.TIE
    elif (main > opp or opp > C.DEFAULTS.PLAY_TO) and main <= C.DEFAULTS.PLAY_TO:
      return C.GAME_RESULTS.WIN
    return C.GAME_RESULTS.LOSE

class Deck:
  def __init__(self):
    self.deck = []

  def clear(self):
    self.deck = []
  
  def request_draw(self, dealer:Dealer, amt = 1):
    drawn = False
    for _ in range(amt):
      v1, _ = self.value()
      if v1 < C.DEFAULTS.PLAY_TO:
        card = dealer.draw()
        if card:
          self.deck.append(card)
          drawn = True
    return drawn
  
  def evaluate(self):
    v1, v2 = self.value()
    if v1 == C.DEFAULTS.PLAY_TO or v2 == C.DEFAULTS.PLAY_TO:
      return C.DEFAULTS.PLAY_TO
    elif v2 < C.DEFAULTS.PLAY_TO:
      return v2 
    return v1
  

  def value(self, a = 0):
    val, i_val = 0, 0
    for card in self.deck[a:]:
      Cv = card['value']
      if Cv == 1:
        val   += 1
        i_val += 11
        continue
      val, i_val = val+Cv, i_val+Cv 
    return val, i_val # possiblities

