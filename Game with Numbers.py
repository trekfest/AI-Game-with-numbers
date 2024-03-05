import time
import pygame
import random
import sys

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = (23, 135, 207)
BUTTON_COLOR = (76, 175, 80)
BUTTON_HOVER_COLOR = (102, 255, 102)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 20

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Number Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)
pygame.mixer.init()
user_sound = pygame.mixer.Sound("user_move.mp3")  
computer_sound = pygame.mixer.Sound("computer_move.mp3")  

def draw_text(surface, text, color, rect, font, aa=True, bkg=None):
    y = rect.top
    lineSpacing = -2
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
        image = font.render(text[:i], aa, color, bkg)
        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
        text = text[i:]
    return text

def input_number(screen, font, prompt):
    WHITE = (255, 255, 255)
    TEXT_COLOR = (0, 0, 0)  # Black text color
    string = ''
    input_rect = pygame.Rect(100, 200, 200, 50)  # Define the text box rectangle
    active = True  # Set active to True initially to show the cursor blinking
    cursor_visible = True
    cursor_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and string.isdigit() and 15 <= int(string) <= 25:
                        return int(string)
                    elif event.key == pygame.K_BACKSPACE:
                        string = string[:-1]
                    else:
                        if event.unicode.isdigit():
                            string += event.unicode

        screen.fill(BG_COLOR)
        draw_text(screen, prompt, TEXT_COLOR, pygame.Rect(100, 100, 600, 50), font)
        pygame.draw.rect(screen, TEXT_COLOR, input_rect, 2)  # Draw the text box border

        # Draw the white rectangle as the background of the input box
        pygame.draw.rect(screen, WHITE, (input_rect.x + 2, input_rect.y + 2, input_rect.width - 4, input_rect.height - 4))

        # Draw the text at the bottom of the box
        text_surface = font.render(string, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(bottomleft=(input_rect.x + 5, input_rect.bottom - 5))
        screen.blit(text_surface, text_rect)

        # Blinking cursor
        if active and pygame.time.get_ticks() - cursor_timer > 500:  # Blink cursor every 500 ms
            cursor_visible = not cursor_visible
            cursor_timer = pygame.time.get_ticks()
        if active and cursor_visible:
            cursor_pos = text_rect.right + 2
            pygame.draw.line(screen, TEXT_COLOR, (cursor_pos, text_rect.top), (cursor_pos, text_rect.bottom), 2)

        pygame.display.flip()
        clock.tick(30)










        
def display_start_menu(screen, font):
    def draw_menu_buttons():
        screen.fill(BG_COLOR)
        draw_text(screen, "Who starts?", TEXT_COLOR, pygame.Rect(100, 100, 600, 50), font)
        user_button.draw(screen)
        draw_text(screen, "Choose algorithm:", TEXT_COLOR, pygame.Rect(user_button.rect.left, user_button.rect.bottom + 40, user_button.rect.width, 50), font)

        for button in [computer_button, minimax_button, alphabeta_button]:
            button.draw(screen)
        pygame.display.flip()

    user_button = Button(100, 150, 200, 50, "User", lambda: "user")
    computer_button = Button(500, 150, 200, 50, "Computer", lambda: "computer")
    minimax_button = Button(100, 300, 200, 50, "Minimax", lambda: "minimax")
    alphabeta_button = Button(500, 300, 200, 50, "Alpha-Beta", lambda: "alphabeta")


    buttons = [user_button, computer_button, minimax_button, alphabeta_button]
    start_player = None
    algorithm_choice = None

    while start_player is None or algorithm_choice is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        if button in [user_button, computer_button]:
                            if start_player is not None:
                                for b in [user_button, computer_button]:
                                    b.selected = False
                            start_player = button.callback()
                            button.selected = True
                        elif button in [minimax_button, alphabeta_button]:
                            if algorithm_choice is not None:
                                for b in [minimax_button, alphabeta_button]:
                                    b.selected = False
                            algorithm_choice = button.callback()
                            button.selected = True

        for button in buttons:
            button.update(pygame.mouse.get_pos())
        draw_menu_buttons()

    return start_player, algorithm_choice


class Button:
    def __init__(self, x, y, w, h, text, callback, selected=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.hover = False
        self.selected = selected

    def draw(self, screen):
        if self.selected:
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, self.rect)
        elif self.hover:
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, self.rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, self.rect)
        draw_text(screen, self.text, TEXT_COLOR, self.rect, font)

    def update(self, pos):
        if not self.selected:
            self.hover = self.rect.collidepoint(pos)

def heuristic_value(node, current_player_score, opponent_score):
    # Calculate the sum of absolute differences between each number in the string and the opponent's score
    total_difference = sum(abs(num - opponent_score) for num in node)
    
    # Adjust the heuristic value based on the current player's score
    if current_player_score < opponent_score:
        return total_difference  # If current player is behind, prioritize reducing the difference
    elif current_player_score > opponent_score:
        return -total_difference  # If current player is ahead, prioritize increasing the difference for the opponent
    else:
        return 0  # If scores are equal, no preference
    


def get_children(node):
    # Placeholder function for generating child nodes
    children = []
    for i in range(len(node)):
        child = node.copy()
        child.pop(i)
        children.append(child)
    return children

def game_over(node):
    return len(node) == 0

def minimax(node, depth, maximizingPlayer, current_player_score, opponent_score):
    if depth == 0 or game_over(node):
        return heuristic_value(node, current_player_score, opponent_score)
    if maximizingPlayer:
        value = -float('inf')
        for child in get_children(node):
            value = max(value, minimax(child, depth - 1, False, current_player_score, opponent_score))
        return value
    else:
        value = float('inf')
        for child in get_children(node):
            value = min(value, minimax(child, depth - 1, True, current_player_score, opponent_score))
        return value

def alphabeta(node, depth, alpha, beta, maximizingPlayer, current_player_score, opponent_score):
    if depth == 0 or game_over(node):
        return heuristic_value(node, current_player_score, opponent_score)
    if maximizingPlayer:
        value = -float('inf')
        for child in get_children(node):
            value = max(value, alphabeta(child, depth - 1, alpha, beta, False, current_player_score, opponent_score))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for child in get_children(node):
            value = min(value, alphabeta(child, depth - 1, alpha, beta, True, current_player_score, opponent_score))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value



class Game:
    def __init__(self, string_length=20, start_player="user", algorithm="minimax"):
        self.string = [random.randint(1, 3) for _ in range(string_length)]
        screen_width = max(800, 60 * string_length + 40)
        screen_height = 600
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.human_score = 80
        self.computer_score = 80
        self.buttons = []
        self.start_player = start_player
        self.algorithm = algorithm
        self.current_player = start_player
        self.dragging = False
        self.dragged_value = None
        self.dragged_index = None
        self.computer_move_text = None
        self.nodes_visited = []
        self.total_move_time = 0.0
        self.drop_area = pygame.Rect(20, screen_height // 2 + 100, screen_width - 40, 100)
        self.update_buttons()
        if self.start_player == "computer":
            self.computer_move()

    def update_buttons(self):
        self.buttons.clear()
        for i, num in enumerate(self.string):
            button = Button(20 + 60*i, SCREEN_HEIGHT // 2, 50, 50, str(num), lambda idx=i: self.prepare_move(idx), selected=False)
            self.buttons.append(button)

    def prepare_move(self, index):
        if self.current_player == "user" and not self.dragging:
            self.dragging = True
            self.dragged_index = index
            self.dragged_value = self.string[index]

    
    def make_move(self, index):
        num = self.string.pop(index)
        if self.current_player == "user":
            self.human_score -= num
            self.current_player = "computer"
            user_sound.play()  # Play sound for user move
        else:
            self.computer_score -= num
            self.current_player = "user"
            computer_sound.play()  # Play sound for computer move

    # Smooth transition for the dragged item
        start_pos = self.buttons[index].rect.topleft
        end_pos = (self.drop_area.left + self.drop_area.width // 2 - 25, self.drop_area.top + self.drop_area.height // 2 - 25)
        delta_x = (end_pos[0] - start_pos[0]) / 30  # Divide by frames for smooth transition
        delta_y = (end_pos[1] - start_pos[1]) / 30
        for i in range(30):
            self.buttons[index].rect.x += delta_x
            self.buttons[index].rect.y += delta_y
            self.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)

        self.dragging = False
        self.dragged_value = None
        self.dragged_index = None
        self.update_buttons()
        if not self.string:  # Game ends
            self.show_winner()
            return
        if self.current_player == "computer":
            pygame.time.delay(500)  # Wait for 0.5 second to simulate computer thinking
            self.computer_move()

    def computer_move(self):
        start_time = time.time()  # Track start time
        # Calculate current player's score and opponent's score
        if self.current_player == "user":
            current_player_score = self.human_score
            opponent_score = self.computer_score
        else:
            current_player_score = self.computer_score
            opponent_score = self.human_score

        # Simulate computer's move. This is a placeholder for the actual logic
        if self.algorithm == "minimax":
            move, _ = self.minimax_decision(current_player_score, opponent_score)
        elif self.algorithm == "alphabeta":
            move, _ = self.alphabeta_decision(current_player_score, opponent_score)
        self.computer_move_text = f"Computer chose: {self.string[move]}"
        self.make_move(move)

    # Track nodes visited and time taken for the move
        end_time = time.time()
        self.nodes_visited.append(len(get_children(self.string)))
        self.total_move_time += end_time - start_time


        
    def minimax_decision(self, current_player_score, opponent_score):
        best_score = -float('inf')
        best_move = None
        for i, option in enumerate(get_children(self.string)):
            score = minimax(option, 3, False, current_player_score, opponent_score)  # Depth limited to 3 for simplicity
            if score > best_score:
                best_score = score
                best_move = i
        return best_move, best_score

    def alphabeta_decision(self, current_player_score, opponent_score):
        best_score = -float('inf')
        best_move = None
        for i, option in enumerate(get_children(self.string)):
            score = alphabeta(option, 3, -float('inf'), float('inf'), False, current_player_score, opponent_score)  # Depth limited to 3 for simplicity
            if score > best_score:
                best_score = score
                best_move = i
        return best_move, best_score

    def draw(self, screen):
        screen.fill(BG_COLOR)
        for button in self.buttons:
            button.draw(screen)
        pygame.draw.rect(screen, (200, 200, 200), self.drop_area)  # Drawing drop area
        draw_text(screen, "Drop here to remove", TEXT_COLOR, self.drop_area, font, aa=True, bkg=None)
        if self.dragging and self.dragged_value is not None:
            draw_text(screen, str(self.dragged_value), TEXT_COLOR, pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 50, 50), font)
        draw_text(screen, f"Human Score: {self.human_score}", TEXT_COLOR, pygame.Rect(20, 20, 200, 50), font)
        draw_text(screen, f"Computer Score: {self.computer_score}", TEXT_COLOR, pygame.Rect(20, 70, 200, 50), font)
        if self.computer_move_text:
            draw_text(screen, self.computer_move_text, TEXT_COLOR, pygame.Rect(20, 170, 200, 50), font)  
        current_player_text = "Current Player: " + ("User" if self.current_player == "user" else "Computer")
        draw_text(screen, current_player_text, TEXT_COLOR, pygame.Rect(20, 120, 200, 50), font)

    def run(self):
        running = True
        while running and self.string:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.rect.collidepoint(event.pos) and self.current_player == "user":
                            self.prepare_move(i)
                            break
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.dragging and self.drop_area.collidepoint(pos):
                        self.make_move(self.dragged_index)
                    self.dragging = False
                    self.dragged_value = None
                    self.dragged_index = None
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        # Update the dragged item's position based on the mouse movement
                        self.buttons[self.dragged_index].rect.x = pos[0] - 25
                        self.buttons[self.dragged_index].rect.y = pos[1] - 25

            self.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)
    
    def show_winner(self):
        # Calculate average time and total nodes visited
        avg_time = self.total_move_time / len(self.nodes_visited)
        total_nodes = sum(self.nodes_visited)

        winner = "Draw"
        if self.human_score > self.computer_score:
            winner = "Human wins!"
        elif self.computer_score > self.human_score:
            winner = "Computer wins!"

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            self.screen.fill(BG_COLOR)
            draw_text(self.screen, winner, TEXT_COLOR, pygame.Rect(100, 250, 600, 50), font)
            draw_text(self.screen, f"Human Score: {self.human_score}", TEXT_COLOR, pygame.Rect(100, 300, 600, 50), font)
            draw_text(self.screen, f"Computer Score: {self.computer_score}", TEXT_COLOR, pygame.Rect(100, 350, 600, 50), font)
            draw_text(self.screen, f"Average Time per Move: {avg_time:.4f} seconds", TEXT_COLOR, pygame.Rect(100, 400, 600, 50), font)
            draw_text(self.screen, f"Total Nodes Visited: {total_nodes}", TEXT_COLOR, pygame.Rect(100, 450, 600, 50), font)
            draw_text(self.screen, "Press R to Restart or Q to Quit", TEXT_COLOR, pygame.Rect(100, 500, 600, 50), font)
            pygame.display.flip()
            clock.tick(60)



def main():
    pygame.init()
    start_player, algorithm = display_start_menu(screen, font)  # Display the start menu and get user choices
    string_length = input_number(screen, font, "Enter string length (15-25):")  # Get the string length from the user
    game = Game(string_length, start_player, algorithm)  # Initialize the game with the chosen settings
    game.run()  # Start the game loop

if __name__ == "__main__":
    main()
