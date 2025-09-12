import pygame
from services import deck
from configs.bots import BM
from configs.constants import *

class Manager():
  running = False

  player  = deck.Deck()
  dealer  = deck.Dealer()
  entity  = deck.Deck()

  plr_turn  = False
  plr_lives = 3
  time      = 180 # in seconds

  entity_pause  = ENTITY_PAUSE_TIME
  entity_health = 3
  stay_streak   = 0
  
  click_times  = [-5,-5]
  delay = MATCH_DELAY_TIME

  config = DEFAULTS()

  def new(self):
    self.config() # update
    self.running   = True
    self.plr_lives = self.config.LIVES
    self.time      = self.config.TIMER
    #
    self.entity_lives = self.config.LIVES
    self.plr_turn = False
    #
    self.reset_match()

  def reset_match(self):
    self.dealer.reset()
    self.player.clear()
    self.player.request_draw(self.dealer, STARTING_CARDS)
    self.entity.clear()
    self.entity.request_draw(self.dealer, STARTING_CARDS)
    #
    self.delay = MATCH_DELAY_TIME
    self.entity_pause = 0
    self.stay_streak  = 0
  # --
  def binds(self, localTime = 0, mouse_pos=(0,0), lmb=False, rmb = False):
    if not self.plr_turn or not self.running: return
    #
    if lmb:
      if localTime - self.click_times[0] <= DOUBLE_CLICK:
        self.plr_turn = False
        self.click_times[0] = -5
        self.entity_pause = 0
        if not self.player.request_draw(self.dealer): # user can draw
          self.stay_streak += 1
        else:
          self.stay_streak = 0
      else:
        self.click_times[0] = localTime

    elif rmb: 
      if localTime - self.click_times[1] <= DOUBLE_CLICK:
        self.click_times[1] = -5
        self.plr_turn = False
        self.stay_streak += 1
        self.entity_pause = 0 
      else:
        self.click_times[1] = localTime

  # --
  def update(self, tick = 0, localTime = 0):
    if not self.running:
      return
    elif self.delay > 0:
      self.delay -= tick
    elif self.plr_turn:
      if self.stay_streak >= STAY_STREAK_TO_END:
        return self.match_ended()
      self.time -= tick
      print(self.player.value())
    else:
      if self.entity_pause == 0:
        choice = self.config.MODE(self.entity, self.player) # runs algorithm
        if choice == DECISION.DRAW:
          self.entity.request_draw(self.dealer)
        else: # defaults to stay
          self.stay_streak += 1
        print(self.entity.value(1))
      # --
      elif self.entity_pause + tick >= self.config.ENTITY_PAUSE:
        self.plr_turn = True
        self.entity_pause = 0
      # --
      self.entity_pause += max(MINIMAL_TICK_INTERVAL, tick)
      # ^ ensures entity goes once ^
        

  # --
  def increment(self, lives:int = None, mode:int = None, timer:int = None, playto:int = None):
    if lives:
      self.config.LIVES_INC = ( round(abs(lives)) if type(lives) == int else (self.config.LIVES_INC + 1) 
      ) % len(self.config.LIVES_SEL)
    if mode:
      self.config.MODE_INC = (((round(abs(mode))) if True else (1)) + self.config.MODE_INC) % len(BM.__modes__)
    if timer:
      self.config.TIMER_INC = ( round(abs(timer)) if type(timer) == int else(self.config.TIMER_INC+ 1) 
      ) % len(self.config.TIMER_SEL)
    if playto:
      self.config.PLAYTO_INC = ( round(abs(playto)) if type(playto) == int else(self.config.PLAYTO_INC+ 1) 
      ) % len(self.config.PLAYTO_SEL)
    
    self.config()
  
  # --
  def match_ended(self):
    results = self.dealer.compare(
      self.player.evaluate(), 
      self.entity.evaluate()
    )

    if results == GAME_RESULTS.WIN:
      self.entity_lives -= 1
      self.plr_turn = True
      print('WON')
    elif results == GAME_RESULTS.LOSE:
      self.plr_lives -= 1
      self.plr_turn = False
      print('LOST')
    else:
      print('TIE')
      self.plr_turn = False

    print(f'{self.config.LIVES - self.entity_lives} : {self.config.LIVES - self.plr_lives}\n{self.player.evaluate()} | {self.entity.evaluate()}')

    self.reset_match()


  