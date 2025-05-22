import os
import pygame


def generate_fontsizes(file_in) -> None:
    os.chdir("resources/fonts/")
    output_str = ""

    for size in range(120):
        font = pygame.font.Font(file_in, size)
        width, height = font.size("A")
        output_str += f"{width},{height}\n"
    output_str = output_str[:-1]

    with open(f"{file_in}.txt", "w", encoding="utf-8") as f:
        f.write(output_str)

    os.chdir("../..")


if __name__ == "__main__":
    pygame.init()
    input_file = input("Input the font file name: ")
    os.chdir("../")
    generate_fontsizes(input_file)
    pygame.quit()
