import pygame
import deck, interface as gui

SCREEN_SIZE = (800,600)
FRAME_RATE  = 60
APP_NAME    = 'BlackJack'

class App:
  def __init__(self):
    self.initialize()
    self.Running   = True
    self.screen    = pygame.display.set_mode(SCREEN_SIZE)
    self.clock     = pygame.time.Clock()
    self.LocalTime = 0
    self.deltaTime = 0
    #
    self.text0 = pygame.font.Font(None, 12)
    self.text1 = pygame.font.Font(None, 16)
    self.text2 = pygame.font.Font(None, 22)
    #
    pygame.display.set_caption(APP_NAME)
    #
    self.deck = deck.Deck()

  def initialize(self):
    pygame.init()
    pygame.font.init()

  def run(self):
    while self.Running:
      if self.keybinds():
        self.exit()
        break
      self.update()
      self.render()
      pygame.display.update()
      self.deltaTime =  self.clock.tick(FRAME_RATE) / 1000
      self.LocalTime += self.deltaTime

  # Main Functions #

  def keybinds(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return True

  # run 2 #
  def update(self):
    pass

  # run 3 #
  def render(self):
    self.screen.fill((5,5,5))
    
    self.screen.blit(self.text0.render('Text0', 0, (255,255,255)), (400, 200))
    self.screen.blit(self.text1.render('Text1', 0, (255,255,255)), (400, 300))
    self.screen.blit(self.text2.render('Text2', 0, (255,255,255)), (400, 400))
  
  # quit func #
  def exit(self):
    pygame.quit()
#


if __name__ == '__main__':
  Blackjack = App()
  Blackjack . run()