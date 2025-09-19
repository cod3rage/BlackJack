from services import interface as Ui, tween
from configs.UIObjects import *
from configs.constants import *

tws = tween.TweenSys()


# ----------------
class GuiManager():
  UiMain    = Ui.UIObj('UIMain')    # camera shake
  UiOverlay = Ui.UIObj('UIOverlay') # no camera shake
  SttgsSect = UiMain.new(Ui.UIObj, 'SettingsSection')
  BindsSect = UiMain.new(Ui.UIObj, 'BindsSection')

  UiMain.visible    = False
  UiOverlay.visible = False
  SttgsSect.visible = False
  BindsSect.visible = False
  SttgsSect.position = (50, SCREEN_Y - 144)
  BindsSect.position = (SCREEN_X - 50, SCREEN_Y - 104)
  #
  clickEffoc = UiMain.new(ClickEffect, 'ClickEffect', 20)# without my coffee I dont give effoc
  clickEffoc.color = (153,153,153)
  clickEffoc()
  #
  BindYeild  = False
  # listeners
  PlayCaught  = False
  Drew_check  = False
  PlrTurn     = True
  DelayCaught = False
  LifeCounter = [0,0]

  def __init__(self, game_manager):
    self.manager = game_manager
    self.config  = self.manager.config
    self.playbttn = self.UiMain.new(PlayBttn, 'PlayBttn', game_manager)
    self.playbttn.position = (HALF_X, SCREEN_Y - 80)
    #
    self.lives = self.SttgsSect.new(SettingsBttn, 'LIVES', game_manager, 'assets/UI/Heart.png')
    self.lives.static   = False
    self.lives.position = (0,48)
    self.lives.suffix = ' Lives' 
    self.timer = self.SttgsSect.new(SettingsBttn, 'TIMER', game_manager, 'assets/UI/Clock.png')
    self.timer.static   = False
    self.timer.position = (0,72)
    self.timer.suffix = 's'
    self.playto = self.SttgsSect.new(SettingsBttn, 'PLAY_TO', game_manager, 'assets/UI/Star.png')
    self.playto.static   = False
    self.playto.position = (0,24)
    self.playto.prefix = 'Play to '
    self.mode = self.SttgsSect.new(SettingsBttn, 'MODE', game_manager, 'assets/UI/Warning.png')
    self.mode.static   = False
    self.mode.position = (0,0)
    self.mode.pre_render__()
    self.lives.pre_render__()
    self.timer.pre_render__()
    self.playto.pre_render__()
    #
    self.rmb = self.BindsSect.new(SettingsBttn, 'RMB', None,'assets/UI/Rmb_icon.png')
    self.rmb.suffix = 'Stay'
    self.rmb.catch  = False
    self.rmb.IconFirst = False
    self.rmb.position = (0,0)
    self.rmb.anchor = (1,0)
    self.lmb = self.BindsSect.new(SettingsBttn, 'LMB', None,'assets/UI/Lmb_icon.png')
    self.lmb.suffix = 'Draw'
    self.lmb.catch  = False
    self.lmb.IconFirst = False
    self.lmb.position = (0, 24)
    self.lmb.anchor = (1,0)
    self.rmb.pre_render__()
    self.lmb.pre_render__()
    #
    self.keep_ingame = [self.lmb, self.rmb, self.playto, self.mode]
    #
    self.status_bar = self.UiMain.new(TopPart,'Status_Bar')
    self.plr_hand   = self.UiMain.new(Hand, 'Player_hand', .9)
    self.plr_hand.position = (HALF_X, SCREEN_Y - 120)
    self.plr_hand.enabled = False
    self.ent_hand   = self.UiMain.new(Hand, 'Entity_hand', .8, 1)
    self.ent_hand.hidden_amt = 1
    self.ent_hand.position = (HALF_X, HALF_Y)
    self.ent_hand.ang = -self.ent_hand.ang
    self.ent_hand.enabled = False

  def set_playing(self):
    self.LifeCounter = [self.config.LIVES,self.config.LIVES]
    
    #
    for item in self.keep_ingame:
      tws.new(item, {'alpha':0}, .3)
      tws.new(item.text, {'alpha':200}, .3)
      tws.new(item.icon, {'alpha':200}, .3)
      item.static = True
    #
    self.ent_hand.enabled = True
    self.plr_hand.enabled = True
    tws.new(self.ent_hand, {'position':(HALF_X, HALF_Y)},.2)
    tws.new(self.plr_hand, {'position':(HALF_X, SCREEN_Y - 120)}, .2)
    #
    tws.new(self.lives, {'alpha':0}, .2)
    tws.new(self.lives.text, {'alpha':0}, .2)
    tws.new(self.lives.icon, {'alpha':0}, .2)
    self.lives.static = True
    tws.new(self.timer.text, {'alpha':0}, .2)
    tws.new(self.timer.icon, {'alpha':0}, .2)
    tws.new(self.timer, {'alpha':0}, .2)
    self.timer.static = True
    tws.new(self.SttgsSect, {'position':(50, SCREEN_Y - 104)}, 0.6)
    #
    self.status_bar.new_game(self.config.LIVES, self.config.MODE_NAME)
    
  #
  def set_not_playing(self):
    for i in self.ent_hand.children:
      tws.new(i, {'alpha': 0}, .3)
    tws.new(self.ent_hand, 
      {'position':(HALF_X, HALF_Y - 20)}, 
      0.3, tween.linear, self.ent_hand.reset
    )
    #
    for i in self.plr_hand.children:
      tws.new(i, {'alpha': 0}, .3)
    tws.new(
      self.plr_hand, 
      {'position':(HALF_X, SCREEN_Y - 60)}, 
      0.3, tween.linear, self.plr_hand.reset
    )
    #
    self.playbttn.input_left()
    #
    for item in self.keep_ingame:
      tws.new(item, {'alpha':0}, .3)
      tws.new(item.text, {'alpha':255}, .3)
      tws.new(item.icon, {'alpha':255}, .3)
      item.static = not item.catch
    #
    tws.new(self.lives, {'alpha':0}, .2)
    tws.new(self.lives.text, {'alpha':255}, .2)
    tws.new(self.lives.icon, {'alpha':255}, .2)
    self.lives.static = False
    tws.new(self.timer.text, {'alpha':255}, .2)
    tws.new(self.timer.icon, {'alpha':255}, .2)
    tws.new(self.timer, {'alpha':0}, .2)
    self.timer.static = False
    #
    tws.new(self.SttgsSect, {'position':(50, SCREEN_Y - 144)}, 0.6)
    #
    self.status_bar.end_game()
  #
  def event_detect(self):
    #
    if self.PlayCaught and self.manager.running:
      if self.LifeCounter[0] > self.manager.plr_lives:
        self.LifeCounter[0]  = self.manager.plr_lives
        self.status_bar.heart_break(plr = True)
      if self.LifeCounter[1] > self.manager.entity_lives:
        self.LifeCounter[1]  = self.manager.entity_lives
        self.status_bar.heart_break(plr = False)
    #
    if self.manager.delay <= 0:
      self.DelayCaught = False
      
      if self.manager.plr_turn and not self.PlrTurn:
        self.status_bar.player_side.activate()
        self.status_bar.entity_side.deactivate()
        self.PlrTurn = True
      elif not self.manager.plr_turn and self.PlrTurn:
        self.plr_hand.deck_upd(self.manager.player.deck)
        self.ent_hand.deck_upd(self.manager.entity.deck)
        self.status_bar.player_side.deactivate()
        self.status_bar.entity_side.activate()
        self.PlrTurn = False
    elif self.manager.delay > 0 and not self.DelayCaught:
      self.PlrTurn = not self.manager.plr_turn
      self.plr_hand.reset()
      self.ent_hand.reset()
      self.status_bar.player_side.deactivate()
      self.status_bar.entity_side.deactivate()
      self.DelayCaught = True
    if self.manager.entity_drew and not self.Drew_check:
      self.plr_hand.deck_upd(self.manager.player.deck)
      self.ent_hand.deck_upd(self.manager.entity.deck)
      self.Drew_check = True
    elif not self.manager.entity_drew and self.Drew_check:
      self.plr_hand.deck_upd(self.manager.player.deck)
      self.ent_hand.deck_upd(self.manager.entity.deck)
      self.Drew_check = False

  #
  def update(self, tick = 0, localTime = 0, scroll = (0,0), tick_cycle = 0):
    tws.update(tick)
    tween_update(tick)
    self.status_bar.textile_update(self.manager.time)
    #
    if self.manager.running and not self.PlayCaught:
      self.PlayCaught = True
      self.set_playing()
    elif not self.manager.running and self.PlayCaught:
      self.PlayCaught = False
      self.set_not_playing()
    #
    if self.manager.running:
      self.event_detect()
    #
    self.UiMain.update(tick, localTime, scroll, tick_cycle)
    self.UiOverlay.update(tick, localTime, (0,0), tick_cycle)
    
  
  def render(self, surface):
    self.UiMain.render(surface)
    self.UiOverlay.render(surface)
  
  def input(self, *args):
    input_1 = self.UiMain.input(*args)
    input_2 = self.UiOverlay.input(*args)
    self.BindYeild = input_1 or input_2


  

