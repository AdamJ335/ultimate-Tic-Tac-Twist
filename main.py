import pygame
import sys
import logging 
import button

from const import WIDTH
from const import HEIGHT
from const import BG_COLOUR
from game import Game
from checkBox import CheckBox

class Main:

    def __init__(self): 
        
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BG_COLOUR)
        pygame.display.set_caption('ULTIMATE TIC TAC TWIST')
        self.game = Game(ultimate=True, max=True)
        self.nextCell = [-1,-1]



    def menu(self):
        pygame.display.set_caption('Menu')
        # load button images
        start_img = pygame.image.load('assets/start_btn.png').convert_alpha()
        exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()

        # create button instances
        start_button = button.Button(253, 475, start_img, 0.8)
        exit_button = button.Button(268, 600, exit_img, 0.8)

        boxes = []
        regularCheck = CheckBox(self.screen, 200, 200, 0, caption='Regular')
        ultimateCheck = CheckBox(self.screen, 200, 250, 1, caption='Ultimate')
        maxCheck = CheckBox(self.screen, 200, 300, 2, caption='Max!!!')
        boxes.append(regularCheck)
        boxes.append(ultimateCheck)
        boxes.append(maxCheck)

        while True:
            screen = self.screen
            if start_button.draw(screen):
                self.mainloop(True, False)
            
            pygame.display.update()
            for event in pygame.event.get():
                 # quit
                if event.type == pygame.QUIT or exit_button.draw(screen):
                    logging.info('Quitting')
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:    
                    for box in boxes:
                        box.update_checkbox(event)
                        if box.checked is True:
                            for b in boxes:
                                if b != box:
                                    b.checked = False
            for box in boxes:
                box.render_checkbox()
                
            pygame.display.flip()
               

    def mainloop(self, ultimate, maxMode):

        screen = self.screen
        game = Game(ultimate=ultimate, max=maxMode)

        self.screen.fill(BG_COLOUR)
        game.render_board(screen)

        while True:

            for event in pygame.event.get():

                # click
                # toDo increase validation rule
                if event.type == pygame.MOUSEBUTTONDOWN and game.playing:
                    xclick, yclick = event.pos

                    if game.check_valid_move(xclick, yclick, self.nextCell):
                        self.nextCell =game.board.mark_sqr(xclick, yclick, game.player, self.nextCell)
                        logging.info('nextCell = %s',self.nextCell)
                        game.board.draw_fig(screen, xclick, yclick)

                        self.nextCellRow = self.nextCell[0]
                        self.nextCellCol = self.nextCell[1]
                        if game.check_next_board_full(xclick, yclick, self.nextCell):
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
    main.menu()
