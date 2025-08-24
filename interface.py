import pygame as py

class UIObj():
  def __init__(self, name = 'UIOBJECT'):
    self.children   = {}
    self.name       = name
    self.visible    = True
    self.position   = (0,0)
    self.render_pos = (0,0)
    self.size       = (10,10)
    self.surface    = None
    #

  #-------------
  def __call__(self, child = ''):
    if child in self.children:
      return self.children[child]
    
  #-------------
  def update(self, tick = 0, localTime = 0, render_pos = (0,0)):
    self.render_pos = (
      render_pos[0] + self.position[0],
      render_pos[1] + self.position[1]
    )
    if self.surface:
      self.surface.update(*self.render_pos,*self.size)

    self.loop('update', tick, localTime, self.render_pos)

  #-------------
  def render(self, surface):
    if surface:
      self.loop('render', surface)
  
  #-------------
  def input(self):
    self.loop('input')

  #--------------
  def loop(self, call:str, *values:any):
    if not call: return
    for item in self.children.values():
      if hasattr(item, call) and hasattr(item, 'visible'):
        att = getattr(item, call)
        if callable(att) and getattr(item, 'visible'):
          att(*values)     
  
  #-------------
  def add(self, name:str = None, obj:type = None) -> 'UIObj':
    if not name:
      name = f'Frame-{len(self.children) + 1}'
    if (type(obj) == type):
      obj = obj(name)
    else:
      obj = Frame(name)
    self.children[name] = obj
    return obj
  

# ---------------------------------
class Frame(UIObj):
  def __init__(self, name = ''):
    super().__init__(name)
    self.color    = (255,255,255)
    self.surface  = py.Rect(*self.position, self.position[0] + self.size[0], self.position[1] + self.size[1])
  
  #-------------
  def render(self, surface):
    py.draw.rect(surface, self.color, self.surface)
    super().render(surface)
  
  #-------------


