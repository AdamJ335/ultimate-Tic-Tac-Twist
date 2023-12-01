import pygame
import sys
import logging 
import button

from const import WIDTH
from const import HEIGHT
from const import BG_COLOUR
from const import CHECKBOX_FILL_COLOUR_GAME
from const import CHECKBOX_FILL_COLOUR_PLAYER

from game import Game
from checkBox import CheckBox

class Main:

    def __init__(self): 
        
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BG_COLOUR)



    def menu(self):        
        pygame.display.set_caption('Menu')
        # load button images
        start_img = pygame.image.load('assets/start_btn.png').convert_alpha()
        exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()

        # create button instances
        start_button = button.Button(260, 475, start_img, 0.8)
        exit_button = button.Button(275, 600, exit_img, 0.8)

        gameModes = []
        regularCheck = CheckBox(self.screen, 200, 200, 0, caption='Regular', check_color=CHECKBOX_FILL_COLOUR_GAME)
        ultimateCheck = CheckBox(self.screen, 200, 250, 1, caption='Ultimate', check_color=CHECKBOX_FILL_COLOUR_GAME)
        maxCheck = CheckBox(self.screen, 200, 300, 2, caption='Max!!!', check_color=CHECKBOX_FILL_COLOUR_GAME)
        regularCheck.checked = True
        gameModes.append(regularCheck)
        gameModes.append(ultimateCheck)
        gameModes.append(maxCheck)

        ultimateMode = False
        maxMode = False

        playerModes = []
        singlePlayerCheck = CheckBox(self.screen, 400, 200, 0, caption='1P', check_color=CHECKBOX_FILL_COLOUR_PLAYER)
        multiPlayerCheck = CheckBox(self.screen, 400, 250, 0, caption='2P', check_color=CHECKBOX_FILL_COLOUR_PLAYER)
        multiPlayerCheck.checked = True
        playerModes.append(singlePlayerCheck)
        playerModes.append(multiPlayerCheck)

        singlePlayer = False

        while True:
            screen = self.screen

            if start_button.draw(screen):
                for player in playerModes:
                    if player.checked:
                        if player.caption == '1P':
                            singlePlayer = True
                            print(singlePlayer)
                        if player.caption == '2P':
                            singlePlayer = False
                            print(singlePlayer)
                for mode in gameModes:
                    if mode.checked:
                        if mode.caption == 'Regular':
                            ultimateMode = False
                            maxMode = False
                        if mode.caption == 'Ultimate':
                            ultimateMode = True
                            maxMode = False
                        if mode.caption == 'Max!!!':
                            ultimateMode = True
                            maxMode = True
                
                logging.info('Starting game with UltimateMode -> %s and MaxMode -> %s', ultimateMode, maxMode)
                logging.info('Single Player mode? %s', singlePlayer)
                self.playGame(ultimateMode, maxMode, singlePlayer)
            
            pygame.display.update()
            for event in pygame.event.get():
                 # quit
                if event.type == pygame.QUIT or exit_button.draw(screen):
                    logging.info('Quitting')
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:    
                    for mode in gameModes:
                        mode.update_checkbox(event)
                        if mode.checked:
                            for b in gameModes:
                                if b != mode:
                                    b.checked = False
                    for player in playerModes:
                        player.update_checkbox(event)
                        if player.checked:
                            for b in playerModes:
                                if b != player:
                                    b.checked = False
            for mode in gameModes:
                mode.render_checkbox()
            for player in playerModes:
                player.render_checkbox()
                
            pygame.display.flip()
               

    def playGame(self, ultimate, maxMode, singlePlayer):

        logging.info('Loading game...')

        screen = self.screen
        screen.fill(BG_COLOUR)
        game = Game(ultimate=ultimate, max=maxMode, singlePlayer=singlePlayer)
        game.play_game(screen)
        self.menu()


if __name__ == '__main__':
    main = Main()
    main.menu()
