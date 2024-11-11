"""
Settings Menu for Logic Quest

This module creates a settings menu for the 'Logic Quest' game using Pygame. 
The menu provides volume control options and displays game control information.

Classes:
    Button: Represents an interactive button in the settings menu.

Functions:
    increase_volume(): Increases the game's volume.
    decrease_volume(): Decreases the game's volume.
    main_menu(): Returns to the main game menu.
    draw_controls_info(win, width, height): Displays the game controls information.
    main(): Main function to execute the settings menu.

Author: Muzzammil Mdathir
Date: 31/3/2024
Version: 1.0
"""
import pygame
import sys
import subprocess

# Initialize the Pygame
pygame.init()
# Initialize the mixer for volume control
pygame.mixer.init()
# Initialize the font
pygame.font.init()

# Get the screen size
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Logic Quest")

BG = pygame.transform.scale(pygame.image.load("backgrounds/bg_offwhite.jpg"), (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 150, 255)

current_volume = 0.5  # Initial volume level (50%)


class Button:
    """
    A class representing a button in the settings menu.
    
    Attributes:
        text (str): The text displayed on the button.
        color (tuple): The button color.
        width, height (int): Dimensions of the button.
        pos (tuple): The position of the button on the screen.
        elevation (int): The elevation effect for the button.
        action (callable): The function to execute when the button is clicked.

    Methods:
        draw(win): Renders the button onto the provided Pygame window.
        checkClick(win): Checks and handles click events on the button.
    """
    def __init__(self, text, color, width, height, pos, elevation, action=None):
        # Attributes
        self.pressed = False
        self.elevation = elevation
        self.dElevation = elevation
        self.original_y_position = pos[1]
        self.action = action

        # Top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = color
        self.main_color = color

        # Bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = BLACK

        # Text
        self.text_surf = pygame.font.SysFont('Arial', 50).render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, win):
        # Elevate the button
        self.top_rect.y = self.original_y_position - self.dElevation
        self.text_rect.center = self.top_rect.center

        # Shadow position
        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)

        self.checkClick(win)

    def checkClick(self, win):
        global current_volume
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#0096FF'
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                self.pressed = True
                self.dElevation = 0
                if self.action:  # Check and call the action
                    self.action()  # Execute the action if the button is pressed
            else:
                self.dElevation = self.elevation
        else:
            self.top_color = self.main_color
            self.dElevation = self.elevation
        if not pygame.mouse.get_pressed()[0]:
            self.pressed = False


# Functions for button actions
def increase_volume():
    """Increases the game's volume."""
    global current_volume
    current_volume = min(1.0, current_volume + 0.05)
    pygame.mixer.music.set_volume(current_volume)


def decrease_volume():
    """Decreases the game's volume."""
    global current_volume
    current_volume = max(0.0, current_volume - 0.05)  # Decrease volume, min out at 0.0
    pygame.mixer.music.set_volume(current_volume)


def main_menu():
    """Navigates back to the main game menu."""
    path = 'landingPage.py'
    subprocess.run([sys.executable, path])
    pygame.quit()

'''
def draw_controls_info(win, width, height):
    """
    Draws the controls information on the screen.
    Args:
        win (pygame.Surface): The Pygame window surface.
        width, height (int): The width and height of the window.
    """
    # Set up the font and size for the controls text
    controls_font = pygame.font.SysFont('Arial', 40)
    # Define the controls information text
    controls_text = [
        "Controls:",
        "Pause: P / CTRL P",
        "Quit: ESC",
        "Save: S / CTRL S",
        "Skip to Next Question: N / CTRL N"
    ]
    start_y = height * 0.425
    line_spacing = 40  # Spacing between lines

    for i, text in enumerate(controls_text):
        text_surface = controls_font.render(text, True, BLACK)
        # Center align text, adjust x as needed for your layout
        text_rect = text_surface.get_rect(center=(width / 2, start_y + i * line_spacing))
        win.blit(text_surface, text_rect)
'''

def main():
    global WIN
    run = True
    WIN.blit(BG, (0, 0))
    clock = pygame.time.Clock()

    # Initialize buttons with descriptions
    buttons = [
        Button("-", '#89CFF0', 100, 80, (WIDTH / 2 - 100, HEIGHT / 2 - 200), 6, decrease_volume),
        Button("+", '#89CFF0', 100, 80, (WIDTH / 2 + 100, HEIGHT / 2 - 200), 6, increase_volume),
        Button("BACK TO MAIN MENU", '#89CFF0', 460, 80, (WIDTH / 2 - 460 / 2, HEIGHT / 2 + 150), 6, main_menu)
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

        # draw a title on screen
        font = pygame.font.SysFont('Arial', 100)
        text = font.render("SETTINGS", True, BLACK)
        WIN.blit(BG, (0, 0))  # Redraw background for a clean slate
        WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, 100))  # Redraw the title

        # Optionally, show current volume on screen
        volume_text = pygame.font.SysFont('Arial', 50).render(f"Volume: {int(current_volume * 100)}%", True, BLACK)
        WIN.blit(volume_text, (WIDTH / 2 - volume_text.get_width() / 0.5, HEIGHT / 3.25))

        # Draw each button
        for button in buttons:
            button.draw(WIN)


        pygame.display.update()
        clock.tick(40)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
