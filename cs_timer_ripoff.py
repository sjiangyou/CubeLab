#from Rubiks_Cube_Avg_Calc import *
import pygame
from pygame.locals import *
import time

key_dict = {K_0:'0', K_1:'1', K_2:'2', K_3:'3', K_4:'4', 
            K_5:'5', K_6:'6', K_7:'7', K_8:'8', K_9:'9'}
#settings = open('config.txt', 'r')

class App:
    all_text = []
    active_text = None
    def __init__(self):
        pygame.init()
        App.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        App.screen.fill(Color('black'))
        self.running = True
        App.filein = Textbox(pos = (0, 0), text = 'File: ')
        App.eventin = Textbox(pos = (0, 50), text = 'Event: ')
        App.timein = Textbox(pos = (0, 100), text = 'Time: ')
        App.scdisplay = Textbox(pos = (0, 150), text = 'Scramble: ')
        #App.avdisplay = [Textbox(pos = (0, 50 * (i + 4)), text = (av + ': ')) for (i, av) in enumerate(settings)]
        App.active_text = App.all_text[0]
    def change_active(self, mouse):
        for text in App.all_text:
            if(pygame.Rect.collidepoint(text.rect, mouse)):
                App.active_text = text
                break
    def run(self):
        while self.running:
            for event in pygame.event.get():
                #print(event)
                if(event.type == pygame.QUIT): self.running = False
                if(event.type == KEYDOWN):
                    if(event.key == K_BACKSPACE):
                        if(len(self.timein.text) > 6):
                            self.timein.text = self.timein.text[:-1]
                    elif(event.key == K_RETURN):
                        pass
                    elif(event.key in key_dict):
                        self.timein.text += event.unicode
                    for text in App.all_text:
                        text.render_conv()
                if(event.type == MOUSEBUTTONDOWN):
                    self.change_active(event.pos)
            self.screen.fill(Color('black'))
            for text in App.all_text:
                text.draw()
            if time.time() % 1 > 0.5:
                pygame.draw.rect(self.screen, Color('white'), App.active_text.cursor)
            pygame.display.update()
             
class Textbox:
    def __init__(self, pos, text):
        self.pos = pos
        self.text = text
        self.fontname = 'couriernew'
        self.fontsize = 50
        self.fontcolor = Color('white')
        self.set_font()
        self.render_conv()
        self.draw()
        App.all_text.append(self)
    def set_font(self):
        self.font = pygame.font.SysFont(self.fontname, self.fontsize)
    def render_conv(self):
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos
        self.cursor = Rect(self.rect.topright, (3, self.rect.height))
    def draw(self):
        App.screen.blit(self.img, self.rect)
    def check_mouse(self, mouse):
        return(self.rect.collidepoint(mouse))

if(__name__ == '__main__'):
    App().run()

#calculator()