from Rubiks_Cube_Avg_Calc import Computer
import pygame
from pygame.locals import *
import time
import os
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Courier_New.ttf'), 'r')
class App:
    all_text = []
    active_text = None
    def __init__(self):
        pygame.init()
        App.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        App.screen.fill(Color('black'))
        self.running = True
        App.filein = Textbox(pos = (0, 0), text = 'File: ', edit = True, fontsize = 50)
        App.eventin = Textbox(pos = (0, 50), text = 'Puzzle: ', edit = True, fontsize = 50)
        App.timein = Textbox(pos = (0, 100), text = 'Time: ', edit = True, fontsize = 50)
        App.scdisplay = [Textbox(pos = (0, 150), text = 'Scramble: ', edit = False, fontsize = 35)]
        App.alerts = Textbox(pos = (0, pygame.display.get_surface().get_height() - 100), text = '', edit = False, fontsize = 50)
        App.computer = Computer('', '')
        App.avdisplay = [Textbox(pos = (200 * i, pygame.display.get_surface().get_height() - 50), text = (av + ': '), edit = False, fontsize = 25) for (i, av) in \
                         enumerate(['AO05', 'AO12', 'AO20'])]
        App.active_text = App.all_text[0]
    
    def change_active(self, mouse):
        for text in App.all_text:
            if(pygame.Rect.collidepoint(text.rect, mouse) and (text.edit)):
                App.active_text = text
                break
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT): self.running = False
                if(event.type == KEYDOWN):
                    if(event.key == K_BACKSPACE and len(self.active_text.text) > self.active_text.init_len):
                        self.active_text.text = self.active_text.text[:-1]
                    elif(event.key == K_RETURN):
                        print(App.computer.single)
                        if(self.active_text == App.timein):
                            App.computer.run(App.timein.text[6:])
                            self.alerts.text = ''
                            if(App.computer.single):
                                self.alerts.text += 'New PB Single! '
                                App.computer.PB_scramble = new_scramble
                            if(App.computer.ao5):
                                self.alerts.text += 'New PB AO5!'
                            print(App.computer.times)
                            for text in App.avdisplay:
                                text.text = text.text[:text.text.find(' ') + 1] + str(App.computer.mid_avg(int(text.text[text.text.find(':') - 2:text.text.find(':')])))
                                print(text.text)
                            App.computer.write_file()
                            print(self.alerts.text)
                            new_scramble = App.computer.generate_scramble()
                            App.timein.text = App.timein.text[:6]
                        else:
                            App.computer = Computer(App.filein.text[6:], App.eventin.text[8:])
                            try:
                                App.computer.read_file()
                                new_scramble = App.computer.generate_scramble()
                            except:
                                new_scramble = 'Failed to read file'
                        App.scdisplay[0].text = 'Scramble: ' + new_scramble
                        indicies = App.scdisplay[0].rollover()
                        count = 0
                        for num, loc in enumerate(indicies[:-1]):
                            if(count + 2 > len(App.scdisplay)):
                                App.scdisplay.append(Textbox(pos = (0, 185 + (35 * count)), text = App.scdisplay[0].text[loc:indicies[num + 1]], edit = False, fontsize = 35))
                            else:
                                App.scdisplay[count + 1].text = App.scdisplay[0].text[loc:indicies[num + 1]]
                            count += 1
                        for idx in range(len(App.scdisplay)):
                            if idx > count:
                                App.scdisplay[idx].text = ''
                        App.scdisplay[0].text = App.scdisplay[0].text[0:indicies[0]]
                    else:
                        self.active_text.text += event.unicode
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
            pygame.display.flip()
        f.close()
             
class Textbox:
    def __init__(self, pos, text, edit, fontsize):
        self.pos = pos
        self.text = text
        self.edit = edit
        self.fontsize = fontsize
        self.fontcolor = Color('white')
        self.init_len = len(text)
        self.set_font()
        self.render_conv()
        self.draw()
        App.all_text.append(self)
    
    def set_font(self):
        self.font = pygame.font.Font(f, self.fontsize)
   
    def render_conv(self):
        try:
            if(self.text[0] == ' '):self.text = self.text[1:]
        except:pass
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos
        self.cursor = Rect(self.rect.topright, (3, self.rect.height))
        self.rect = Rect(self.pos, (pygame.display.Info().current_w, 50))
    
    def draw(self):
        App.screen.blit(self.img, self.rect)
    
    def check_mouse(self, mouse):
        return(self.rect.collidepoint(mouse))
    
    def rollover(self):
        return_indicies = [0]
        possible_splits = [i for i, char in enumerate(self.text) if char == ' ']
        low, high = 46, 49
        print(possible_splits)
        while possible_splits:
            try:return_indicies.append(max(search_num_list(possible_splits, low, high)))
            except ValueError: return_indicies.append(possible_splits[-1])
            possible_splits = [idx for idx in possible_splits if idx > return_indicies[-1]]
            delta_index = return_indicies[-1] - return_indicies[-2]
            low += delta_index
            high += delta_index
        print(return_indicies)
        #return_indicies.append(len(self.text) - 1)
        return return_indicies[1:]

def search_num_list(lst, lower_bound, upper_bound):
    return([num for num in lst if lower_bound <= num <= upper_bound])

if(__name__ == '__main__'):
    App().run()