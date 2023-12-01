import pygame
import logging
import pyautogui

from board import Board
from const import WIDTH
from const import HEIGHT
from const import CROSS_COLOUR
from const import CIRCLE_COLOUR
from const import BG_COLOUR

class Game:

    def __init__(self, ultimate=False, max=False, singlePlayer=False):
        self.ultimate = ultimate
        self.max = max
        self.singlePlayer = singlePlayer
        self.board = Board(ultimate=ultimate, max=max)
        self.player = 1
        self.playing = True
        self.nextCell = [-1,-1]
        pygame.font.init()

    def play_game(self, screen):
        pygame.display.set_caption('ULTIMATE TIC TAC TWIST')
        
        self.board.render(screen)
        logging.info('Starting in game loop')
        while True:
            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN and self.playing:
                    xclick, yclick = event.pos

                    if self.board.valid_sqr(xclick, yclick, self.nextCell, self.max):
                        self.nextCell = self.board.mark_sqr(xclick, yclick, self.player, self.nextCell)
                        logging.info('nextCell = %s',self.nextCell)
                        self.board.draw_fig(screen, xclick, yclick)

                        self.nextCellRow = self.nextCell[0]
                        self.nextCellCol = self.nextCell[1]
                        if self.board.next_board_full(xclick, yclick, self.nextCell, self.ultimate, self.max):
                            self.nextCell = [-1,-1] 
                        
                        # ultimate winner ?
                        winner = self.board.check_draw_win(screen)
                        if winner:
                            self.board.manage_win(screen, winner, onmain=True)
                            self.ultimate_winner(screen, winner)

                        self.next_turn()
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
                        self.nextCell = [-1,-1]
                    if event.key == pygame.K_ESCAPE:
                        logging.info('Returning to Main menu')
                        screen.fill(BG_COLOUR)
                        return
                # quit
                if event.type == pygame.QUIT:
                    logging.info('Quitting to Menu')
                    screen.fill(BG_COLOUR)
                    return
            pygame.display.update()

    def next_turn(self):
        self.player = 2 if self.player == 1 else 1

    def ultimate_winner(self, surface, winner):
        print('ULTIMATE WINNER! ->', winner)

        if winner == 1:
            # color = CROSS_COLOUR
            # desc
            iDesc = (WIDTH // 2 - 110, HEIGHT // 2 - 110)
            fDesc = (WIDTH // 2 + 110, HEIGHT // 2 + 110)
            # asc
            iAsc = (WIDTH // 2 - 110, HEIGHT // 2 + 110)
            fAsc = (WIDTH // 2 + 110, HEIGHT // 2 - 110)
            # draw
            pygame.draw.line(surface, BG_COLOUR, iDesc, fDesc, 22)
            pygame.draw.line(surface, BG_COLOUR, iAsc, fAsc, 22)

        else:
            # color = CIRCLE_COLOUR
            # center
            center = (WIDTH // 2, HEIGHT // 2   )
            pygame.draw.circle(surface, BG_COLOUR, center, WIDTH // 4, 22)
        
        font = pygame.font.SysFont('monospace', 64)
        lbl = font.render('WINNER!', 1, BG_COLOUR)
        surface.blit(lbl, (WIDTH // 2 - lbl.get_rect().width // 2, HEIGHT // 2 + 220))

        self.playing = False
    
    def restart(self):
        self.__init__(self.ultimate, self.max)