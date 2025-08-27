import pygame as py

class UIObj():
  def __init__(self, name = 'UIOBJECT', parent = None):
    self.children   = {}
    self.name       = name
    self.visible    = True
    self.position   = (0,0)
    self.render_pos = (0,0)
    self.size       = (10,10)
    self.hitbox     = False
    self.surface    = None
    self.parent     = parent
    self.boundboxes = {}

  #-------------
  def __call__(self, child = ''):
    if child in self.children:
      return self.children[child]
    
  #-------------
  def update(self, tick = 0, localTime = 0, render_pos = (0,0), *other):
    self.render_pos = (
      render_pos[0] + self.position[0],
      render_pos[1] + self.position[1]
    )

    self.loop('update', tick, localTime, self.render_pos, *other)

  #-------------
  def render(self, surface):
    if surface:
      self.loop('render', surface)
  
  #-------------
  def input(self, pos = (0,0), clicked = False, *other):
    hit = False
    for item in self.boundboxes.values():
      if hasattr(item, 'visible') and getattr(item, 'visible'):
        if (item.render_pos[1] <= pos[1] <= item.render_pos[1] + item.size[1]) and (item.render_pos[0] <= pos[0] <= item.render_pos[0] + item.size[0]):
          item.input(pos, clicked, *other)
          hit = True
    return hit

  #--------------
  def loop(self, call:str, *values:any):
    if not call: return
    for item in self.children.values():
      if hasattr(item, call) and hasattr(item, 'visible'):
        att = getattr(item, call)
        if callable(att) and getattr(item, 'visible'):
          att(*values)
  
  #-------------
  def add(self, obj:type = None, name:str = None, *other) -> 'UIObj':
    if not name:
      name = f'Frame-{len(self.children) + 1}'
    if (type(obj) == type):
      obj = obj(name, self, *other)
    else:
      obj = Frame(name, self, *other)
    self.children[name] = obj
    return obj
  
  #-------------
  def ancestor(self):
    if self.parent == None:
      return self
    return UIObj.ancestor(self.parent)


# ---------------------------------
class Frame(UIObj):
  def __init__(self, name = None, parent = None):
    super().__init__(name, parent)
    self.color    = (255,255,255)
    self.surface  = py.Rect(*self.position, self.position[0] + self.size[0], self.position[1] + self.size[1])
  
  #-------------
  def render(self, surface):
    py.draw.rect(surface, self.color, self.surface)
    super().render(surface)
  
  #-------------
  def update(self, tick = 0 , localTime = 0, render_pos = (0,0), *other):
    super().update(tick, localTime, render_pos, *other)
    self.surface.update(*self.render_pos,*self.size)
    

# ---------------------------------
class Button(Frame):
  def __init__(self, name='UIOBJECT', parent=None):
    super().__init__(name, parent)
    #
    self.hovering = 0
    self.hitbox   = True

    unc = self.ancestor()

    self.id = len(unc.boundboxes) + 1
    unc.boundboxes[self.id]  = self

  def input(self, pos, clicked, cycle = 0, localTime = 0):
    if self.hovering + 1 < cycle:
      self.hover()
    self.hovering = cycle
    if clicked:
      self.clicked()
  
  def clicked(self):
    self.color = (255,0,0)

  def hover(self):
    self.color = (0,0,255)
  
  def unhover(self):
    self.color = (0,255,0)

  def update(self, tick=0, localTime=0, render_pos=(0, 0), cycle = 0 ,*other):
    if 0 < self.hovering <= cycle - 1:
      self.unhover()
      self.hovering = 0
    super().update(tick, localTime, render_pos, cycle, *other) 
    
    
# ---------------------------------
class TextLabel(UIObj):
  def __init__(self, name=None, parent=None, txt_size = 16 ,FileArg = None):
    if not py.font.get_init():
      return
    super().__init__(name, parent)

    self.centerX = False
    self.centerY = False

    self.FileArg    = FileArg
    self.txt_size   = txt_size
    self.color      = (255,255,255)
    self.font       = py.font.Font(self.FileArg, self.txt_size)
    self.text       = ''
    self.antialias  = 1
    self.background = None

    self.final = None
    self()

  def __call__(self, *args):
    if args:
      return super().__call__(args)
    self.final = self.font.render(self.text, self.antialias, self.color, self.background)
    self.size  = self.font.size(self.text)

  def render(self, surface:py.surface):
    surface.blit(self.final, self.render_pos)
    super().render(surface)
  
  def update(self, tick=0, localTime=0, render_pos=(0, 0),*other):
    self.loop('update', tick, localTime, self.render_pos, *other) 

    self.render_pos = (
      render_pos[0] + self.position[0] - (self.size[0] if self.centerX else 0) / 2,
      render_pos[1] + self.position[1] - (self.size[1] if self.centerY else 0) / 2
    )


# ---------------------------------
class ImageLabel(UIObj):
  def __init__(self, name=None, parent=None, file_Arg = ''):
    super().__init__(name, parent)
    self.surface = py.image.load(file_Arg)

  def render(self, surface:py.surface):
    surface.blit(self.surface, self.render_pos)
    super().render(surface)
