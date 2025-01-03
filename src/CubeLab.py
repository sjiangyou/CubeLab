import time
import os
import pygame
from pygame.locals import *
from Computer import Computer
from Find_User_Dir import find
from Parse_Scene_XML import parse


class App:
    all_scenes = []
    file = ""
    puzzle = ""
    program_dir = find("CubeLab")
    computer = Computer("", "")
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    running = False
    width, height = pygame.display.get_surface().get_size()
    backgroundcolor = (0, 0, 0)
    textcolor = (255, 255, 255)
    main_fontsize = 0
    second_fontsize = 0
    third_fontsize = 0
    fonts: list[tuple] = []
    averages: list[str] = []
    timing_method = ""

    def __init__(self) -> None:
        os.chdir(App.program_dir)
        pygame.init()
        pygame.display.set_caption("CubeLab")
        with open("config.txt", "r", encoding="utf-8") as file:
            self.user_settings = (file.read().split("\n"))[1::2]
        self.apply_user_settings()
        App.screen.fill(App.backgroundcolor)
        App.running = True
        self.active_scene = Scene(f"{App.timing_method}_Scene.xml")
        self.active_text = self.active_scene.active_text = eval(
            f"self.active_scene.{self.active_scene.input_nodes[0]}"
        )

    def apply_user_settings(self) -> None:
        App.averages = self.user_settings[0].split(", ")
        App.main_fontsize = int(self.user_settings[1])
        App.second_fontsize = int(self.user_settings[2])
        App.third_fontsize = App.second_fontsize - 20
        with open("fontsizes.txt", "r", encoding="utf-8") as fontsizes:
            fonts = fontsizes.read().split("\n")
        App.fonts = [eval(size) for size in fonts]
        App.textcolor, App.backgroundcolor = self.extract_color(
            self.user_settings[3]
        ), self.extract_color(self.user_settings[4])
        App.timing_method = self.user_settings[5]
        os.chdir(find(self.user_settings[6]))

    def extract_color(self, rgb) -> tuple:
        rgb = rgb.split(",")
        rgb = [int(value) for value in rgb]
        return tuple(rgb)

    def change_active_text_mouse(self, mouse) -> None:
        for text in self.active_scene.nodes:
            if pygame.Rect.collidepoint(text.rect, mouse) and (
                text.edit or isinstance(text, Button)
            ):
                self.active_scene.active_text = text
                break
        self.active_text = self.active_scene.active_text

    def change_active_text_keyboard(self) -> None:
        self.active_scene.active_index = (self.active_scene.active_index + 1) % len(
            self.active_scene.input_nodes
        )
        self.active_text = self.active_scene.active_text = eval(
            f"self.active_scene.{self.active_scene.input_nodes[self.active_scene.active_index]}"
        )

    def run(self) -> None:
        while App.running:
            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or self.active_text == self.active_scene.exitbutton
                ):
                    App.running = False
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        if (
                            len(self.active_scene.active_text.text)
                            > self.active_scene.active_text.init_len
                        ):
                            self.active_scene.active_text.text = (
                                self.active_scene.active_text.text[:-1]
                            )
                    elif event.key == K_TAB:
                        self.change_active_text_keyboard()
                    elif event.key == K_RETURN:
                        App.file = self.active_scene.filein.text[
                            self.active_scene.filein.init_len :
                        ]
                        App.puzzle = self.active_scene.eventin.text[
                            self.active_scene.eventin.init_len :
                        ]
                        App.computer = Computer(App.file, App.puzzle)
                        try:
                            App.computer.read_file()
                            new_scramble = App.computer.generate_scramble()
                        except (FileNotFoundError, IndexError):
                            try:
                                newfile = open(
                                    str(App.computer.file), "x", encoding="utf-8"
                                )
                            except FileExistsError:
                                new_scramble = App.computer.scramble = (
                                    "Invalid Puzzle. "
                                )
                            except FileNotFoundError:
                                new_scramble = App.computer.scramble = (
                                    "Invalid Session. "
                                )
                            else:
                                with newfile:
                                    newfile.write("(Name Here)\nS:\nAO5:\nPB Scramble:")
                                new_scramble = App.computer.scramble = (
                                    "Created new file. "
                                )
                        if self.active_scene.active_text == self.active_scene.timein:
                            App.computer.run(
                                self.active_scene.timein.text[
                                    self.active_scene.timein.init_len :
                                ]
                            )
                            self.active_scene.alerts.text = ""
                            if App.computer.single:
                                self.active_scene.alerts.text += "New PB Single! "
                                App.computer.single = False
                            if App.computer.average:
                                self.active_scene.alerts.text += (
                                    f"New PB {App.computer.average_type}!"
                                )
                                App.computer.average = False
                            new_scramble = App.computer.generate_scramble()
                            self.active_scene.timein.text = (
                                self.active_scene.timein.text[:6]
                            )
                        self.active_scene.scdisplay[0].text = (
                            "Scramble: " + new_scramble
                        )
                        for text in self.active_scene.avdisplay:
                            if text.text[0].upper() == "A":
                                text.text = text.text[: text.text.find(" ") + 1] + str(
                                    App.computer.do_avg(
                                        int(
                                            text.text[
                                                text.text.find("O")
                                                + 1 : text.text.find(":")
                                            ]
                                        )
                                    )
                                )
                            if text.text[0].upper() == "M":
                                text.text = text.text[: text.text.find(" ") + 1] + str(
                                    App.computer.do_mean(
                                        int(
                                            text.text[
                                                text.text.find("O")
                                                + 1 : text.text.find(":")
                                            ]
                                        )
                                    )
                                )
                        for idx, text in enumerate(self.active_scene.previoussolves):
                            try:
                                text.text = str(App.computer.times[idx])
                            except IndexError:
                                text.text = ""
                        indicies = self.active_scene.scdisplay[0].rollover()
                        count = 0
                        for num, loc in enumerate(indicies[:-1]):
                            if count + 2 > len(self.active_scene.scdisplay):
                                self.active_scene.scdisplay.append(
                                    Textbox(
                                        pos=(
                                            0,
                                            (App.main_fontsize * 3)
                                            + (App.second_fontsize * (count + 1)),
                                        ),
                                        text=self.active_scene.scdisplay[0].text[
                                            loc : indicies[num + 1]
                                        ],
                                        edit=False,
                                        fontsize=App.second_fontsize,
                                    )
                                )
                            else:
                                self.active_scene.scdisplay[count + 1].text = (
                                    self.active_scene.scdisplay[0].text[
                                        loc : indicies[num + 1]
                                    ]
                                )
                            count += 1
                            self.active_scene.nodes.append(
                                self.active_scene.scdisplay[-1]
                            )
                        for idx, elem in enumerate(self.active_scene.scdisplay):
                            if idx > count:
                                elem.text = ""
                        self.active_scene.scdisplay[0].text = (
                            self.active_scene.scdisplay[0].text[0 : indicies[0]]
                        )
                    else:
                        self.active_scene.update_active_text(event.unicode)
                    for text in self.active_scene.nodes:
                        text.render()
                if event.type == MOUSEBUTTONDOWN:
                    self.change_active_text_mouse(event.pos)
            self.screen.fill(App.backgroundcolor)
            for text in self.active_scene.nodes:
                text.draw()
            if time.time() % 1 > 0.5 and not isinstance(self.active_text, Button):
                pygame.draw.rect(
                    self.screen, App.textcolor, self.active_scene.active_text.cursor
                )
            pygame.display.update()
            pygame.display.flip()


class Scene:
    def __init__(self, file) -> None:
        self.file = file
        self.nodes: list = []
        self.names = self.populate_scene(file)[1]
        self.input_nodes: list[Textbox] = [
            self.names[i] for i, node in enumerate(self.nodes) if node.edit
        ]
        self.active_index = 0
        self.active_text = self.nodes[0]
        App.all_scenes.append(self)

    def populate_scene(self, file) -> tuple[list, list]:
        data = parse(file)
        elements: list = []
        names: list[str] = []
        for i, elem in enumerate(data[0]):
            if isinstance(elem[0], list):
                temp = []
                if elem[1]["iterator"] == "":
                    for e in elem[0]:
                        temp.append(eval(e))
                else:
                    for iterator in eval(elem[1]["iterator"]):
                        temp.append(eval(elem[0][0]))
                elements.insert(data[1][i], temp)
            else:
                elements.insert(data[1][i], eval(elem[0]))
            names.insert(data[1][i], elem[1]["name"])
        for elem in elements:
            if isinstance(elem, list):
                self.nodes.extend(elem)
            else:
                self.nodes.append(elem)
        self.title, self.back_color, self.scene_type = data[2], data[3], data[4]
        self.input_texts = [text for text in self.nodes if text.edit]
        self.active_text = self.input_texts[0]
        for i, elem in enumerate(elements):
            setattr(self, names[i], elem)
        return elements, names

    def update_active_text(self, char) -> None:
        self.active_text.text += char if char.isprintable() else ""

    def render(self) -> None:
        for node in self.nodes:
            node.render()
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
        self.render()
        self.draw()

    def set_font(self) -> None:
        self.font = pygame.font.Font(
            os.path.join(App.program_dir, "Courier_New.ttf"), self.fontsize
        )

    def render(self) -> None:
        try:
            if self.text[0] == " ":
                self.text = self.text[1:]
        except IndexError:
            pass
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos
        self.cursor = Rect(self.rect.topright, (3, self.rect.height))
        self.rect = Rect(
            self.pos, (pygame.display.get_surface().get_width(), self.fontsize)
        )

    def draw(self) -> None:
        App.screen.blit(self.img, self.rect)

    def check_mouse(self, mouse) -> bool:
        return self.rect.collidepoint(mouse)

    def rollover(self) -> list:
        return_indicies = [0]
        possible_splits = [i for i, char in enumerate(self.text) if char == " "]
        max_move_length = max([len(move) for move in App.computer.scramble.split(" ")])
        high = (
            pygame.display.get_surface().get_width() // (App.fonts[self.fontsize][0])
        ) - 1
        low = high - max_move_length
        while possible_splits:
            try:
                return_indicies.append(
                    max([num for num in possible_splits if low <= num <= high])
                )
            except ValueError:
                return_indicies.append(possible_splits[-1])
            possible_splits = [
                idx for idx in possible_splits if idx > return_indicies[-1]
            ]
            delta_index = return_indicies[-1] - return_indicies[-2]
            low += delta_index
            high += delta_index
        return return_indicies[1:]


class Button(Textbox):
    def __init__(self, pos, text, fontsize) -> None:
        super().__init__(pos, text, False, fontsize)

    def render(self) -> None:
        try:
            if self.text[0] == " ":
                self.text = self.text[1:]
        except IndexError:
            pass
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos


def main() -> None:
    App().run()


if __name__ == "__main__":
    main()
