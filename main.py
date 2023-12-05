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
        # Load game logo
        icon_img = pygame.image.load('assets/game_icon.png').convert_alpha()      
        pygame.display.set_icon(icon_img)

        icon_img_button = button.Button(372, 250, icon_img, 8)

        pygame.display.set_caption('Menu')

        # load how to play button
        how_to_play_img = pygame.image.load('assets/how_to_play_img.png').convert_alpha()
        how_to_play_btn = button.Button(675, 184, how_to_play_img, 5)

        # load button images
        start_img = pygame.image.load('assets/start_btn.png').convert_alpha()
        exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()

        #load Title screen image
        title_img = pygame.image.load('assets/title_img.png').convert_alpha()
        title_img_btn = button.Button(75, 25, title_img, 1.5)

        # load modes and players labels
        players_label_img = pygame.image.load('assets/players_label_img.png').convert_alpha()
        mode_label_img = pygame.image.load('assets/mode_label_img.png').convert_alpha()

        mode_label_btn = button.Button(195, 575, mode_label_img, 5)
        players_label_btn = button.Button(620, 575, players_label_img, 5)

        # create button instances
        start_btn = button.Button(140, 850, start_img, 10)
        exit_btn = button.Button(618, 850, exit_img, 10)

        
        regularCheck = Checkbox(self.screen, 200, 650, 0,
                                caption='Regular', check_color=CHECKBOX_FILL_COLOUR_GAME, cross_filled=True)
        ultimateCheck = Checkbox(self.screen, 210, 700, 1,
                                caption='Ultimate', check_color=CHECKBOX_FILL_COLOUR_GAME, cross_filled=True)
        maxCheck = Checkbox(self.screen, 220, 750, 2,
                            caption='Max!!!', check_color=CHECKBOX_FILL_COLOUR_GAME, cross_filled=True)
        regularCheck.checked = True
        game_modes = [regularCheck, ultimateCheck, maxCheck]

        ultimate_mode = False
        max_mode = False

        
        singleplayer_check = Checkbox(self.screen, 625, 650, 0, 
                                    caption='1P', check_color=CHECKBOX_FILL_COLOUR_PLAYER)
        multiplayer_check = Checkbox(self.screen, 635, 700, 0,
                                    caption='2P', check_color=CHECKBOX_FILL_COLOUR_PLAYER)
        multiplayer_check.checked = True
        player_modes = [singleplayer_check, multiplayer_check]

        single_player = False
        while True:
            screen = self.screen
            icon_img_button.draw(screen)
            title_img_btn.draw(screen)
            mode_label_btn.draw(screen)
            players_label_btn.draw(screen)

            if how_to_play_btn.draw(screen):
                print('LEARN TO PLAY YOURSELF NOOB')

            if start_btn.draw(screen):
                for player in player_modes:
                    if player.checked:
                        if player.caption == '1P':
                            single_player = True
                            print(single_player)
                        if player.caption == '2P':
                            single_player = False
                            print(single_player)
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
                logging.info('Single Player mode? %s', single_player)
                self.play_game(ultimate_mode, max_mode, single_player)
            
            pygame.display.update()
            for event in pygame.event.get():
                 # quit
                if event.type == pygame.QUIT or exit_btn.draw(screen):
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
