"""
Login Interface for Logic Quest Game

This module implements a login interface for the 'Logic Quest' game using Pygame. 
It features text input boxes for username and optional key, with logic to handle different user roles.

Classes:
    TextInputBox: Manages text input for username and key.
    Button: Represents a button in the interface.

Functions:
    create_button(msg, width, height, x, y, hc, dc, fc): Creates and manages a button.
    login(): Manages the login process.
    landing(): Transitions to the main user interface.
    landing_1(): Transitions to an alternative main user interface for specific users.
    main(): Main function to execute the login interface.
"""
import pygame
import sys
import subprocess

pygame.init()

# Get the screen size
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("logic game")

clock = pygame.time.Clock()

BG = pygame.transform.scale(pygame.image.load("backgrounds/bg_offwhite.jpg"), (WIDTH, HEIGHT))
font = pygame.font.SysFont("Ariel", 60)
largefont = pygame.font.SysFont("Ariel", 100)
smallfont = pygame.font.SysFont("Ariel", 50)
black = (10, 10, 10)
grey = (112, 128, 144)
blue = (0, 0, 255)


class TextInputBox:
    """
    A class for handling text input fields.

    Attributes:
        x, y (int): The x and y coordinates of the text box.
        width, height (int): The width and height of the text box.
        font (pygame.font.Font): The font used for the text.
        text_color, inactive_color, active_color (tuple): Color specifications for text and box states.

    Methods:
        handle_event(event): Processes events related to the text box.
        draw(win): Draws the text box on the screen.
    """
    def __init__(self, x, y, width, height, font, text_color, inactive_color, active_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = inactive_color
        self.text = ''
        self.font = font
        self.text_color = text_color
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.active_color if self.active else self.inactive_color
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, win):
        txt_surface = self.font.render(self.text, True, self.text_color)
        width = max(self.rect.w, txt_surface.get_width() + 10)
        self.rect.w = width
        win.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(win, self.color, self.rect, 2)


def create_button(msg, width, height, x, y, hc, dc, fc):
    """
    Creates a button with specified properties.

    Args:
        msg (str): Text to be displayed on the button.
        width, height (int): Dimensions of the button.
        x, y (int): Coordinates for the button placement.
        hc, dc, fc (tuple): Colors for hover, default, and font.

    Returns:
        bool: True if the button is clicked, False otherwise.
    """
    button_width = width
    button_height = height

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

    if (x + button_width > mouse[0] > x and y + button_height > mouse[1] > y):
        pygame.draw.rect(WIN, hc, (x, y, button_width, button_height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(WIN, dc, (x, y, button_width, button_height))

    buttontext = smallfont.render(msg, True, fc)
    text_rect = buttontext.get_rect(center=(x + button_width / 2, y + button_height / 2))
    WIN.blit(buttontext, text_rect)


def landing():
    """
    Transitions to the main menu interface for regular users.
    """
    path = "landingPage.py"
    subprocess.run([sys.executable, path])
    pygame.quit()

def landing_1():
    """
    Transitions to the main menu interface for instructors or developers.
    """
    path = "landingPage_1.py"
    subprocess.run([sys.executable, path])
    pygame.quit()


def login():
    """
    Manages the login procedure, including user input handling and screen transition.
    """
    login_text = largefont.render("Login Page", True, black)
    username_text = smallfont.render("Username: ", True, black)
    key_text = smallfont.render("Key(Optional): ", True, black)

    box_width = 250
    box_height = 50
    dark_grey = (50, 50, 50)
    dark_blue = (0, 0, 128)
    username_box = TextInputBox((WIDTH - box_width) / 2, 320, box_width, box_height, font, black, dark_grey, dark_blue)
    key_box = TextInputBox((WIDTH - box_width) / 2, 420, box_width, box_height, font, black, dark_grey, dark_blue)

    while True:
        WIN.blit(BG, (0, 0))
        WIN.blit(login_text, ((WIDTH - login_text.get_width()) / 2, 40))
        WIN.blit(username_text, ((WIDTH - username_text.get_width()) / 2, 280))
        WIN.blit(key_text, ((WIDTH - key_text.get_width()) / 2, 380))

        username_box.draw(WIN)
        key_box.draw(WIN)

        p_button = create_button("Proceed", 150, 50,  WIDTH / 2 - 75, 500, grey, blue, black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            username_box.handle_event(event)
            key_box.handle_event(event)

        with open('usernames.txt', 'r') as file:
            with open('keys.txt', 'r') as file2:
                content = file.read()
                content2 = file2.read()
                if username_box.text == '' and p_button:
                    err1_msg = smallfont.render("Input Username", True, black)
                    WIN.blit(err1_msg, ((WIDTH/2) - 20, (HEIGHT/2)))
                if username_box.text in content and username_box.text != '':
                    if p_button and key_box.text == '':
                        print("Proceed to main menu")
                        with open('cur_username.txt', 'w') as file3:
                            file3.write(username_box.text)
                        landing()

                    elif p_button and key_box.text in content2:
                        print("Proceed to main menu as instructor/developer")
                        with open('cur_username.txt', 'w') as file3:
                            file3.write(username_box.text)
                        landing_1()
                    elif p_button and key_box.text not in content2:
                        err2_msg = smallfont.render("Invalid Key", True, black)
                        WIN.blit(err2_msg, ((WIDTH/2)-20, HEIGHT/2))
                elif p_button and username_box.text not in content and username_box.text != '':
                    print("New account added proceed as user")
                    with open('cur_username.txt', 'w') as file3:
                        file3.write(username_box.text)
                    update = False
                    with open('usernames.txt', 'r') as f:
                        lines = f.read().split('\n')
                        length = len(lines)
                        new_lines = []
                        for i in range(length):
                            new_lines.append(lines[i])
                        new_lines.append(username_box.text)
                        update = True

                    if update:
                        with open('usernames.txt', 'w') as f:
                            for i in range(len(new_lines)):
                                if new_lines[i] != '':
                                    f.write(str(new_lines[i]))
                                    f.write('\n')
                    print(new_lines)
                    landing()


        pygame.display.update()
        clock.tick(15)


def main():
    """
    The main function to execute the login interface, including initializing the game loop.
    """
    run = True
    while run:
        if login():
            run = False
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            # quit if u enter escape
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
    pygame.quit()


if __name__ == "__main__":
    main()