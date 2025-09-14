from services import interface as Ui, tween
from configs.constants import *
from random import randint
from math import floor

tws = tween.TweenSys()

class UserTab(Ui.UIObj):
    def __init__(self, name='UIOBJECT', parent=None, spacing = 5):
      super().__init__(name, parent)
      self.visible = False
      self.title   = name
      self.turn    = False
      self.spacing = spacing
      self.visible_hearts = 3
      self.broken_hearts  = 0
      self.heart_size = (0,0)
      self.heart_space = 0
      self.top_title = self.new(Ui.Text, 'Top_Title', 22)
      self.top_title.text = name 
      self.top_title.color = (153,153,153)
      self.top_title()
      self.lean_left = True

      self.hearts = []

      for iteration in range(max(DEFAULTS.LIVES_SEL)):
        container = self.new(Ui.UIObj, f'Heart_{iteration}_Container')
        container.visible = False
        self.hearts.append(container)
        #
        container.heart = container.new(Ui.Image, f'Heart_{iteration}', 'assets/UI/Heart.png')
        container.heart()
        container.outline = container.new(Ui.Image, f'Heart_{iteration}', 'assets/UI/Heart_Outline.png')
        container.outline.visible = False
        container.outline()
        self.heart_size = container.heart.size
        container.position = (iteration * spacing + self.heart_size[0] * iteration, self.top_title.size[1] + 5)
      
      self()

    def pre_render__(self):
      self.heart_space = self.heart_size[0] * self.visible_hearts + self.spacing * max(self.visible_hearts - 1, 0)
      self.top_title()
      self.size = (
        max(self.heart_space, self.top_title.size[0]),
        self.top_title.size[1] + 5 + self.heart_size[1]
      )
      super().pre_render__()
      
      
    
    def reset(self, hearts = 3, title = None):
      self.title = title or self.title
      self.visible_hearts = hearts
      self.broken_hearts  = 0
      self.top_title.text = self.title
      self.top_title()

      self()

      local_i = 0
      right_offset = (0) if self.lean_left else (self.size[0] - self.heart_space)
      for heart in self.hearts:
        heart.enabled = local_i < hearts
        heart.position = (local_i * self.spacing + self.heart_size[0] * local_i + right_offset, self.top_title.size[1] + 5)
        if not self.lean_left:
          heart.anchor = (0,0)
        local_i += 1
        #
        if heart.enabled:
          heart.heart.alpha = 0
          heart.heart()
          tws.new(heart.heart, {'alpha':255}, MATCH_DELAY_TIME)
        
      self.top_title.alpha = 0
      self.top_title()
      tws.new(self.top_title, {'alpha':255}, MATCH_DELAY_TIME)
      if self.lean_left:
        self.top_title.position = (0,0)
        self.top_title.anchor = (0,0)
      else:
        self.top_title.position = (self.size[0], 0)
        self.top_title.anchor = (1,0)
    
    def activate(self):
      if self.turn: return
      self.turn = True
      self.top_title.color = (153,153,153)
      tws.new(self.top_title, {'color':(153,30,30)}, 0.3)
      for num, heart in enumerate(self.hearts):
        if num < self.broken_hearts:
          heart.outline.color = (255,255,255)
          tws.new(heart.outline, {'color':(255,0,0)}, 0.3)
        else:
          heart.heart.color = (255,255,255)
          tws.new(heart.heart, {'color':(255,0,0)}, 0.3)
        
    def deactivate(self):
      if not self.turn: return
      self.turn = False
      self.top_title.color = (153,30,30)
      tws.new(self.top_title, {'color':(153,153,153)}, 0.3)
      for num, heart in enumerate(self.hearts):
        if num < self.broken_hearts:
          heart.outline.color = (255,0,0)
          tws.new(heart.outline, {'color':(255,255,255)}, 0.3)
        else:
          heart.heart.color = (255,0,0)
          tws.new(heart.heart, {'color':(255,255,255)}, 0.3)
    
    def break_heart(self):
      subject = self.hearts[min(self.hearts.__len__()-1, self.broken_hearts)]
      self.broken_hearts += 1
      subject.outline.alpha = 180
      subject.outline.scale = 1
      subject.outline.visible = True
      subject.outline.color = (255,255,255)
      subject.outline()
      subject.heart()
      tws.new(subject.heart, {'alpha':0, 'scale':2, 'anchor':(.5,.5)}, .3)



class TopPart(Ui.UIObj):
  def __init__(self, name='UIOBJECT', parent=None):
    super().__init__(name, parent)
    self.position = (HALF_X, 50)
    self.visible  = False
    #
    self.sides_spaces = 85
    #
    self.player_side = self.new(UserTab, 'You')
    self.entity_side = self.new(UserTab, 'Entity')
    self.player_side.lean_left = False
    self.entity_side.position  = (self.sides_spaces * 2 + self.player_side.size[0], 0)
    #
    self.timer = self.new(Ui.UIObj, 'Timer')
    self.timer.visible = True
    self.timer.color = (153,153,153)
    self.time  = self.timer.new(Ui.Text, 'TimerText', 22)
    self.time.text = '67:67'
    self.time.color  = (0,0,0)
    self.time()
    self.timer.size = (self.time.size[0] + 12, self.time.size[1] + 12)
    self.time.position = (6, 6)
    self.timer()
    #
    self.timer.anchor  = (.5,.5)
    self.anchor = (.5,.5)
    self()
    self.enabled = False
  
  def new_game(self, hearts = 3, entity_name = 'Entity'):
    self.entity_side.reset(hearts, entity_name)
    self.entity_side.position  = (self.sides_spaces * 2 + self.player_side.size[0], 0)
    self.player_side.reset(hearts)
    #
    self.enabled  = True
    self.position = (HALF_X, 50)
    self.timer.color = (0,0,0)
    #
    self.timer()
    tws.new(self.timer, {'color':(156,156,156)}, MATCH_DELAY_TIME)
    #
    self.pre_render__()

  
  def pre_render__(self):
    self.player_side()
    self.entity_side()
    self.size = (
      self.entity_side.position[0] + self.entity_side.size[0],
      self.player_side.size[1]
    )

    self.player_side.position = (max(0, self.entity_side.size[0] - self.player_side.size[0]),0)

    self.timer.position = (
      self.size[0]/2,
      self.size[1]/2
    )
    
    super().pre_render__()
  
  def textile_update(self, time = 0):
    mins, secs = divmod(time, 60)
    self.time.text = f'{floor(mins)}:{floor(secs)}' + ('0' if secs < 10 else '')
    self.timer.size = (self.time.size[0] + 12, self.time.size[1] + 12)
    self.time()
    self.timer()
  
  def heart_break(self, plr = True):
    if plr: return self.player_side.break_heart()
    return self.entity_side.break_heart()



class PlayBttn(Ui.UIObj):
  def __init__(self, name='Button0', parent=None, gm_manager=None):
    super().__init__(name, parent)
    self.manager = gm_manager
    self.visible  = False
    self.color = (255,255,255)
    self.size = (160,40)
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
    if self.manager.running: return
    tws.new(self.bg_img, {'scale': 1,'alpha':255}, 0.15)
    tws.new(self.stroke, {'scale': 1, 'alpha': 255}, 0.1)
    
  def input_left(self, *_):
    if self.manager.running: return
    tws.new(self.bg_img, {'scale': 0.95,'alpha': 180}, 0.15)
    tws.new(self.stroke, {'scale': 1.1,'alpha': 0}, 0.1)
    

  def input_caught(self, pos, clicked, cycle, dt):
    if clicked and self.manager and not self.manager.running:
      self.manager.new()
      self.manager.delay = MATCH_DELAY_TIME * 2
      tws.new(self.bg_img, {'scale': 1.1,'alpha': 0}, 0.1)
      tws.new(self.stroke, {'scale': 1.1,'alpha': 0}, 0.1)
    


# ----------------

class SettingsBttn(Ui.UIObj):
  def __init__(self, name='SettingBttn', parent=None, manager = None, file_arg = None):
    super().__init__(name, parent)
    self.manager = manager
    self.config  = None if not manager else manager.config
    self.color = (153,153,153)
    self.size  = (0,0)
    self.alpha = 0
    self.position = (50, SCREEN_Y - 50)
    self.catch  = True
    self.pack   = [False] * len(DEFAULTS.ARG_POS)
    self.static = True
    self.IconFirst = True
    #
    for num, val in enumerate(DEFAULTS.ARG_POS):
      if val == name:
        self.pack[num] = True
        break
    #
    self.prefix  = ''
    self.suffix  = ''
    self.spacing = 8
    self.padding = (6,6)
    #
    self.icon = self.new(Ui.Image, 'Icon', file_arg)
    self.icon.anchor = (0,0.5)
    self.icon.color  = (255,255,255)
    #
    self.text = self.new(Ui.Text, 'textlabel', 24)
    self.text.anchor = (0,0.5)
    self.text.color  = (153,153,153)
    #
    self()

  def pre_render__(self):
    val = ''
    if not self.static:
      val = getattr(self.config, self.name)
      if callable(val): 
        val = self.config.MODE_NAME
    self.text.text = self.prefix + str(val) + self.suffix
    self.icon()
    self.text()
    #
    self.size = (
      self.icon.size[0] + self.text.size[0] + self.padding[0] + self.spacing + self.padding[0],
      max(self.icon.size[1], self.text.size[1]) + self.padding[1]
    )
    #
    if self.IconFirst:
      self.icon.position = (self.padding[0], self.size[1]/2)
      self.text.position = (self.padding[0] + self.icon.size[0] + self.spacing ,self.size[1]/2)
    else:
      self.text.position = (self.padding[0], self.size[1]/2)
      self.icon.position = (self.padding[0] + self.text.size[0] + self.spacing ,self.size[1]/2)
    #
    super().pre_render__()

  def input_first(self, *_):
    if self.static: return
    tws.new(self, {'alpha':255}, 0.1)
    tws.new(self.text, {'color':(0,0,0)}, 0.1)
    tws.new(self.icon, {'color':(0,0,0)}, 0.1) 
  
  def input_left(self, *_):
    if self.static: return
    tws.new(self, {'alpha':0}, 0.1) 
    tws.new(self.text, {'color':(153,153,153)}, 0.1) 
    tws.new(self.icon, {'color':(255,255,255)}, 0.1) 

  def input_caught(self, pos, clicked, *_):
    if clicked and self.manager and not self.manager.running and not self.static:
      self.manager.increment(*self.pack)
      self()
      self.text.color = (153,153,153)
      self.icon.color = (255,255,255)
      tws.new(self.text, {'color':(0,0,0)}, 0.3) 
      tws.new(self.icon, {'color':(0,0,0)}, 0.3)
    

# ----------------

class ClickEffect(Ui.Text):
  def Clicked(self, mouse_pos = (0,0), promts = ['hi']):
    self.rotation = 0
    self.alpha = 255
    # + 5 for the cursor offset
    self.position = (mouse_pos[0] + 5, mouse_pos[1])
    self.text = promts[randint(0, promts.__len__() - 1)]
    #
    tws.new(self, {'position':(mouse_pos[0] + 5 + randint(18,28), mouse_pos[1] - 32), 'alpha': 0, 'rotation' : -randint(5,25)}, 0.5)



def tween_update(tick = 0):
  tws.update(tick)