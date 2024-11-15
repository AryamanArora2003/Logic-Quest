"""
Lightning Mode Quiz Game

This module contains a Pygame-based quiz game, where players answer questions by dragging and dropping answers. 
It includes functionalities for displaying questions, tracking scores, and a countdown timer.

Classes:
    Button: Represents a clickable button in the game.
    DraggableItem: Represents a draggable item for answer selection.

Global Variables:
    WIDTH, HEIGHT: Dimensions of the game window.
    WIN: Pygame window surface.
    BG: Background image for the game.
    font, mediumfont, smallfont: Different fonts used in the game.

Functions:
    get_question_text(): Retrieves the text for the current question.
    get_question_number_text(): Retrieves the text for the current question number.
    get_current_options(): Retrieves the current set of answer options.
    get_current_answer(): Retrieves the correct answer for the current question.
    create_draggable_items(): Creates draggable items for answer options.

Author: Michael
Date: 31/03/2024
Version: 1.0
"""
import pygame
import sys
import time
import subprocess

def main():
    # Initialize Pygame
    pygame.init()

    # Get the screen size
    screen_info = pygame.display.Info()
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Lightning Mode")

    clock = pygame.time.Clock()

    BG = pygame.transform.scale(pygame.image.load("backgrounds/bg_offwhite.jpg"),(WIDTH, HEIGHT))
    font = pygame.font.SysFont("arial", 45)
    mediumfont = pygame.font.SysFont("arial", 30)
    smallfont = pygame.font.SysFont("arial", 20)
    black = (10, 10, 10)
    grey = (112, 128, 144)
    red = (255, 0, 0)

    TOP_MARGIN = 50
    BOTTOM_MARGIN = 100
    LEFT_MARGIN = 50
    ANSWER_BANK_Y = HEIGHT - BOTTOM_MARGIN + 20
    BLANKS_Y = TOP_MARGIN + 200
    BLANK_WIDTH = 100
    BLANK_HEIGHT = 30
    BLANK_SPACING = 20
    ANSWER_ITEM_SPACING = 120
    SOL_BOX_X = (WIDTH - BLANK_WIDTH) // 2
    SOL_BOX_Y = (HEIGHT - BLANK_HEIGHT) // 2

    current_question_index = 0
    player_score = 0
    num_correct = 0

    with open('cur_username.txt', 'r') as f:
        username = f.read()

    with open('questions.txt', 'r') as f:
        questions = []
        for line in f:
            if '.' in line:
                # Split line at the first dot and take the second part
                line_text = line.split('.', 1)[1].strip()
                questions.append(line_text)

    with open('options.txt', 'r') as f:
        raw_options = f.read().split('\n\n')
        options = [option.strip().split('\n') for option in raw_options]

    with open('answers.txt', 'r') as f:
        answers = []
        for line in f:
            if '.' in line:
                # Split line at the first dot and take the second part
                line_text = line.split('.', 1)[1].strip()
                answers.append(line_text)

    with open('difficulty.txt', 'r') as f:
        difficulties = []
        for line in f:
            dif = line.strip().split('.')[1]
            difficulties.append(int(dif))

    def get_question_text():
        return mediumfont.render(questions[current_question_index], True, black)

    def get_question_number_text():
        return font.render(f"Question Number: {current_question_index + 1}", True, black)

    def get_current_options():
        return options[current_question_index]

    def get_current_answer():
        return options[current_question_index]

    class Button:
        """
        A class to represent a button in the game's interface.
        Methods include drawing the button and checking if it's hovered over or clicked.
        """
        def __init__(self, color, x, y, width, height, text=''):
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text

        def draw(self, win, outline=None):
            if outline:
                pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

            if self.text != '':
                font = pygame.font.SysFont('arial', 20)
                text = font.render(self.text, 1, (0, 0, 0))
                win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        def is_over(self, pos):
            # Pos is the mouse position or a tuple of (x,y) coordinates
            if self.x < pos[0] < self.x + self.width:
                if self.y < pos[1] < self.y + self.height:
                    return True
            return False

    class DraggableItem:
        """
        A class to represent a draggable item for answering questions in the game.
        It handles events related to dragging and dropping items.
        """
        def __init__(self, text, x, y, w, h, font, sol):
            self.text = text
            self.rect = pygame.Rect(x, y, w, h)
            self.font = font
            self.dragging = False
            self.offset_x = 0
            self.offset_y = 0
            self.sol = sol

        def draw(self, win):

            pygame.draw.rect(win, grey, self.rect)

            text_surface = self.font.render(self.text, True, black)

            win.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


        def handle_event(self, event):
            global current_question_index  # Reference the global variable
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mouse_x, mouse_y = event.pos
                    self.rect.x = mouse_x + self.offset_x
                    self.rect.y = mouse_y + self.offset_y

        def check_collision_with_ans(self):
            if self.rect.colliderect(pygame.Rect(SOL_BOX_X, SOL_BOX_Y, 100, 50)):
                return True
            return False

        def is_ans(self):
            if self.sol:
                return True
            return False

    next_question_button = Button(grey, WIDTH - 200, HEIGHT - 60, 160, 40, 'Next Question')

    def create_draggable_items():
        answer = answers[current_question_index]
        current_options = get_current_options()

        if current_options[0].strip().endswith('.'):
            current_options = current_options[1:]

        item_width = 100  # Adjust the width as needed to fit the text
        total_width = (len(current_options) - 1) * ANSWER_ITEM_SPACING + len(current_options) * item_width
        start_x = (WIDTH - total_width) // 2  # Center the options
        drag_items = []
        for i, text in enumerate(current_options):
            if text == answer:
                drag_items.append(
                    DraggableItem(text, start_x + i * (item_width + ANSWER_ITEM_SPACING), ANSWER_BANK_Y, item_width, 50,
                                smallfont, True))
            else:
                drag_items.append(
                    DraggableItem(text, start_x + i * (item_width + ANSWER_ITEM_SPACING), ANSWER_BANK_Y, item_width, 50,
                                smallfont, False))
        return drag_items


    # Initial display setup
    question_description_text = get_question_text()
    question_number_text = get_question_number_text()
    items = create_draggable_items()

    blanks = [
        pygame.Rect(LEFT_MARGIN, BLANKS_Y, BLANK_WIDTH, BLANK_HEIGHT),
        # Add more Rects for blanks if needed
    ]



    def modemenu():
        path = 'modemenu.py'
        subprocess.run([sys.executable, path])
        pygame.quit()

    run = True
    timer = 500
    while run:

        answer = answers[current_question_index]

        time_msg = font.render("Times UP", True, red)

        score_str = str(player_score)
        timer_str = str(timer/50)
        num_ans_str = str(num_correct)
        score_text = smallfont.render(score_str, True, black)
        timer_text = smallfont.render(timer_str, True, black)
        round_score = smallfont.render("Round Score:", True, black)
        tot_round_score = smallfont.render("Total Round Score:", True, black)
        tot_correct_ans = smallfont.render("Total Questions Answered:", True, black)
        num_ans = smallfont.render(num_ans_str, True, black)
        time_rmn = smallfont.render("Time Remaining:", True, black)
        font = pygame.font.SysFont('Arial', 35)
        text = font.render("ESC to quit", True, black)
        WIN.blit(BG, (0, 0))
        text_width = text.get_width()
        WIN.blit(text, (WIDTH - text_width - 10, 10))
        WIN.blit(question_number_text, (LEFT_MARGIN, TOP_MARGIN))
        WIN.blit(question_description_text, ((WIDTH - BLANK_WIDTH) // 2 , (HEIGHT - BLANK_HEIGHT) // 2 - 50))
        WIN.blit(time_rmn, (750, 50))
        WIN.blit(timer_text, (950, 50))
        WIN.blit(round_score, (750, 100))
        WIN.blit(score_text, (950, 100))
        #next_question_button.draw(WIN, black)



        if timer == 0:
            WIN.blit(time_msg, ((WIDTH - 200) / 2, ((HEIGHT - 100) / 2) - 200))
            WIN.blit(time_msg, ((WIDTH - 200) / 2, ((HEIGHT - 100) / 2) - 200))
            WIN.blit(tot_round_score, (((WIDTH - 200) / 2) - 25, ((HEIGHT - 150) / 2) - 100))
            WIN.blit(score_text, (((WIDTH - 200) / 2) + 150, (((HEIGHT - 150) / 2) - 100)))
            WIN.blit(tot_correct_ans, (((WIDTH - 250) / 2) - 65, ((HEIGHT - 150) / 2) - 50))
            WIN.blit(num_ans, (((WIDTH - 200) / 2) + 150, (((HEIGHT - 150) / 2) - 50)))
            update = False
            with open('scores.txt', 'r') as f:
                lines = f.read().split('\n')
                print(lines)
                length = len(lines)
                for i in range(length):
                    if lines[i] == username:
                        print(int(lines[i + 1]))
                        if int(lines[i + 1]) < player_score:
                            lines[i + 1] = player_score
                            update = True
                if username not in lines:
                    lines.append(username)
                    lines.append(player_score)
                    update = True
            if update:
                print(lines)
                with open('scores.txt', 'w') as f:
                    for i in range(len(lines)):
                        f.write(str(lines[i]))
                        f.write("\n")
            run = False



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            for item in items:
                item.handle_event(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    if item.check_collision_with_ans() and item.is_ans():
                        num_correct = num_correct + 1
                        current_question_index = (current_question_index + 1) % len(questions)
                        question_description_text = get_question_text()
                        question_number_text = get_question_number_text()
                        items = create_draggable_items()
                        player_score = player_score + difficulties[current_question_index]
                        timer = 500

            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_question_button.is_over(pygame.mouse.get_pos()):
                    current_question_index = (current_question_index + 1) % len(questions)
                    question_description_text = get_question_text()
                    question_number_text = get_question_number_text()
                    items = create_draggable_items()
                    timer = 500
            elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        modemenu()
                        break
        timer = timer - 1



        for item in items:
            item.draw(WIN)

        for blank in blanks:
            pygame.draw.rect(WIN, (0, 0, 0), (SOL_BOX_X, SOL_BOX_Y, 100, 50), 2)  # Draw a rectangle with an outline

        pygame.display.update()
        clock.tick(60)
    time.sleep(3)
    modemenu()
    sys.exit()
if __name__ == '__main__':
    main()