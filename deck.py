from random import randint

CARDS  = ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King']
SHAPES = ['Spade','Heart','Club','Diamond']

class Deck:
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
    card_data = {
      'shape'     : shape,
      'card'      : card,
      'card_name' : CARDS[card],
      'shape_name': SHAPES[shape],
      'value'     : min(card + 1, 10),
      'name'      : f'{CARDS[card]} of {SHAPES[shape]}s'
    }
    return card_data

  def add_card(self, shape:int = 0, card:int = 0):
    self.deck.append((
      min( abs(round(shape)) , len(SHAPES) ), 
      min( abs(round(card))  , len(CARDS)  )
    ))

  def reset(self):
    self.deck = []
    for shape in range(len(SHAPES)):
      for card in range(len(CARDS)):
        self.add_card(shape, card)
    self.shuffle()
  


