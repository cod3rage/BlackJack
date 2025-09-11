import pygame as py


class UIObj():
  def __init__(self, name = 'UIOBJECT', parent = None):
    #
    self.parent   = parent
    self.children = []
    #
    self.name = name
    self.Id   = 0

    # render enchancements
    self.alpha    = 255
    self.scale    = 1
    self.rotation = 0

    # enablilities
    self.visible = True
    self.enabled = True

    # catch user input
    self.caught     = False
    self.last_catch = 0
    self.catch      = False

    # cords
    self.position = (0,0)
    self.anchor   = (0,0) # center cord relitive
    self.size     = (10,10)
    self.color    = (255,255,255)

    # pre-render
    self.render_pos = (0,0)
    self.surface = py.Surface(self.size)

  #-------------
  def pre_update__(self):
    return

  def input_first(self, pos, clicked, *_):
    return # mouse entered 

  def input_left(self, *_):
    return # mouse left

  def input_caught(self, *_):
    return # mouse hovering
  
  def pre_render__(self):
    self.scale    = abs(self.scale)
    self.rotation = abs(self.rotation) % 360
    self.alpha    = min(abs(self.alpha), 255)
    #
    self.surface = py.surface.Surface(self.size)
    self.surface = py.transform.scale_by(self.surface, self.scale)
    self.surface = py.transform.rotate(self.surface, self.rotation)
    self.surface.set_alpha(self.alpha)
    self.surface.fill(self.color)
  
  def __render__(self, surface:py.surface.Surface):
    surface.blit(self.surface, self.render_pos)

  #-------------
  def __call__(self, name = None, Id = None):
    if not name and not Id:
      self.pre_render__()
    else: 
      for child in self.children:
        if Id and getattr(child, 'Id') == Id:
          return child
        elif name and getattr(child, 'name') == name:
          return child


  #-------------
  def update(self, tick = 0, localTime = 0, render_pos = (0,0), *other):
    self.pre_update__()
    self.render_pos = (
      render_pos[0] + self.position[0] - self.size[0] * self.anchor[0],
      render_pos[1] + self.position[1] - self.size[1] * self.anchor[1]
    )
    self.loop('update', tick, localTime, self.render_pos, *other)


  #-------------
  def render(self, surface):
    if not surface: return
    if self.visible:
      self.__render__(surface)
    self.loop('render', surface)
  

  #-------------
  def input(self, pos = (0,0), clicked = None, cycle = 0, *other):
    if cycle < 10: return 
    if self.loop('input', pos, clicked, cycle, *other): return True
    #
    if (self.catch):
      if ( self.render_pos[0] <= pos[0] < self.render_pos[0] + self.size[0] and 
        self.render_pos[1] <= pos[1] < self.render_pos[1] + self.size[1]
      ):
        if not self.caught:
          self.caught = True
          self.input_first(pos, clicked, cycle, *other)
        self.input_caught(pos, clicked, cycle, *other)
        return True
      elif self.caught:
        self.caught = False
        self.input_left(pos, clicked, cycle, *other)

      


  #--------------
  def loop(self, call:str, *values:any):
    if not call or not self.enabled: return
    return_statement = False
    for item in self.children:
      if hasattr(item, call):
        att = getattr(item, call)
        if callable(att):
          return_statement = att(*values)
    return return_statement


  #-------------
  def new(self, obj:type = None, name:str = None, *other) -> 'UIObj':
    if (type(obj) == type):
      obj = obj(name, self, *other)
    else:
      obj = UIObj(name, self, *other)
    setattr(obj, 'Id', self.children.__len__())
    self.children.append(obj)
    return obj


  #-------------
  def ancestor(self):
    if self.parent == None:
      return self
    return UIObj.ancestor(self.parent)




### < ---------  [   Other Interface Objects   ]  ------------ > ###


class Image(UIObj):
  def __init__(self, name=None, parent=None, file_Arg = ''):
    super().__init__()
    self.file_arg = file_Arg
    self.img = py.image.load(file_Arg)
    self.surface = self.img
    self.color = None
    self()
  
  def pre_render__(self):
    self.scale    = abs(self.scale)
    self.rotation = abs(self.rotation) % 360
    self.alpha    = min(abs(self.alpha), 255)
    #
    self.surface = py.transform.scale_by(self.img, self.scale)
    self.surface = py.transform.rotate(self.surface, self.rotation)
    self.surface.set_alpha(self.alpha)
    self.size = self.surface.get_size()
    if self.color:
      self.surface.fill(self.color, special_flags=py.BLEND_MULT)
  

#

class Text(UIObj):
  def __init__(self, name=None, parent=None, txt_size = 16 ,FileArg = None):
    if not py.font.get_init():
      py.font.init()
    self.FileArg    = FileArg
    self.txt_size   = txt_size
    self.font       = py.font.Font(self.FileArg, self.txt_size)
    self.text       = ''
    self.antialias  = 1
    self.background = None
    super().__init__(name, parent)



  def pre_render__(self):
    self.scale    = abs(self.scale)
    self.rotation = abs(self.rotation) % 360
    self.alpha    = min(abs(self.alpha), 255)
    #
    self.surface  = self.font.render(self.text, self.antialias,self.color, self.background)
    #
    self.surface = py.transform.scale_by(self.surface, self.scale)
    self.surface = py.transform.rotate(self.surface, self.rotation)
    self.surface.set_alpha(self.alpha)
    self.size = self.font.size(self.text)
  





    



