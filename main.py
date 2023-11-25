import pygame
import sys
import logging 

from const import WIDTH
from const import HEIGHT
from const import BG_COLOUR
from game import Game


class Main:

    def __init__(self): 
        
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BG_COLOUR)
        pygame.display.set_caption('ULTIMATE TIC TAC TWIST')
        self.game = Game(ultimate=True, max=False)
        self.nextCell = [-1,-1]

    def mainloop(self):

        screen = self.screen
        game = self.game

        self.screen.fill(BG_COLOUR)
        game.render_board(screen)

        while True:

            for event in pygame.event.get():

                # click
                # toDo increase validation rule
                if event.type == pygame.MOUSEBUTTONDOWN and game.playing:
                    xclick, yclick = event.pos

                    if game.board.valid_sqr(xclick, yclick, self.nextCell):
                        self.nextCell =game.board.mark_sqr(xclick, yclick, game.player, self.nextCell)
                        logging.info('nextCell = %s',self.nextCell)
                        game.board.draw_fig(screen, xclick, yclick)

                        self.nextCellRow = self.nextCell[0]
                        self.nextCellCol = self.nextCell[1]
                        if game.board.next_board_full(xclick, yclick, self.nextCell):
                            self.nextCell = [-1,-1] 
                        
                        # ultimate winner ?
                        winner = game.board.check_draw_win(screen)
                        if winner:
                            game.board.manage_win(screen, winner, onmain=True)
                            game.ultimate_winner(screen, winner)

                        game.next_turn()
                    else:
                        logging.info('Invalid move!')

                # keypress
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        logging.info('Restarting the game!')
                        game.restart()
                        self.screen.fill(BG_COLOUR)
                        game.render_board(screen)

                # quit
                if event.type == pygame.QUIT:
                    logging.info('Quitting')
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.mainloop()
