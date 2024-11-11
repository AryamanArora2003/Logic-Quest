"""
This module implements the mode menu of the application using Pygame. 
It provides a user interface for selecting different game modes.

Classes:
    Button: A class to represent an interactive button in the UI.

Functions:
    main_menu(): Function to return to the main menu.
    tutorial(): Function to start the tutorial.
    main(): The main function to execute the mode menu interface.
Author: Muzzammil Mudathir
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

# Get the screen size
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Logic Quest")

# load background image
BG = pygame.transform.scale(pygame.image.load("backgrounds/bg_offwhite.jpg"), (WIDTH, HEIGHT))

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 150, 255)

current_description = ""  # global variable for the description

# Calculate the center coordinates
center_x = WIDTH / 2 - 200 / 2
center_y = HEIGHT / 2 - 100 / 2


class Button:
    """
    Class to create an interactive button in the UI.

    Attributes:
        text (str): Text displayed on the button.
        color (str): Color of the button.
        width, height (int): Dimensions of the button.
        pos (tuple): Position of the button.
        elevation (int): Elevation of the button for a 3D effect.
        description (str): Description shown when the button is hovered.
        action (callable): Action performed when the button is clicked.

    Methods:
        draw(win): Renders the button onto the specified window.
        checkClick(win): Handles mouse click events for the button.
        show_description(win): Displays the button's description.
    """

    def __init__(self, text, color, width, height, pos, elevation, description="", action=None):
        # attributes
        self.pressed = False
        self.elevation = elevation
        self.dElevation = elevation
        self.original_y_position = pos[1]
        self.description = description
        self.action = action

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = color
        self.main_color = color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = BLACK

        # text
        self.text_surf = pygame.font.SysFont('Arial', 50).render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, win):

        # elevate the button
        self.top_rect.y = self.original_y_position - self.dElevation
        self.text_rect.center = self.top_rect.center

        # shadow position
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dElevation

        # handle mouse events and hover effects
        pygame.draw.rect(WIN, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(WIN, self.top_color, self.top_rect, border_radius=12)
        WIN.blit(self.text_surf, self.text_rect)

        self.checkClick(win)

    def checkClick(self, win):
        global current_description
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#0096FF'
            self.show_description(win)
            if pygame.mouse.get_pressed()[0]:
                self.dElevation = 0
                self.pressed = True
            else:
                self.dElevation = self.elevation
                if self.pressed:
                    print("Button Clicked")
                    self.pressed = False
        else:
            self.dElevation = self.elevation
            self.top_color = self.main_color
            if current_description == self.description:
                current_description = ""
        if self.pressed:
            if self.action:
                self.action()
            self.pressed = False

    def show_description(self, win):
        # Display description text on hover
        if self.description:
            description_surf = pygame.font.SysFont('Arial', 30).render(self.description, True, BLACK)
            description_rect = description_surf.get_rect(center=(WIDTH / 2, HEIGHT - 200))
            pygame.draw.rect(win, '#0096FF', description_rect.inflate(30, 10), border_radius=5)
            win.blit(description_surf, description_rect)


def main_menu():
    """
    Returns to the main menu of the application.
    """
    path = "landingPage_1.py"
    subprocess.run([sys.executable, path])
    pygame.quit()


def tutorial():
    """
    Starts the tutorial of the game.
    """
    pygame.mixer.music.stop()
    path = 'tutorial.py'
    subprocess.run([sys.executable, path])
    pygame.quit()


def instructor_mode():
    path = "instructorMode.py"
    subprocess.run([sys.executable, path])
    pygame.quit()


def developer_mode():
    path = "developerMode.py"
    subprocess.run([sys.executable, path])
    pygame.quit()


def main():
    """
    The main function of the script. It initializes the mode menu and handles user interactions.
    """
    global WIN, current_description
    run = True
    WIN.blit(BG, (0, 0))
    clock = pygame.time.Clock()

    # Initialize buttons with descriptions
    buttons = [
        Button("Instructor Mode", '#89CFF0', 340, 80, (WIDTH / 2 - 340 / 2, HEIGHT / 2 - 200), 6,
                       "For educators to view, add questions, and navigate through an intuitive interface. Features adding questions with multiple choice options.", instructor_mode),
        Button("Developer Mode", '#89CFF0', 365, 80, (WIDTH / 2 - 360 / 2, HEIGHT / 2 - 80), 6,
                       "Designed for developing the game, prints out command inputs.", developer_mode),
        Button("TUTORIAL", '#89CFF0', 390, 80, (WIDTH / 2 - 385 / 2, HEIGHT / 2 + 40), 6, action=tutorial),
        Button("BACK TO MAIN MENU", '#89CFF0', 460, 80, (WIDTH / 2 - 460 / 2, HEIGHT / 2 + 150), 6, action=main_menu)
    ]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
            if event.type == pygame.VIDEORESIZE:
                WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # draw()

        # draw a title on screen
        font = pygame.font.SysFont('Arial', 100)
        text = font.render("GAME MODES", True, BLACK)
        WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, 100))

        # Clear the screen before drawing buttons
        WIN.blit(BG, (0, 0))  # Redraw background for a clean slate
        WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, 50))  # Redraw the title

        # Draw each button
        for button in buttons:
            button.draw(WIN)

        pygame.display.update()
        clock.tick(40)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
