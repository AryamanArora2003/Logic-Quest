"""
This module contains the implementation of a graphical user interface for the tutorial page of the game. It includes a customizable button class.

Classes:
    Button: Represents a clickable button in the GUI.

Functions:
    main_menu(): Navigates to the main menu of the application.
    main(): The main function of the script that runs the GUI loop.
Author: Kassem Kanjo
Date: 30/3/2024
Version: 1.0
"""
import pygame
import sys
import subprocess
import time


# Initialize the Pygame
pygame.init()

# Get the screen size
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Logic Quest")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# load background image
BG = pygame.transform.scale(pygame.image.load("backgrounds/bg_offwhite.jpg"),(WIDTH, HEIGHT))


class Button:
    """
    class to create a clickable button in the GUI.

    Attributes:
        text (str): Text displayed on the button.
        color (str): Background color of the button.
        width (int): Width of the button.
        height (int): Height of the button.
        pos (tuple): X and Y position of the button.
        elevation (int): Elevation of the button to create a 3D effect.
        action (callable): Function to execute when the button is clicked.

    Methods:
        draw(): Renders the button onto the screen.
        checkClick(): Checks if the button is clicked and triggers the action.
    """
    def __init__(self,text, color, width, height, pos, elevation, action=None):
        #attributes
        self.pressed = False
        self.elevation = elevation
        self.dElevation = elevation
        self.original_y_position = pos[1]
        self.action = action
        self.last_click_time = 0

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
        current_time = time.time()
        if current_time - self.last_click_time < 0.5:
            return
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
            self.last_click_time = current_time
            if self.action:
                self.action()
            self.pressed = False


def main_menu():
    """
    Navigates to the main menu of the application.
    """
    path = "modemenu.py"
    subprocess.run([sys.executable, path])
    pygame.quit()


# Define tutorial pages functions here

def draw_text(text, size, position):
    font = pygame.font.SysFont('Arial', size)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=position)
    WIN.blit(text_surf, text_rect)

def draw_tutorial_page_1():
    # Constants for positioning and text sizes
    center_x = WIDTH // 2
    large_text_size = 50
    normal_text_size = 30
    section_gap = HEIGHT // 16  # Adjust the gap for spacing between sections

    # Helper function to calculate Y positions
    def calc_y(base, multiplier):
        return HEIGHT // 4 + section_gap * multiplier

    # Title
    draw_text('Welcome to Logic Quest!', large_text_size, (center_x, calc_y(0, 0)))

    # Introduction section
    intro_text = [
        'Logic Quest is a fun way to learn propositional logic statements. This game features many different modes to choose from.',

    ]
    for i, text in enumerate(intro_text):
        draw_text(text, normal_text_size, (center_x, calc_y(0, i+1)))

    # Instructions section
    instructions_text = [
        'Training Mode:',
        'Unlimited time to read and answer by dragging options to a submission box. Questions cannot be skipped until right answer is chosen.',
        'Lightning Mode:',
        'Fast-paced, with a time limit. Similar drag-and-drop gameplay but with points for correct answers and a leaderboard.',
        'Instructor Mode:',
        'For educators to view, add questions, and navigate through an intuitive interface.',
        'Features adding questions with multiple choice options. Can only be accessed by existing users.',
        'Developer Mode:',
        'Designed for developing the game, prints out command inputs.',
        'Can only be accessed by existing users.'
    ]
    for i, text in enumerate(instructions_text):
        draw_text(text, normal_text_size, (center_x, calc_y(0, i+2)))



def draw_tutorial_page_2():
    # Content for page 2
    draw_text('Controls', 50, (WIDTH // 2, HEIGHT // 4))
    draw_text('Drag/Drop onto Answer Box', 30, (WIDTH // 2, HEIGHT // 3.15))
    draw_text('Pause: Command P / CTRL P', 30, (WIDTH // 2, HEIGHT // 2.65))
    draw_text('Save: Command S / CTRL S', 30, (WIDTH // 2, HEIGHT // 2.25))
    draw_text('Quit: ESC', 30, (WIDTH // 2, HEIGHT // 1.95))



current_page = 1
total_pages = 2


def go_next_page():
    global current_page
    if current_page < total_pages:
        current_page += 1


def go_previous_page():
    global current_page
    if current_page > 1:
        current_page -= 1


back_button = Button("Back", "#89CFF0", 150, 75, (50, 50), 6, main_menu)
next_button = Button("Next", "#89CFF0", 150, 75, (WIDTH - 200, HEIGHT - 100), 6, go_next_page)
previous_button = Button("Previous", "#89CFF0", 150, 75, (50, HEIGHT - 100), 6, go_previous_page)


def main():
    global WIN
    run = True
    while run:
        WIN.blit(BG, (0, 0))  # Reset background at the start of each loop iteration

        # Draw current tutorial page
        if current_page == 1:
            draw_tutorial_page_1()
        elif current_page == 2:
            draw_tutorial_page_2()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.VIDEORESIZE:
                WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # Draw the navigation and action buttons
        back_button.draw()
        if current_page < total_pages:
            next_button.draw()
        if current_page > 1:
            previous_button.draw()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()


back_button = Button("Back", "#89CFF0", 150, 75, (50,50), 6, main_menu)

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
            if event.type == pygame.VIDEORESIZE:
                WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        # Draw the buttons
        back_button.draw()
        pygame.display.update()

    
    pygame.quit()

if __name__ == "__main__":
    main()