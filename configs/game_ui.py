import services.interface as Ui
import pygame as py
from configs.constants import *

class GuiManager():
  UiManager = Ui.UIObj('UIManager')
  UiMain    = UiManager.new(Ui.UIObj,'UIMain')    # camera shake
  UiOverlay = UiManager.new(Ui.UIObj,'UIOverlay') # no camera shake
  BindYeild = False

  def update(self, tick = 0, localTime = 0, scroll = (0,0), tick_cycle = 0):
    self.UiMain.update(tick, localTime, scroll, tick_cycle)
    self.UiOverlay.update(tick, localTime, (0,0), tick_cycle)
  
  def render(self, surface):
    self.UiMain.render(surface)
    self.UiOverlay.render(surface)
  
  def input(self, mouse_pos = (0,0),*args):
    self.BindYeild = self.UiManager.input(mouse_pos, *args)

  # -----------[   GAME INTERFACE   ]------------ #

  ply_bttn = UiMain.new(None, 'PlayButton')
  ply_bttn.size  = (160, 40)
  ply_bttn.color = (255, 255, 255)
  ply_bttn.visible  = True
  ply_bttn.position = (HALF_X - 80, SCREEN_Y - 170)
  ply_bttn.catch = True
  # ply_bttn.anchor   = (0.5,0.5)
  ply_bttn()
  # -----------[   GAME INTERFACE   ]------------ #