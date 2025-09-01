import pygame
from services import interpolation, tween, game_manager
from configs import game_ui, bots
from configs.constants import *

class App:
  def __init__(self):
    self.initialize()  
    self.Running   = False
    self.screen    = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(APP_NAME)

    # time
    self.clock      = pygame.time.Clock()
    self.LocalTime  = 0
    self.deltaTime  = 0
    self.tick_cycle = 0

    # globals
    self.scroll    = (0,0)
    self.mouse_pos = (0,0)

    #pack managers
    self.manager = game_manager.Manager()
    self.Gui     = game_ui.GuiManager()
    self.tween   = tween.TweenSys()


  def initialize(self):
    pygame.init()
    pygame.font.init()

  def run(self):
    self.Running = True
    while self.Running:
      if self.binds():
        self.exit()
        break
      self.update()
      self.render()
      pygame.display.flip()
      self.deltaTime  =  self.clock.tick(FRAME_RATE) / 1000
      self.LocalTime  += self.deltaTime
      self.tick_cycle += 1

  # Main Functions #

  def binds(self):
    clicked, events = False, pygame.event.get()
    #
    for event in events:
      if event.type == pygame.QUIT:
        return True
      if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        clicked = True
    #
    self.mouse_pos = pygame.mouse.get_pos()
    self.Gui.input(self.mouse_pos, clicked, self.tick_cycle)
    if (not self.Gui.BindYeild):
      self.manager.binds(events, self.LocalTime, self.mouse_pos, clicked)

  # run 2 #
  def update(self):
    self.manager.update(self.deltaTime, self.LocalTime)
    #
    self.scroll = interpolation.cam_shake(
      *self.mouse_pos, 
      *self.scroll,
      self.deltaTime
    )
    # -
    self.tween.update(self.deltaTime)
    # -
    self.Gui.update( 
      self.deltaTime, 
      self.LocalTime, 
      (-self.scroll[0], -self.scroll[1]),
      self.tick_cycle
    )

  # run 3 #
  def render(self):
    self.screen.fill((0,0,0))
    self.Gui.render(self.screen)
    pygame.draw.circle(self.screen, (255,0,0), (HALF_X, HALF_Y), 2)
  
  # quit func #
  def exit(self):
    pygame.quit()
#


if __name__ == '__main__':
  Blackjack = App()
  Blackjack . run()