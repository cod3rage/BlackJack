import pygame
from services import deck
from configs.bots import BM
from configs.constants import *

class Manager():
  running   = False
  queue_end = False

  config = DEFAULTS()

  player  = deck.Deck(config)
  entity  = deck.Deck(config)
  dealer  = deck.Dealer(config)

  plr_turn  = False
  plr_lives = 3
  time      = 180 # in seconds

  entity_pause  = ENTITY_PAUSE_TIME
  entity_drew   = False
  entity_lives  = plr_lives
  stay_streak   = 0
  
  click_times  = [-5,-5]
  delay = MATCH_DELAY_TIME

  def new(self):
    self.config() # update
    self.running   = True
    self.plr_lives = self.config.LIVES
    self.time      = self.config.TIMER
    #
    self.entity_lives = self.config.LIVES
    self.plr_turn = False
    self.queue_end = False
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
    self.entity_drew = False
  # --
  def binds(self, localTime = 0, mouse_pos=(0,0), lmb=False, rmb = False):
    if not self.plr_turn or not self.running or self.delay > 0: return
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
    return True

  # --
  def update(self, tick = 0, *_):
    if not self.running:
      return
    elif self.delay > 0:
      self.delay -= tick
      if self.queue_end and self.delay <= 0:
        self.running = False
        return
    elif self.plr_turn:
      if self.stay_streak >= STAY_STREAK_TO_END:
        return self.match_ended()
      self.time -= tick
      if self.time <= 0:
        return self.end_game(GAME_RESULTS.LOSE)
    else:
      if self.entity_pause + tick >= (self.config.ENTITY_PAUSE * 0.5) > self.entity_pause:
        choice = self.config.MODE(self.entity, self.player, self.config.PLAY_TO) # runs algorithm
        if choice == DECISION.DRAW:
          if not self.entity.request_draw(self.dealer):
            self.stay_streak += 1
        else: # defaults to stay
          self.stay_streak += 1
        self.entity_drew = True
      # --
      elif self.entity_pause + tick >= self.config.ENTITY_PAUSE:
        self.plr_turn = True
        self.entity_drew = False
        self.entity_pause = 0
        if self.stay_streak >= STAY_STREAK_TO_END:
          self.match_ended()
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
    elif results == GAME_RESULTS.LOSE:
      self.plr_lives -= 1
      self.plr_turn = False
    else:
      self.plr_turn = False

    if self.plr_lives <= 0:
      return self.end_game(GAME_RESULTS.LOSE)
    elif self.entity_lives <= 0:
      return self.end_game(GAME_RESULTS.WIN)


    self.reset_match()

  def end_game(self, match:GAME_RESULTS):
    self.queue_end = True
    self.delay = MATCH_DELAY_TIME

  