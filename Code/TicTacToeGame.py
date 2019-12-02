#%% md
###  **<h1><center>Tic Tac Toe Game</center></h1>**
#%% md
### Libraries

Pygame is a Free and Open Source python programming language library for making multimedia applications like games. In this project, pygame is used for GUI implementation of Tic Tac Toe game.

#%%
# Python library used for GUI

import pygame
from pygame.locals import *
#%% md
### Game Board Features

This is to create the constants for the features of the game board. It includes features like width, height, color, font size, etc.
#%%
# Create the features of the game board

Board_width = 3  # number of columns in the board
Board_height = 3 # number of rows in the board
Tile_size = 100
Window_width = 480
Window_height = 480
FPS = 30  # Frames per second
Blank = None

# Color of the game board

#                  R    G    B
Black =          (  0,   0,   0)
White =          (255, 255, 255)
Green =          (  0,  204,  0)
Dark_turquoise = (  3,  54,  73)
Magenta =        (  255, 0, 255)

Background_color = Dark_turquoise
Tile_color = Magenta
Text_color = White
Border_color = Green
Font_size = 20

Button_color = White
Button_text_color = Black
Message_color = White
#%%
Blank = 10
Player_O = 11
Player_X = 21


Player_O_win = Player_O * 3
Player_X_win = Player_X * 3

Continue_Game  = 10
Draw_Game      = 20
Quit_Game      = 30

X_margin = int((Window_width - (Tile_size * Board_width + (Board_width - 1))) / 2)
Y_margin = int((Window_height - (Tile_size * Board_height + (Board_height - 1))) / 2)

choice = 0
#%% md
### Winning Cases

This function is used to check possible winning cases. A player can win the Tic Tac Toe game if he/she gets all their marks in either horizontal, vertical or diagonal of the game board. Otherwise, the game will be considered as a draw game.
#%%
# Check possiblities of winning in the game

def Check_Winner(board):
    def Check_Draw():
        return sum(board)%10 == 9

    def check_horizontal(player):   # Horizontal Win
        for i in [0, 3, 6]:
            if sum(board[i:i+3]) == 3 * player:
                return player

    def check_vertical(player):   # Vertical Win
        for i in range(3):
            if sum(board[i::3]) == 3 * player:
                return player

    def check_diagonals(player):   # Main Diagonal Win
        if (sum(board[0::4]) == 3 * player) or (sum(board[2:7:2]) == 3 * player):
            return player

    for player in [Player_X, Player_O]:
        if any([check_horizontal(player), check_vertical(player), check_diagonals(player)]):
            return player

    return Draw_Game if Check_Draw() else Continue_Game
#%%
def unit_score(winner, depth):
    if winner == Draw_Game:
        return 0
    else:
        return 10 - depth if winner == Player_X else depth - 10
#%%
# Get available moves on the game board

def get_available_move(board):
    return [i for i in range(9) if board[i] == Blank]
#%% md
### Minimax Algorithm

Minimax is a artificial intelligence algorithm applied in two player Tic Tac Toe game. It is used for decision making. 

The algorithm search, recursively for the best move that leads the Max player to win or not lose (draw). It consider the current state of the game and the available moves at that state, then for each valid move it plays (alternating min and max) until it finds a terminal state (win, draw or lose).
#%%
# Minimax Algorithm used for this game

def minimax(board, depth):
    global choice
    result = Check_Winner(board)
    if result != Continue_Game:
        return unit_score(result, depth)

    depth += 1  # index of the node in the game tree
    scores = []   # an array of scores
    steps = []   # an array of moves(steps)

    for step in get_available_move(board):
        score = minimax(update_state(board, step, depth), depth)
        scores.append(score)
        steps.append(step)

    if depth % 2 == 1:
        max_value_index = scores.index(max(scores))
        choice = steps[max_value_index]
        return max(scores)
    else:
        min_value_index = scores.index(min(scores))
        choice = steps[min_value_index]
        return min(scores)
#%% md
We should update the variables of the game state and get the new updated state. After updating game states, we need to update the actual board data structure 
#%%
def update_state(board, step, depth):   
    board = list(board)
    board[step] = Player_X if depth % 2 else Player_O
    return board

def update_board(board, step, player):
    board[step] = player
#%%
# Assigining X and O to both the players by checking which player is playing

def change_to_player(player):
    if player == Player_O:
        return 'O'
    elif player == Player_X:
        return 'X'
    elif player == Blank:
        return '-'
#%% md
### Draw the game board

The function Draw_Board handles drawing the entire board and all of its tiles to the displaySurf display Surface object. The fill() method completely paints over anything that used to be drawn on the display Surface object before so that we start from scratch.
Then the code handles drawing the message at the top of the window. We use this to display the text at the top of the window.

Next, nested for loops are used to draw each tile to the display Surface object by calling the drawTile() function.

The code then draw a border around the tiles. The top left corner of the boarder will be 5 pixels to the left and 5 pixels above the top left corner of the tile at board coordinates (0, 0). The width and height of the border are calculated from the number of tiles wide and high the board is (stored in the Board_width and Board_height constants) multiplied by the size of the tiles (stored in the Tile_size constant).

The rectangle we draw will have a thickness of 4 pixels, so we will move the boarder 5 pixels to the left and above where the top and left variables point so the thickness of the line won’t overlap the tiles. We will also add 11 to the width and length (5 of those 11 pixels are to compensate for moving the rectangle to the left and up).

Finally, we draw the buttons off to the slide of the screen. The text and position of these buttons never changes, which is why they were stored in constant variables at the beginning of the main() function.


#%%
# Drawing the game board using defined features

def Draw_Board(board, message):
    displaySurf.fill(Background_color)
    if message:
        textSurf, textRect = makeText(message, Message_color, Background_color, 5, 5)
        displaySurf.blit(textSurf, textRect)

    for tile_x in range(3):
        for tile_y in range(3):
            if board[tile_x*3+tile_y] != Blank:
                drawTile(tile_x, tile_y, board[tile_x*3+tile_y])

    left, top = get_Left_Top_Of_Tile(0, 0)
    width = Board_width * Tile_size
    height = Board_height * Tile_size
    pygame.draw.rect(displaySurf, Border_color, (left - 5, top - 5, width + 11, height + 11), 4)

    displaySurf.blit(New_surf, New_rect)
    displaySurf.blit(New_surf2, New_rect2)
#%% md
### Convet Board Coordinates to Pixel Coordinates

For the board XY coordinates that are passed in, the function get_Left_Top_Of_Tile() calculates and returns the pixel XY coordinates of the pixel at the top left of that board space.
#%%
# Converting board coordinates to pixel coordinates

def get_Left_Top_Of_Tile(tile_X, tile_Y):
    left = X_margin + (tile_X * Tile_size) + (tile_X - 1)
    top = Y_margin + (tile_Y * Tile_size) + (tile_Y - 1)
    return (left, top)
#%% md
### Make Text Appear on the Screen

The makeText() function handles creating the Surface and Rect objects for positioning text on the screen.
Instead of doing all these calls each time we want to make text on the screen, we can just call makeText() instead. 
This saves us on the amount of typing we have to do for our program. (Though drawTile() makes the calls to render() and get_rect() itself because it positions the text Surface object by the center point rather than the topleft point and uses a transparent background color.) 

#%%
# Making Text Appear on the Screen

def makeText(text, color, bgcolor, top, left):
    textSurf = Basic_font.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)
#%% md
### Draw a Tile

The drawTile() function will draw a single numbered tile on the board. 

The tile_x and tile_y parameters are the board coordinates of the tile.
The adj_x and adj_y keyword parameters are for making minor adjustments to the position of the tile.

The Pygame drawing functions only use pixel coordinates, so first it converts the board coordinates in tile_x and tile_y to pixel coordinates, which we will be stored in variables left and top (since get_Left_Top_Of_Tile() returns the top left corner’s coordinates). 

We draw the background square of the tile with a call to pygame.draw.rect() while adding the adj_x and adj_y values to left and top in case the code needs to adjust the position of the tile.

Then the Surface object is created that has the number text drawn on it. A Rect object for the Surface object is positioned, and then used to blit the Surface object to the display Surface.

The drawTile() function does not call pygame.display.update() function, since the caller of drawTile() probably will want to draw more tiles for the rest of the board before making them appear on the screen.

#%%
# Draw a tile at board coordinates.

def drawTile(tile_x, tile_y, symbol, adj_x=0, adj_y=0):
    left, top = get_Left_Top_Of_Tile(tile_x, tile_y)
    pygame.draw.rect(displaySurf, Tile_color, (left + adj_x, top + adj_y, Tile_size, Tile_size))
    textSurf = Basic_font.render(symbol_to_str(symbol), True, Text_color)
    textRect = textSurf.get_rect()
    textRect.center = left + int(Tile_size / 2) + adj_x, top + int(Tile_size / 2) + adj_y
    displaySurf.blit(textSurf, textRect)
#%%
def symbol_to_str(symbol):
    if symbol == Player_O:
        return 'O'
    elif symbol == Player_X:
        return 'X'
#%% md
### Convert Pixel coordinates to Board coordinates

If the pixel coordinates that were passed in are within that space on the board, it returns those board coordinates. 
Since all of the tiles have a width and height that is set in the Tile_size constant, we can create a Rect object that represents the space on the board by getting the pixel coordinates of the top left corner of the board space, and then use the collidepoint() Rect method to see if the pixel coordinates are inside that Rect object’s area.

If the pixel coordinates that were passed in were not over any board space, then the value None is returned.
#%%
# Converting from Pixel Coordinates to Board Coordinates

def get_spot_clicked(x, y):
    for tile_X in range(3):
        for tile_Y in range(3):
            left, top = get_Left_Top_Of_Tile(tile_X, tile_Y)
            tileRect = pygame.Rect(left, top, Tile_size, Tile_size)
            if tileRect.collidepoint(x, y):
                return (tile_X, tile_Y)
    return None
#%%
def board_to_step(spot_x, spot_y):
    return spot_x * 3 + spot_y
#%%
def check_valid_move(coords, board):
    step = board_to_step(*coords)
    return board[step] == Blank
#%% md
### main() function 

main() function will handle creating the window, clock object, and font object.
#%%
# Diplaying the final game

def main():
    global FPS_clock, displaySurf, Basic_font, New_surf, New_rect, New_surf2, New_rect2
    two_player = False #by default false
    pygame.init()
    FPS_clock = pygame.time.Clock()
    displaySurf = pygame.display.set_mode((Window_width, Window_height))
    pygame.display.set_caption('Tic Tac Toe')
    Basic_font = pygame.font.Font('freesansbold.ttf', Font_size)
    New_surf, New_rect = makeText('vs AI', Text_color, Tile_color, Window_width - 120, Window_height - 60)
    New_surf2, New_rect2 = makeText('vs Human', Text_color, Tile_color, Window_width - 240, Window_height - 60)
    board = [Blank] * 9
    game_over = False
    x_turn = True
    msg = "Welcome to this game"   # Contains the message to show in the upper left corner.
    Draw_Board(board, msg)
    pygame.display.update()   # pygame.display.update() is called to draw the display Surface object on the actual computer screen

    while True:
        coords = None
        for event in pygame.event.get():   # event handling loop
            if event.type == MOUSEBUTTONUP:   # If the type of event was a MOUSEBUTTONUP event (that is, the player had released a mouse button somewhere over the window), then we pass the mouse coordinates to our getSpotClicked() function which will return the board coordinates of the spot on the board the mouse release happened. The event.pos[0] is the X coordinate and event.pos[1] is the Y coordinate.
                coords = get_spot_clicked(event.pos[0], event.pos[1])
                if not coords and New_rect.collidepoint(event.pos):
                    board = [Blank] * 9
                    game_over = False
                    msg = "Welcome to this game"
                    Draw_Board(board, msg)
                    pygame.display.update()
                    two_player = False
                if not coords and New_rect2.collidepoint(event.pos):
                    board = [Blank] * 9
                    game_over = False
                    msg = "Welcome to this game"
                    Draw_Board(board, msg)
                    pygame.display.update()
                    two_player = True
        if coords and check_valid_move(coords, board) and not game_over:
            if two_player:
                next_step = board_to_step(*coords)
                if x_turn:
                    update_board(board, next_step, Player_X)
                    x_turn = False
                else:
                    update_board(board, next_step, Player_O)
                    x_turn = True
                Draw_Board(board, msg)
                pygame.display.update()

            if not two_player:
                next_step = board_to_step(*coords)
                update_board(board, next_step, Player_X)
                Draw_Board(board, msg)
                pygame.display.update()
                minimax(board, 0)
                update_board(board, choice, Player_O)

            result = Check_Winner(board)
            game_over = (result != Continue_Game)

            if result == Player_X:
                msg = "The winner of this game is X"
            elif result == Player_O:
                msg = "The winner of this game is O"
            elif result == Draw_Game:
                msg = "Draw Game"

            Draw_Board(board, msg)
            pygame.display.update()

#%% md
### Start the game
#%%
# Start playing the game by calling main() function

if __name__ == '__main__':
    main()
#%%
if __name__ == '__main__':
    main()
#%%
