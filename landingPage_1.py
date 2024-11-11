"""
This module contains the implementation of the main landing page of the application.

Classes:
    Button: Represents a button in the application GUI.

Functions:
    quit_game(): Quits the game and closes the application.
    play_game(): Launches the game.
    settings(): Opens the settings menu.
    leaderboard(): Opens the leaderboard.
    main(): The main function of the script.

Author: Kassem Kanjo
Date: 30/3/2024
Version: 1.0
"""
import pygame
import sys
import subprocess

# Initialize the Pygame
pygame.init()
# initialize the font
pygame.font.init()
# initialize the mixer
pygame.mixer.init()

pygame.mixer.music.load('audios/Monkeys-Spinning-Monkeys(chosic.com).mp3')
#pygame.mixer.music.load('audios/Move-Forward(chosic.com).mp3')
pygame.mixer.music.play(-1, fade_ms=1000)


# Get the screen size
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Logic Quest")

# load background image
BG = pygame.transform.scale(pygame.image.load("backgrounds/bg_offwhite.jpg"),(WIDTH, HEIGHT))

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)


# Calculate the center coordinates
center_x = WIDTH / 2 - 200 / 2
center_y = HEIGHT / 2 - 100 / 2


class Button:
    """
    class used to represent a button in the application GUI.

    Attributes:
        text (str): The text displayed on the button.
        color (tuple): The color of the button.
        width (int): The width of the button.
        height (int): The height of the button.
        pos (tuple): The position of the button.
        elevation (int): The elevation of the button.
        action (function): The action performed when the button is pressed.

    Methods:
        draw(): Draws the button on the screen.
        checkClick(): Checks if the button is clicked and updates its state.
    """
    def __init__(self,text, color, width, height, pos, elevation, action=None):
        #attributes
        self.pressed = False
        self.elevation = elevation
        self.dElevation = elevation
        self.original_y_position = pos[1]
        self.action = action

        #top rectangle
        self.top_rect = pygame.Rect(pos,(width, height))
        self.top_color = color
        self.main_color = color

        #bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = BLACK


        #text
        self.text_surf = pygame.font.SysFont('Arial', 50).render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)


    def draw(self):
        #elevate the button
        self.top_rect.y = self.original_y_position - self.dElevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dElevation

        pygame.draw.rect(WIN, self.bottom_color, self.bottom_rect, border_radius = 12)
        pygame.draw.rect(WIN, self.top_color, self.top_rect, border_radius = 12)
        WIN.blit(self.text_surf, self.text_rect)
        self.checkClick()


    def checkClick(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#0096FF'
            if pygame.mouse.get_pressed()[0]:
                self.dElevation = 0
                self.pressed = True
            else:
                self.dElevation = self.elevation
                if self.pressed:
                    self.pressed = False
        else:
            self.dElevation = self.elevation
            self.top_color = self.main_color

        if self.pressed:
            if self.action:
                self.action()
            self.pressed = False

def quit_game():
    """
    Quits the game and closes the application.
    """
    pygame.quit()
    sys.exit()

def play_game():
    """
    Takes you to choose the game mode.
    """
    pygame.mixer.music.stop()
    path = 'modemenu_1.py'
    subprocess.run([sys.executable, path])
    pygame.quit()

def settings():
    """
    Opens the settings menu.
    """
    pygame.mixer.music.stop()
    path = 'Settings.py'
    subprocess.run([sys.executable, path])
    pygame.quit()

def leaderboard():
    """
    Opens the leaderboard.
    """
    pygame.mixer.music.stop()
    path = 'Leaderboard.py'
    subprocess.run([sys.executable, path])
    pygame.quit()



# create the buttons
start_button = Button("START GAME", '#89CFF0', 320, 80, (WIDTH/2 - 320/2, HEIGHT/2 - 250), 6,play_game)
load_button = Button("LOAD GAME", '#89CFF0', 320, 80, (WIDTH/2 - 320/2, HEIGHT/2 - 150), 6)
settings_button = Button("SETTINGS", '#89CFF0', 320, 80, (WIDTH/2 - 320/2, HEIGHT/2 - 50), 6, settings)
leaderboard_button = Button("LEADERBOARD", '#89CFF0', 320, 80, (WIDTH/2 - 320/2, HEIGHT/2 + 50), 6, leaderboard)
quit_button = Button("QUIT", '#89CFF0', 320, 80, (WIDTH/2 - 320/2, HEIGHT/2 + 150), 6, quit_game)

def main():
    """
    The main function of the script. Initializes the GUI and enters the main loop.
    """
    global WIN
    run = True
    WIN.blit(BG, (0,0))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            '''
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
            '''
            if event.type == pygame.VIDEORESIZE:
                WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # draw a title on screen
        font = pygame.font.SysFont('Arial', 100)
        text = font.render("LOGIC QUEST", True, BLACK)
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, 100))

        # draw the buttons
        start_button.draw()
        load_button.draw()
        settings_button.draw()
        leaderboard_button.draw()
        quit_button.draw()

        # write text
        font = pygame.font.SysFont('Arial', 35)
        text = font.render("Authors: Kassem Kanjo, Muzzammil Mudathir, Aryaman Arora, Michael Peter Timothy Turkstra", True, BLACK)
        WIN.blit(text, (WIDTH/2 - text.get_width()+1200/2, HEIGHT - 250))
        # make second half of the text
        text = font.render("Mohammad Shayaan Shahid", True, BLACK)
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT - 210))
        text = font.render("Team 31", True, BLACK)
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT - 165))
        text = font.render("Winter 2023-2024", True, BLACK)
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT - 120))
        text = font.render("Created as part of CS 2212 at Western University", True, BLACK)
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT - 75))
        # write 'ESC to quit' text
        font = pygame.font.SysFont('Arial', 35)
        text = font.render("ESC to quit", True, BLACK)
        WIN.blit(text, (10, 10))

        pygame.display.update()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
