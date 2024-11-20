import pygame
import numpy as np
import sys
import random


# Game Setup and Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS


# AI difficulty settings
LEVELS = {
    "Easy": {"epsilon": 0.2, "depth": 2},
    "Medium": {"epsilon": 0.1, "depth": 4},
    "Hard": {"epsilon": 0.05, "depth": 6},
}

# Piece Types constants
EMPTY, HUMAN1, HUMAN2, KING1, KING2 = 0, 1, 2, 3, 4

# Colors
BROWN = (139, 100, 19)
RED = (255, 0, 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (135, 206, 235)
HIGHLIGHT_COLOR = (255, 165, 0)  
SELECTED_COLOR = (0, 0, 139) 
DOT_COLOR = (0, 0, 139)  

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Game")
FONT = FONT = pygame.font.SysFont("Comic Sans MS", 30)


def draw_text(text, color, x, y):
    label = FONT.render(text, True, color)
    WIN.blit(label, (x, y))
    pygame.display.update()

def draw_button(text, color, rect):
    pygame.draw.rect(WIN, color, rect)
    label = FONT.render(text, True, BLACK)
    WIN.blit(label, (rect[0] + 20, rect[1] + 10))
    pygame.display.update()

def draw_piece(piece, row, col):
    color = RED if piece in [HUMAN1, KING1] else BLACK  
    radius = SQUARE_SIZE // 3
    center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
    
    pygame.draw.circle(WIN, color, center, radius)
    
    # Draw a hollow ring for Kings
    if piece in [KING1, KING2]:
        pygame.draw.circle(WIN, WHITE, center, radius // 2, 5) 

def start_screen():
    WIN.fill(LIGHT_BLUE)
    draw_text("Welcome to Checkers!", BLACK, WIDTH // 2 - 200, HEIGHT // 4)
    human_button = pygame.Rect(WIDTH // 4, HEIGHT // 2, 300, 50)
    ai_button = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, 300, 50)
    draw_button("Human vs Human", YELLOW, human_button)
    draw_button("Human vs AI", YELLOW, ai_button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if human_button.collidepoint(event.pos):
                    return "Human vs Human"
                if ai_button.collidepoint(event.pos):
                    return "Human vs AI"
        pygame.display.update()

def get_level_settings(level):
    """Returns epsilon and depth based on the selected level."""
    settings = LEVELS.get(level, LEVELS["Medium"])
    # Explicitly convert depth to an integer
    settings["depth"] = int(settings["depth"])
    return settings["epsilon"], settings["depth"]

def get_level_screen():
    WIN.fill(LIGHT_BLUE)
    draw_text("Select Difficulty Level", BLACK, WIDTH // 2 - 200, HEIGHT // 4)
    easy_button = pygame.Rect(WIDTH // 4, HEIGHT // 2, 300, 50)
    medium_button = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 60, 300, 50)
    hard_button = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 120, 300, 50)
    
    draw_button("Easy", YELLOW, easy_button)
    draw_button("Medium", YELLOW, medium_button)
    draw_button("Hard", YELLOW, hard_button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    return "Easy"
                if medium_button.collidepoint(event.pos):
                    return "Medium"
                if hard_button.collidepoint(event.pos):
                    return "Hard"

        pygame.display.update()

# Creates initial board with pieces in starting positions
def create_board():
    board = np.zeros((ROWS, COLS), dtype=int)
    # Place HUMAN2 pieces in top 3 rows
    for row in range(3):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                board[row, col] = HUMAN2
    # Place HUMAN1 pieces in bottom 3 rows
    for row in range(5, ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                board[row, col] = HUMAN1
    return board

# Draws the game board with all visual elements
def draw_board(board, last_move=None, valid_moves=[], selected_piece=None):
    WIN.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            # Draw checkerboard pattern
            color = BROWN if (row + col) % 2 == 1 else WHITE
            pygame.draw.rect(WIN, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Highlight the last move
            if last_move and (row, col) in last_move:
                pygame.draw.rect(WIN, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Draw the piece
            piece = board[row, col]
            if piece != EMPTY:
                draw_piece(piece, row, col)

            # Draw valid move dots (including jump dots)
            if (row, col) in valid_moves:
                pygame.draw.circle(WIN, DOT_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 8)

            # Highlight the selected piece
            if selected_piece == (row, col):
                pygame.draw.rect(WIN, SELECTED_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    pygame.display.update()


def get_possible_moves(board, row, col):
    # Gets all possible moves for a piece at given position
    simple_moves = []
    jump_moves = []
    piece = board[row, col]
    if piece == EMPTY:
        return [], []

    # Directions for normal and king pieces
    if piece in [HUMAN1]:  
        directions = [(-1, -1), (-1, 1)]
    elif piece in [HUMAN2]:  
        directions = [(1, -1), (1, 1)]
    elif piece in [KING1, KING2]:  
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    else:
        directions = []  

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            if board[new_row, new_col] == EMPTY:
                # Add to simple moves
                simple_moves.append((new_row, new_col))
            elif board[new_row, new_col] != piece and board[new_row, new_col] != EMPTY:
                # Check if the piece being jumped over belongs to the opponent
                if (piece == HUMAN1 and (board[new_row, new_col] == HUMAN2 or board[new_row, new_col] == KING2)) or \
                (piece == HUMAN2 and (board[new_row, new_col] == HUMAN1 or board[new_row, new_col] == KING1)) or \
                (piece == KING1 and (board[new_row, new_col] == HUMAN2 or board[new_row, new_col] == KING2)) or \
                (piece == KING2 and (board[new_row, new_col] == HUMAN1 or board[new_row, new_col] == KING1)):
                    # Check for jump move
                    jump_row, jump_col = new_row + dr, new_col + dc
                    if 0 <= jump_row < ROWS and 0 <= jump_col < COLS and board[jump_row, jump_col] == EMPTY:
                        jump_moves.append((jump_row, jump_col))

    return simple_moves, jump_moves


def get_all_valid_moves(board, player):
    all_simple_moves = []
    all_jump_moves = []

    for row in range(ROWS):
        for col in range(COLS):
            if board[row, col] == player or board[row, col] == player + 2:  
                simple_moves, jump_moves = get_possible_moves(board, row, col)
                for move in simple_moves:
                    all_simple_moves.append((row, col, move[0], move[1]))
                for move in jump_moves:
                    all_jump_moves.append((row, col, move[0], move[1]))

    return all_simple_moves, all_jump_moves


def apply_move(board, row, col, new_row, new_col):
    piece = board[row, col]
    board[new_row, new_col] = piece
    board[row, col] = EMPTY

    # Remove the opponent's piece if jumping
    if abs(new_row - row) > 1:  # Jump move
        mid_row, mid_col = (row + new_row) // 2, (col + new_col) // 2
        board[mid_row, mid_col] = EMPTY

    # Promote to King if it reaches the opponent's back row
    if new_row == 0 and piece == HUMAN1:
        board[new_row, new_col] = KING1
    elif new_row == ROWS - 1 and piece == HUMAN2:
        board[new_row, new_col] = KING2

    return [(row, col), (new_row, new_col)]

def evaluate_board(board):
    score = 0
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row, col]
            if piece == HUMAN2:  # AI's normal pieces
                score += 1
            elif piece == KING2:  # AI's kings
                score += 3
            elif piece == HUMAN1:  # Human's normal pieces
                score -= 1
            elif piece == KING1:  # Human's kings
                score -= 3
    return score

def minimax(board, depth, maximizing_player, alpha, beta, epsilon=0):
    # Base case: reached max depth
    if depth == 0:
        return evaluate_board(board), None

    valid_moves, jump_moves = get_all_valid_moves(board, HUMAN2 if maximizing_player else HUMAN1)
    all_moves = jump_moves if jump_moves else valid_moves

    if not all_moves:  # No moves available
        return evaluate_board(board), None

    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        random.shuffle(all_moves)  # Introduce randomness based on epsilon
        for move in all_moves:
            # Try move and get evaluation
            temp_board = board.copy()
            apply_move(temp_board, move[0], move[1], move[2], move[3])
            eval, _ = minimax(temp_board, depth - 1, False, alpha, beta, epsilon)
            # Update best move if better
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

            # Epsilon introduces randomness in decision-making at each level
            if random.random() < epsilon:
                best_move = random.choice(all_moves)  # Add randomness
                break

        return max_eval, best_move
    else:
        min_eval = float('inf')
        random.shuffle(all_moves)  # Introduce randomness based on epsilon
        for move in all_moves:
            temp_board = board.copy()
            apply_move(temp_board, move[0], move[1], move[2], move[3])
            eval, _ = minimax(temp_board, depth - 1, True, alpha, beta, epsilon)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break

            # Epsilon introduces randomness in decision-making at each level
            if random.random() < epsilon:
                best_move = random.choice(all_moves)  # Add randomness
                break

        return min_eval, best_move

def ai_make_move(board, level="Medium"):
    epsilon, depth = get_level_settings(level)  # Get settings based on the selected level
    _, best_move = minimax(board, depth, True, float('-inf'), float('inf'), epsilon)
    if best_move:
        return apply_move(board, best_move[0], best_move[1], best_move[2], best_move[3])
    return None

# Function to ask the user if they want to continue jumping
def ask_user_continue_jump():
    font = pygame.font.SysFont('Comic Sans MS', 24)  # Font for the text
    screen = pygame.display.get_surface()  # Get the current screen
    clock = pygame.time.Clock()  # For controlling the frame rate

    # Set up the dialog box
    box_width, box_height = 300, 150
    box_x = (screen.get_width() - box_width) // 2
    box_y = (screen.get_height() - box_height) // 2
    button_width, button_height = 100, 40

    # Colors for the dialog box
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    # Text to display on the dialog box
    text_continue = font.render('Continue jumping?', True, BLACK)
    text_yes = font.render('Yes', True, WHITE)
    text_no = font.render('No', True, WHITE)

    # Create the dialog box and buttons
    dialog_box = pygame.Surface((box_width, box_height))
    dialog_box.fill(WHITE)
    pygame.draw.rect(dialog_box, BLACK, (0, 0, box_width, box_height), 3)

    # Button positions
    yes_button = pygame.Rect(box_x + 40, box_y + 80, button_width, button_height)
    no_button = pygame.Rect(box_x + 160, box_y + 80, button_width, button_height)

    # Main loop for the prompt
    while True:
        screen.fill(LIGHT_BLUE)  # Clear the screen
        screen.blit(dialog_box, (box_x, box_y))  # Draw the dialog box
        screen.blit(text_continue, (box_x + (box_width - text_continue.get_width()) // 2, box_y + 20))  # Display the question
        pygame.draw.rect(screen, BLUE, yes_button)  # Draw the 'Yes' button
        pygame.draw.rect(screen, RED, no_button)   # Draw the 'No' button
        screen.blit(text_yes, (yes_button.x + (button_width - text_yes.get_width()) // 2, yes_button.y + (button_height - text_yes.get_height()) // 2))
        screen.blit(text_no, (no_button.x + (button_width - text_no.get_width()) // 2, no_button.y + (button_height - text_no.get_height()) // 2))

        pygame.display.update()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # If the user quits, return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return True  # User clicks 'Yes'
                elif no_button.collidepoint(event.pos):
                    return False  # User clicks 'No'

        clock.tick(30)  # Limit the frame rate to 30 FPS

def show_winner(winner):
    WIN.fill(BLACK)
    draw_text(f"{winner} Wins!", YELLOW, WIDTH // 2 - 120, HEIGHT // 2 - 40)
    pygame.display.update()
    pygame.time.delay(3000)


def show_final_board(board, last_move):
    draw_board(board, last_move)
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    # Initialize game
    mode = start_screen()
    if mode == "Human vs AI":
        level = get_level_screen()
    board = create_board()
    draw_board(board)

    # Game State Variables
    player = HUMAN1
    selected_piece = None
    valid_moves = []
    last_move = None
    jumping = False 

    # Game loop
    while True:
        draw_board(board, last_move, valid_moves, selected_piece)

        # Handle events (clicks, quits)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE

                if selected_piece:
                    # If a valid move is clicked, make the move
                    if (row, col) in valid_moves:
                        last_move = apply_move(board, selected_piece[0], selected_piece[1], row, col)
                        # Check if the recent move is a jump move
                        if abs(row - selected_piece[0]) == 2 and abs(col - selected_piece[1]) == 2:  # Jump move check
                            simple_moves, jump_moves = get_possible_moves(board, row, col)
                            if jump_moves:
                                # Ask the user if they want to perform another jump
                                if ask_user_continue_jump():
                                    selected_piece = (row, col)
                                    valid_moves = jump_moves  # Only allow further jumps
                                    jumping = True  # Set jumping flag to True
                                    continue
                        selected_piece = None
                        valid_moves = []
                        jumping = False
                        player = HUMAN2 if player == HUMAN1 else HUMAN1
                    else:
                        if not jumping:
                            selected_piece = None
                            valid_moves = []

                elif board[row, col] == player or board[row, col] == player + 2:
                    # If a piece is selected, fetch its valid moves
                    selected_piece = (row, col)
                    simple_moves, jump_moves = get_possible_moves(board, row, col)
                    valid_moves = simple_moves + jump_moves  # Combine both types of moves

        # Check if any player has no moves left
        if not get_all_valid_moves(board, HUMAN1)[0] and not get_all_valid_moves(board, HUMAN1)[1]:
            winner = "Player 2"
            show_winner(winner)
            break
        if not get_all_valid_moves(board, HUMAN2)[0] and not get_all_valid_moves(board, HUMAN2)[1]:
            winner = "Player 1"
            show_winner(winner)
            break

        # If playing against AI, make the AI move
        if mode == "Human vs AI" and player == HUMAN2:
            last_move = ai_make_move(board, level)
            if last_move:  # Ensure AI made a move
                player = HUMAN1

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()