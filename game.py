import logging
import pygame
import pyautogui
import random
import time

from board import Board
from const import BG_COLOUR
from const import HEIGHT
from const import WIDTH

class Game:

    def __init__(self, ultimate=False, max_mode=False, single_player=False):
        self.ultimate = ultimate
        self.max_mode = max_mode
        self.single_player = single_player
        self.board = Board(ultimate=ultimate, max_mode=max_mode)
        self.player = 1
        self.playing = True
        self.next_cell = [-1,-1]
        pygame.font.init()

    def play_game(self, screen):
        pygame.display.set_caption('TIC TAC TOE')
        
        self.board.render(screen)
        logging.info('Starting in game loop')
        self.board.highlight_valid_move(screen, self.next_cell, self.player)
        while True:
            if self.single_player and self.player == 2 and self.playing:
                self.handle_computer_move(screen)
            
            for event in pygame.event.get():

                # click on square
                if event.type == pygame.MOUSEBUTTONDOWN and self.playing:
                    xclick, yclick = event.pos

                    if self.board.valid_sqr(xclick, yclick, self.next_cell, self.max_mode):

                        self.handle_move(screen, xclick, yclick)

                    else:
                        logging.info('Invalid move!')
                        pyautogui.alert("Your move does not work as it is Invalid!")

                # keypress
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        logging.info('Restarting the game!')
                        self.restart()
                        screen.fill(BG_COLOUR)
                        self.board.render(screen)
                        self.set_free_move()
                        self.board.highlight_valid_move(screen, self.next_cell, self.player)
                    if event.key == pygame.K_ESCAPE:
                        self.return_to_main(screen)
                        return
                # quit
                if event.type == pygame.QUIT:
                    self.return_to_main(screen)
                    return
            pygame.display.update()

    # Marks correct square to draw, checks if the board state has won, set the next valid move to highlight
    def handle_move(self, screen, xclick, yclick):
        self.next_cell = self.board.mark_sqr(xclick, yclick, self.player, self.next_cell)
        logging.info('nextCell = %s',self.next_cell)
        self.board.draw_fig(screen, xclick, yclick)

        self.next_cell_row = self.next_cell[0]
        self.next_cell_col = self.next_cell[1]

        # winner ?
        winner = self.board.check_draw_win(screen)
        if winner:
            self.board.manage_win(screen, winner, onmain=True)
            self.ultimate_winner(screen, winner)

        if self.board.next_board_full(self.next_cell, self.ultimate):
            logging.info("Next board is full, setting free move")
            self.set_free_move()

        self.next_turn()
        
        if self.playing:
            self.board.highlight_valid_move(screen, self.next_cell, self.player)

    def next_turn(self):
        self.player = 2 if self.player == 1 else 1

    # Gets all valid moves, randomly pick one, find click pos and handle move
    def handle_computer_move(self, screen):
        logging.info("Handling CPU Turn")

        # Add CPU 'think' time
        time.sleep(random.random()+0.5)

        valid_moves = self.board.fetch_valid_moves(self.next_cell, self.ultimate, self.max_mode)

        logging.debug('valid moves -> ', valid_moves)

        grid_pos = valid_moves[len(valid_moves)-1]

        move_chosen = valid_moves[random.randint(0, len(valid_moves)-2)]
        
        multiplier = int(WIDTH / 3)
        if self.ultimate and not self.max_mode:
            multiplier = int(multiplier / 3)
        if self.max_mode:
            multiplier = int(multiplier / 9)

        if self.max_mode:
            xclick = grid_pos[0] + (move_chosen[0] * int((WIDTH / 9))) + (move_chosen[3] * multiplier) 
            yclick = grid_pos[1] + (move_chosen[1] * int((WIDTH / 9))) + (move_chosen[2] * multiplier) 
        else:
            xclick = grid_pos[0] + (move_chosen[1] * multiplier)
            yclick = grid_pos[1] + (move_chosen[0] * multiplier)

        logging.debug('Computer co-ordinates move chosen -> %s ', move_chosen)

        logging.debug('Calculating "click" position xclick/yclick -> [%s / %s]', xclick, yclick)

        self.handle_move(screen, xclick, yclick)


    def ultimate_winner(self, surface, winner):
        logging.info('WINNER! -> %s' , winner)

        # Cross winner
        if winner == 1:
            iDesc = (WIDTH // 2 - 110, HEIGHT // 2 - 110)
            fDesc = (WIDTH // 2 + 110, HEIGHT // 2 + 110)
            # asc
            iAsc = (WIDTH // 2 - 110, HEIGHT // 2 + 110)
            fAsc = (WIDTH // 2 + 110, HEIGHT // 2 - 110)
            # draw
            pygame.draw.line(surface, BG_COLOUR, iDesc, fDesc, 22)
            pygame.draw.line(surface, BG_COLOUR, iAsc, fAsc, 22)

        #Circle winner
        else:
            center = (WIDTH // 2, HEIGHT // 2   )
            pygame.draw.circle(surface, BG_COLOUR, center, WIDTH // 4, 22)
        
        font = pygame.font.SysFont('monospace', 64)
        lbl = font.render('WINNER!', 1, BG_COLOUR)
        surface.blit(lbl, (WIDTH // 2 - lbl.get_rect().width // 2, HEIGHT // 2 + 220))

        self.playing = False
    def set_free_move(self):
        self.next_cell = [-1,-1]
    def return_to_main(self, screen):
        logging.info('Returning to Main menu')
        screen.fill(BG_COLOUR)
    def restart(self):
        self.__init__(self.ultimate, self.max_mode)