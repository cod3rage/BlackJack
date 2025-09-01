from services import deck
from configs.constants import *

class Manager():
  running = False

  player  = deck.Deck()
  stack   = deck.Dealer()
  entity  = deck.Deck()

  plr_turn  = False
  plr_lives = 3
  time      = 180 # in seconds

  stay_streak = 0
  
  click_times  = (-5,-5)

  config = DEFAULTS()

  def new(self):
    self.config() # update
    self.running = True
    self.plr_lives = self.config.LIVES
    self.time      = self.config.TIMER

  # --
  def binds(self, localTime = 0, events=None, mouse_pos=(0,0), lmb_click=False):
    pass

  # --
  def update(self, tick = 0, localTime = 0):
    self.increment(mode = True)
    print(self.config.MODE)
    self.run()

  # --
  def increment(self, lives:int = None, mode:int = None, timer:int = None, playto:int = None):
    if lives:
      self.config.LIVES_INC = ( round(abs(lives)) if type(lives) == int else (self.config.LIVES_INC+ 1) 
      ) % len(self.config.LIVES_SEL)
    if mode:
      self.config.MODE_INC = ( round(abs(mode)) if type(mode) == int else(self.config.MODE_INC+ 1) 
      ) % len(BM.__modes__)
    if timer:
      self.config.TIMER_INC = ( round(abs(timer)) if type(timer) == int else(self.config.TIMER_INC+ 1) 
      ) % len(self.config.TIMER_SEL)
    if playto:
      self.config.PLAYTO_INC = ( round(abs(playto)) if type(playto) == int else(self.config.PLAYTO_INC+ 1) 
      ) % len(self.config.PLAYTO_SEL)
    
    self.config()

  