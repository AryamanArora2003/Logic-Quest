
"""
add question Screen for Pygame Application

This module implements an interactive input screen for the 'Logic Quest' game using Pygame. 
It features text input boxes for question creation and options, along with buttons for submission and return.

Classes:
    Button: A class for creating interactive buttons.
    TextInputBox: A class for creating and handling text input fields.

Functions:
    draw_labels(): Draws labels for the text input boxes on the screen.
    append_to_file(file_path, data): Appends data to a specified file with index management.
    submit_action(text_boxes): Handles the action of the submit button.
    main(): The main function to run the input screen interface.
"""
import pygame
import os

pygame.init()

# Screen setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)  # Make the screen resizable
pygame.display.set_caption("Input Screen")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font
FONT = pygame.font.SysFont(None, 32)

# Load and scale the background image
bg = pygame.image.load("backgrounds/bg_offwhite.jpg")
bg_rescaled = pygame.transform.scale(bg, (width, height))

# Blit the background
screen.blit(bg_rescaled, (0, 0))

# Button class
class Button:
    """
    Class to create an interactive button in the UI.

    Attributes:
        text (str): Text displayed on the button.
        x, y (int): X and Y position of the button.
        width, height (int): Width and height of the button.
        action (callable): Function to execute on button click.

    Methods:
        draw(win): Draws the button on the specified window.
        clicked(pos): Checks if the button is clicked at the given mouse position.
    """
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action

    def draw(self, win):
        pygame.draw.rect(win, GRAY, (self.x, self.y, self.width, self.height))
        text_surf = FONT.render(self.text, True, BLACK)
        win.blit(text_surf, (self.x + (self.width - text_surf.get_width()) / 2, self.y + (self.height - text_surf.get_height()) / 2))

    def clicked(self, pos):
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

# Text box class
class TextBox:
    """
    Class for creating and handling a text input box.

    Attributes:
        rect (pygame.Rect): Rectangle defining the input box's size and position.
        text (str): Text entered in the box.
        active (bool): Whether the input box is currently active.

    Methods:
        handle_event(event): Handles events for the input box.
        draw(win): Draws the input box on the specified window.
    """
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, win):
        pygame.draw.rect(win, WHITE, self.rect)
        pygame.draw.rect(win, BLACK, self.rect, 2)
        text_surf = FONT.render(self.text, True, BLACK)
        win.blit(text_surf, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surf.get_height()) / 2))

# Initialize text boxes and labels
labels = ["Question description", "Question solution", "Question Difficulty", "Option 1", "Option 2", "Option 3", "Option 4", "You must fill in all textboxes before you can click submit"]

# Function to draw labels
def draw_labels():
    """
    Draws labels for each text input box on the screen.
    """
    for i, label in enumerate(labels):
        label_surf = FONT.render(label, True, BLACK)
        screen.blit(label_surf, (50, 30 + i * 60))

# Function to append data to a file with index management
def append_to_file(file_path, data):
    """
    Appends data to a file, managing indexes for new entries.

    Args:
        file_path (str): Path of the file to which data is appended.
        data (str): Data to be appended to the file.
    """
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as f:
            f.write("1." + data + "\n")
    else:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Find the last non-empty line with a valid index
        index = 0
        for line in reversed(lines):
            try:
                index = int(line.split('.')[0])
                break
            except ValueError:
                continue  # Skip lines that don't start with an integer

        # If no valid index was found, start from 1; otherwise, increment the last index
        index = index + 1 if index else 1
        new_line = f"{index}.{data}\n"

        with open(file_path, 'a') as f:
            f.write(new_line)


# Function to handle submit button click
def submit_action(text_boxes):
    """
    Handles the submit button action, writing input data to files.

    Args:
        text_boxes (list[TextInputBox]): List of text input boxes.
    """
    # Check if all textboxes have input
    if all(box.text.strip() for box in text_boxes):
        # Append to files
        append_to_file("questions.txt", text_boxes[0].text)
        append_to_file("answers.txt", text_boxes[1].text)
        append_to_file("difficulty.txt", text_boxes[2].text)

        # Format the options.txt file to maintain the correct text format
        if not os.path.isfile("options.txt"):
            with open("options.txt", 'w') as f:
                f.write("1.\n")
                for i in range(3, 7):
                    f.write(text_boxes[i].text + "\n")
                f.write("\n")
        else:
            with open("options.txt", 'r') as f:
                lines = f.readlines()

            index = 0
            for line in reversed(lines):
                try:
                    index = int(line.split('.')[0])
                    break
                except ValueError:
                    continue

            index = index + 1 if index else 1
            with open("options.txt", 'a') as f:
                f.write(f"{index}.\n")
                for i in range(3, 7):
                    f.write(text_boxes[i].text + "\n")
                f.write("\n")

        # Clear the textboxes after submission
        for box in text_boxes:
            box.text = ""



def main():
    """
    Main function to run the input screen. It initializes the screen, 
    handles events, and updates the display.
    """
    global width, height, screen, bg_rescaled

    run = True
    clock = pygame.time.Clock()

    text_boxes = [TextBox(50, 50 + i * 60, 140, 30) for i in range(7)]
    return_button = Button('Return', 50, height - 60, 100, 50)
    submit_button = Button('Submit', width - 150, height - 60, 100, 50)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                bg_rescaled = pygame.transform.scale(bg, (width, height))

            for box in text_boxes:
                box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if submit_button.clicked(mouse_pos):
                    submit_action(text_boxes)
                elif return_button.clicked(mouse_pos):
                    run = False  # This will close the window when the return button is clicked

        screen.fill(WHITE)
        screen.blit(bg_rescaled, (0, 0))

        draw_labels()

        for box in text_boxes:
            box.draw(screen)

        return_button.draw(screen)
        submit_button.draw(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()