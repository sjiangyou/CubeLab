from Computer import Computer
from Find_User_Dir import find
import pygame
from pygame.locals import *
import time
import os

class App:
    all_text = []
    all_scenes = []
    active_text = None
    active_scene = None
    def __init__(self) -> None:
        App.program_dir = find('CubeLab')
        os.chdir(App.program_dir)
        self.config_file = open('config.txt', 'r')
        self.user_settings = (self.config_file.read().split('\n'))[1::2]
        self.config_file.close()
        pygame.init()
        pygame.display.set_caption('CubeLab')
        App.computer = Computer('', '')
        self.apply_user_settings()
        App.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        App.screen.fill(App.backgroundcolor)
        App.running = True
        App.filein = Textbox(pos = (0, 0), text = 'Session: ', edit = True, fontsize = App.main_fontsize)
        App.eventin = Textbox(pos = (0, App.main_fontsize), text = 'Puzzle: ', edit = True, fontsize = App.main_fontsize)
        App.timein = Textbox(pos = (0, 2 * App.main_fontsize), text = 'Time: ', edit = True, fontsize = App.main_fontsize)
        App.scdisplay = [Textbox(pos = (0, 3 * App.main_fontsize), text = 'Scramble: ', edit = False, fontsize = App.other_fontsize)]
        App.alerts = Textbox(pos = (0, pygame.display.get_surface().get_height() - App.other_fontsize + 20 - App.main_fontsize), text = '', edit = False, fontsize = App.main_fontsize)
        App.avdisplay = [Textbox(pos = (round(13.5 * App.fonts[App.other_fontsize - 20][0] * i), pygame.display.get_surface().get_height() - App.other_fontsize + 20), text = (av + ': '), edit = False, fontsize = App.other_fontsize - 20) for (i, av) in enumerate(self.averages)]
        App.previous_solves = [Textbox(pos = (pygame.display.get_surface().get_width() - 200, int(round(0.6 * i * App.main_fontsize))), text = '', edit = False, fontsize = int(round(0.6 * App.main_fontsize))) for i in range(5)]
        App.exitbutton = Button(pos = (0, pygame.display.get_surface().get_height() - App.other_fontsize + 20 - 2 * App.main_fontsize), text = 'Exit ', fontsize = App.main_fontsize)
        App.stackmat_scene = Scene('Stackmat', App.all_text, App.backgroundcolor)
        App.timer_scene = Scene('Timer', App.all_text, App.backgroundcolor)
        App.active_text = App.stackmat_scene.nodes[0]
        App.active_scene = App.stackmat_scene
    
    def apply_user_settings(self) -> None:
        self.averages = self.user_settings[0].split(', ')
        App.main_fontsize = int(self.user_settings[1])
        App.other_fontsize = int(self.user_settings[2])
        fontsizes = open('fontsizes.txt', 'r')
        fonts = fontsizes.read().split('\n')
        fontsizes.close()
        App.fonts = [eval(size) for size in fonts]
        App.textcolor, App.backgroundcolor = self.extract_color(self.user_settings[3]), self.extract_color(self.user_settings[4])
        os.chdir(find(self.user_settings[5]))
    
    def extract_color(self, rgb) -> tuple:
        rgb = rgb.split(',')
        rgb = [int(value) for value in rgb]
        return tuple(rgb)
    
    def change_active(self, mouse) -> None:
        for text in App.all_text:
            if(pygame.Rect.collidepoint(text.rect, mouse) and (text.edit or type(text) == Button)):
                App.active_text = text
                break
    
    def run(self) -> None:
        while App.running:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT or self.active_text == App.exitbutton): App.running = False
                if(event.type == KEYDOWN):
                    if(event.key == K_BACKSPACE):
                        if(len(self.active_text.text) > self.active_text.init_len): self.active_text.text = self.active_text.text[:-1]
                    elif(event.key == K_TAB):
                        App.active_text = App.all_text[(App.all_text.index(App.active_text) + 1) % 3]
                    elif(event.key == K_RETURN):
                        App.computer = Computer(App.filein.text[(App.filein.init_len):], App.eventin.text[(App.eventin.init_len):])
                        try:
                            App.computer.read_file()
                            new_scramble = App.computer.generate_scramble()
                        except(FileNotFoundError, IndexError):
                            try:newfile = open(str(App.computer.file), 'x')
                            except FileExistsError:new_scramble = App.computer.scramble = 'Invalid Puzzle. '
                            except FileNotFoundError:new_scramble = App.computer.scramble = 'Invalid Session. '
                            else:
                                newfile.write('(Name Here)\nS:\nAO5:\nPB Scramble:')
                                newfile.close()
                                new_scramble = App.computer.scramble = 'Created new file. '
                        if(self.active_text == App.timein):
                            App.computer.run(App.timein.text[6:])
                            self.alerts.text = ''
                            if(App.computer.single):
                                self.alerts.text += 'New PB Single! '
                                App.computer.single = False
                            if(App.computer.average):
                                self.alerts.text += (f'New PB {App.computer.average_type}!')
                                App.computer.average = False
                            new_scramble = App.computer.generate_scramble()
                            App.timein.text = App.timein.text[:6]
                        App.scdisplay[0].text = 'Scramble: ' + new_scramble
                        for text in App.avdisplay:
                            if(text.text[0].upper() == 'A'):
                                text.text = text.text[:text.text.find(' ') + 1] + str(App.computer.do_avg(int(text.text[text.text.find('O') + 1:text.text.find(':')])))
                            if(text.text[0].upper() == 'M'):
                                text.text = text.text[:text.text.find(' ') + 1] + str(App.computer.do_mean(int(text.text[text.text.find('O') + 1:text.text.find(':')])))
                        for idx, text in enumerate(App.previous_solves):
                            try:text.text = str(App.computer.times[idx])
                            except IndexError: text.text = ''
                        indicies = App.scdisplay[0].rollover()
                        count = 0
                        for num, loc in enumerate(indicies[:-1]):
                            if(count + 2 > len(App.scdisplay)):
                                App.scdisplay.append(Textbox(pos = (0, (self.main_fontsize * 3) + (self.other_fontsize * (count + 1))), text = App.scdisplay[0].text[loc:indicies[num + 1]], edit = False, fontsize = App.other_fontsize))
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
            self.screen.fill(App.backgroundcolor)
            for text in App.stackmat_scene.nodes:
                text.draw()
            if(time.time() % 1 > 0.5 and type(App.active_text) != Button):
                pygame.draw.rect(self.screen, App.textcolor, App.active_text.cursor)
            pygame.display.update()
            pygame.display.flip()
            
class Scene:
    def __init__(self, title, nodes, back_color) -> None:
        self.title = title
        self.nodes = nodes
        self.back_color = back_color
        App.all_scenes.append(self)
        
    def set_active(self) -> None:
        App.active_scene = self
        self.render_conv()
    
    def render_conv(self) -> None:
        for node in self.nodes:
            node.render_conv()
            node.draw()

class Textbox:
    def __init__(self, pos, text, edit, fontsize) -> None:
        self.pos = pos
        self.text = text
        self.edit = edit
        self.fontsize = fontsize
        self.fontcolor = App.textcolor
        self.init_len = len(text)
        self.set_font()
        self.render_conv()
        self.draw()
        App.all_text.append(self)
    
    def set_font(self) -> None:
        self.font = pygame.font.Font(os.path.join(App.program_dir, 'Courier_New.ttf'), self.fontsize)
   
    def render_conv(self) -> None:
        try:
            if(self.text[0] == ' '):self.text = self.text[1:]
        except:pass
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos
        self.cursor = Rect(self.rect.topright, (3, self.rect.height))
        self.rect = Rect(self.pos, (pygame.display.get_surface().get_width(), self.fontsize))
    
    def draw(self) -> None:
        App.screen.blit(self.img, self.rect)
    
    def check_mouse(self, mouse) -> bool:
        return(self.rect.collidepoint(mouse))
    
    def rollover(self) -> list:
        return_indicies = [0]
        possible_splits = [i for i, char in enumerate(self.text) if char == ' ']
        max_move_length = max([len(move) for move in App.computer.scramble.split(' ')])
        high = (pygame.display.get_surface().get_width() // (App.fonts[self.fontsize][0])) - 1
        low = high - max_move_length
        while possible_splits:
            try:return_indicies.append(max([num for num in possible_splits if low <= num <= high]))
            except ValueError: return_indicies.append(possible_splits[-1])
            possible_splits = [idx for idx in possible_splits if idx > return_indicies[-1]]
            delta_index = return_indicies[-1] - return_indicies[-2]
            low += delta_index
            high += delta_index
        return return_indicies[1:]

class Button(Textbox):
    def __init__(self, pos, text, fontsize) -> None:
        super().__init__(pos, text, False, fontsize)
        
    def render_conv(self) -> None:
        try:
            if(self.text[0] == ' '):self.text = self.text[1:]
        except:pass
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

def main() -> None:
    App().run()

if(__name__ == '__main__'):
    main()