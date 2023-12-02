import sys
import logging 
import pygame
import button

from const import WIDTH
from const import HEIGHT
from const import BG_COLOUR
from const import CHECKBOX_FILL_COLOUR_GAME
from const import CHECKBOX_FILL_COLOUR_PLAYER

from game import Game
from checkBox import Checkbox

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

        
        regularCheck = Checkbox(self.screen, 200, 200, 0,
                                caption='Regular', check_color=CHECKBOX_FILL_COLOUR_GAME, cross_filled=True)
        ultimateCheck = Checkbox(self.screen, 200, 250, 1,
                                caption='Ultimate', check_color=CHECKBOX_FILL_COLOUR_GAME, cross_filled=True)
        maxCheck = Checkbox(self.screen, 200, 300, 2,
                            caption='Max!!!', check_color=CHECKBOX_FILL_COLOUR_GAME, cross_filled=True)
        regularCheck.checked = True
        game_modes = [regularCheck, ultimateCheck, maxCheck]

        ultimate_mode = False
        max_mode = False

        
        singleplayer_check = Checkbox(self.screen, 400, 200, 0, 
                                    caption='1P', check_color=CHECKBOX_FILL_COLOUR_PLAYER)
        multiplayer_check = Checkbox(self.screen, 400, 250, 0,
                                    caption='2P', check_color=CHECKBOX_FILL_COLOUR_PLAYER)
        multiplayer_check.checked = True
        player_modes = [singleplayer_check, multiplayer_check]

        singlePlayer = False

        while True:
            screen = self.screen

            if start_button.draw(screen):
                for player in player_modes:
                    if player.checked:
                        if player.caption == '1P':
                            singlePlayer = True
                            print(singlePlayer)
                        if player.caption == '2P':
                            singlePlayer = False
                            print(singlePlayer)
                for mode in game_modes:
                    if mode.checked:
                        if mode.caption == 'Regular':
                            ultimate_mode = False
                            max_mode = False
                        if mode.caption == 'Ultimate':
                            ultimate_mode = True
                            max_mode = False
                        if mode.caption == 'Max!!!':
                            ultimate_mode = True
                            max_mode = True
                
                logging.info('Starting game with UltimateMode -> %s and MaxMode -> %s', ultimate_mode, max_mode)
                logging.info('Single Player mode? %s', singlePlayer)
                self.play_game(ultimate_mode, max_mode, singlePlayer)
            
            pygame.display.update()
            for event in pygame.event.get():
                 # quit
                if event.type == pygame.QUIT or exit_button.draw(screen):
                    logging.info('Quitting')
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:    
                    for mode in game_modes:
                        mode.update_checkbox(event)
                        if mode.checked:
                            for b in game_modes:
                                if b != mode:
                                    b.checked = False
                    for player in player_modes:
                        player.update_checkbox(event)
                        if player.checked:
                            for b in player_modes:
                                if b != player:
                                    b.checked = False
            for mode in game_modes:
                mode.render_checkbox()
            for player in player_modes:
                player.render_checkbox()
                
            pygame.display.flip()
               

    def play_game(self, ultimate, max_mode, single_player):

        logging.info('Loading game...')

        screen = self.screen
        screen.fill(BG_COLOUR)
        game = Game(ultimate=ultimate, max_mode=max_mode, single_player=single_player)
        game.play_game(screen)
        self.menu()


if __name__ == '__main__':
    main = Main()
    main.menu()
