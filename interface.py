import pygame

class UIObj():
  def __init__(self, name = 'UIOBJECT'):
    self.children = {}
    self.name     = name
    self.visible  = True
  
  def __call__(self, child = ''):
    if child in self.children:
      return self.children[child]
  
  def update(self, tick = 0, localTime = 0):
    self.loop('update', tick, localTime)

  def render(self, surface):
    if surface:
      self.loop('render', surface)
  
  def input(self):
    self.loop('input')

  def loop(self, call:str, *values:any):
    if not call: return
    for item in self.children.values():
      if hasattr(item, call) and hasattr(item, 'visible'):
        att = getattr(item, call)
        if callable(att) and getattr(item, 'visible'):
          att(*values)
        
  
  def add(self, name:str, obj:type = None):
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
    self.position = (0,0)
    self.size     = (10,10)
    self.color    = (255,255,255)
    self.rotation = 0
    # --
    

  def add(self, name, obj):
    return super().add(name, obj)

  def update(self, tick = 0, localTime = 0):
    super().update(tick, localTime)
  
  def render(self, surface):
    super().render(surface)
  
  def input(self):
    super().input()

# ---------------------------------

