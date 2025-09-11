from services import interface as Ui, tween, game_manager as manager
from configs.constants import *

tws = tween.TweenSys()

class PlayBttn(Ui.UIObj):
  def __init__(self, name='Button0', parent=None, gm_manager=None):
    super().__init__(name, parent)
    self.manager = gm_manager
    self.visible  = False
    self.color = (255,255,255)
    self.size = (160,40)
    self.position = (HALF_X, SCREEN_Y - 120)
    self.catch  = True
    self.anchor = (.5,.5)

    self.bg_img = self.new(Ui.Image, 'Background',f'assets/UI/Button.png')
    self.bg_img.anchor = (.5,.5)
    self.bg_img()

    self.stroke = self.new(Ui.Image, 'Stroke', f'assets/UI/Outline.png')
    self.stroke.anchor = (.5,.5)
    self.stroke.scale = 1.1
    self.stroke.alpha = 0
    self.stroke()

    self.txt = self.new(Ui.Text, 'Text', 28)
    self.txt.color = (0,0,0)
    self.txt.text  = 'Play'
    self.txt.anchor = (.5,.5)
    self.txt()

    center = (self.size[0]/2, self.size[1]/2)
    self.txt.position = center
    self.bg_img.position = center
    self.stroke.position = center

    self()

  def input_first(self, *_):
    tws.new(self.bg_img, {'scale': 1,'alpha':255}, 0.15)
    tws.new(self.stroke, {'scale': 1, 'alpha': 255}, 0.1)
    
  def input_left(self, *_):
    tws.new(self.bg_img, {'scale': 0.95,'alpha': 180}, 0.15)
    tws.new(self.stroke, {'scale': 1.1,'alpha': 0}, 0.1)
    

  def input_caught(self, pos, clicked, cycle, dt):
    if clicked and self.manager and not self.manager.running:
      self.manager.new()
    


# ----------------

class SettingsBttn(Ui.UIObj):
  def __init__(self, name='SettingBttn', parent=None, manager = None, file_arg = None):
    super().__init__(name, parent)
    self.manager = manager
    self.config  = manager.config
    self.color = (153,153,153)
    self.alpha = 0
    self.position = (500,500)
    self.catch = True
    self.pack = [False] * len(DEFAULTS.ARG_POS)
    #
    for num, val in enumerate(DEFAULTS.ARG_POS):
      if val == name:
        self.pack[num] = True
        break
    #
    self.prefix = ''
    self.suffix = ''
    self.spacing = 8
    self.padding = (6,6)
    #
    self.icon = self.new(Ui.Image, 'Icon', file_arg)
    self.icon.anchor = (0,0.5)
    self.icon.color = (255,255,255)
    #
    self.text = self.new(Ui.Text, 'textlabel', 24)
    self.text.anchor = (0,0.5)
    self.text.color = (153,153,153)
    #
    self()

  def pre_render__(self):
    val = getattr(self.config, self.name)
    if callable(val): 
      val = val.__name__[0].upper() + val.__name__[1:]
    self.text.text = self.prefix + str(val) + self.suffix
    self.icon()
    self.text()
    #
    self.size = (
      self.icon.size[0] + self.text.size[0] + self.padding[0] + self.spacing + self.padding[0],
      max(self.icon.size[1], self.text.size[1]) + self.padding[1]
    )
    #
    self.icon.position = (self.padding[0], self.size[1]/2)
    self.text.position = (self.padding[0] + self.icon.size[0] + self.spacing ,self.size[1]/2)
    #
    super().pre_render__()

  def input_first(self, *_):
    tws.new(self, {'alpha':255}, 0.1)
    tws.new(self.text, {'color':(0,0,0)}, 0.1)
    tws.new(self.icon, {'color':(0,0,0)}, 0.1) 
    
  def input_left(self, *_):
    tws.new(self, {'alpha':0}, 0.1) 
    tws.new(self.text, {'color':(153,153,153)}, 0.1) 
    tws.new(self.icon, {'color':(255,255,255)}, 0.1) 

  def input_caught(self, pos, clicked, *_):
    if clicked and self.manager and not self.manager.running:
      self.manager.increment(*self.pack)
      self()
    

# ------
class GuiManager():
  UiMain    = Ui.UIObj('UIMain')    # camera shake
  UiOverlay = Ui.UIObj('UIOverlay') # no camera shake
  UiMain.visible    = False
  UiOverlay.visible = False
  BindYeild = False

  def __init__(self, game_manager):
    self.UiMain.new(PlayBttn, 'PlayBttn', game_manager)
    lives = self.UiMain.new(SettingsBttn, 'LIVES', game_manager, 'assets/UI/Heart.png')
    lives.suffix = ' Lives'
    lives()
    #
    timer = self.UiMain.new(SettingsBttn, 'TIMER', game_manager, 'assets/UI/Clock.png')
    timer.position = (500,550)
    timer.suffix = 's'
    timer()
    #
    playto = self.UiMain.new(SettingsBttn, 'PLAY_TO', game_manager, 'assets/UI/Star.png')
    playto.position = (500,600)
    playto.prefix = 'Play to '
    playto()
    #
    mode = self.UiMain.new(SettingsBttn, 'MODE', game_manager, 'assets/UI/Warning.png')
    mode.position = (500,450)
    mode()

  def update(self, tick = 0, localTime = 0, scroll = (0,0), tick_cycle = 0):
    tws.update(tick)
    self.UiMain.update(tick, localTime, scroll, tick_cycle)
    self.UiOverlay.update(tick, localTime, (0,0), tick_cycle)
  
  def render(self, surface):
    self.UiMain.render(surface)
    self.UiOverlay.render(surface)
  
  def input(self, *args):
    input_1 = self.UiMain.input(*args)
    input_2 = self.UiOverlay.input(*args)
    self.BindYeild = input_1 or input_2


  

