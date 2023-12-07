import logging 
import pygame
import sys
import webbrowser

from const import BG_COLOUR
from const import CAPTION_1P
from const import CAPTION_2P
from const import CAPTION_MAX
from const import CAPTION_REGULAR
from const import CAPTION_ULTIMATE
from const import HEIGHT
from const import WIDTH

from button import Button
from checkBox import Checkbox
from game import Game

class Main:

    def __init__(self): 
        
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BG_COLOUR)

    def menu(self):  
        pygame.display.set_caption('Menu')

        # Load game logo
        icon_img = load_img_btn('game_icon.png', 372, 250, 8)
        
        # load how to play button
        how_to_play_btn = load_img_btn('how_to_play_btn.png', 675, 184, 5)

        #load Title screen image
        title_img = load_img_btn('title_img.png', 75, 25, 1.5)

        # load modes and players labels
        mode_img = load_img_btn('mode_label_img.png', 195, 575, 5)
        players_img = load_img_btn('players_label_img.png', 620, 575, 5)

        # create start and exit button
        start_btn = load_img_btn('start_btn.png', 140, 850, 10)
        exit_btn = load_img_btn('exit_btn.png', 618, 850, 10)

        
        regular_check = Checkbox(self.screen, 200, 650, caption=CAPTION_REGULAR, cross_filled=True)
        ultimate_check = Checkbox(self.screen, 210, 700, caption=CAPTION_ULTIMATE, cross_filled=True)
        max_check = Checkbox(self.screen, 220, 750, caption=CAPTION_MAX, cross_filled=True)
        
        regular_check.checked = True
        game_modes = [regular_check, ultimate_check, max_check]

        singleplayer_check = Checkbox(self.screen, 625, 650, caption=CAPTION_1P)
        multiplayer_check = Checkbox(self.screen, 635, 700, caption=CAPTION_2P)

        multiplayer_check.checked = True
        player_modes = [singleplayer_check, multiplayer_check]

        ultimate_mode = False
        max_mode = False
        single_player = False
        while True:
            screen = self.screen
            icon_img.draw(screen)
            title_img.draw(screen)
            mode_img.draw(screen)
            players_img.draw(screen)
            exit_btn.draw(screen)

            if how_to_play_btn.draw(screen):
                self.how_to_play_screen()

            if start_btn.draw(screen):

                single_player = single_player_checked(player_modes)

                ultimate_mode, max_mode = mode_checker(game_modes)
                                
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
                    switch_check_box(event, game_modes)

                    switch_check_box(event, player_modes)

            render_checklist(game_modes)
            render_checklist(player_modes)
                
            pygame.display.flip()
               

    def play_game(self, ultimate, max_mode, single_player):

        logging.info('Loading game...')

        screen = self.screen
        screen.fill(BG_COLOUR)
        game = Game(ultimate=ultimate, max_mode=max_mode, single_player=single_player)
        game.play_game(screen)

        # game breaks out of loop, go back to menu
        self.menu()
    
    def how_to_play_screen(self):
        screen = self.screen
        screen.fill(BG_COLOUR)

        how_to_play_title = load_img_btn('how_to_play_title.png', 83, 25, 17)
        back_btn = load_img_btn('back_btn.png', 686, 820, 10)
        how_to_play_content = load_img_btn('how_to_play.png', 193, 197, 0.15)
        info_btn = load_img_btn('info_btn.png', 858, 197, 3)

        while True:
            screen.fill(BG_COLOUR)
            how_to_play_title.draw(screen)
            how_to_play_content.draw(screen)
            if info_btn.draw(screen):
                webbrowser.open(r"https://www.thegamegal.com/2018/09/01/ultimate-tic-tac-toe/")
            if back_btn.draw(screen):
                screen.fill(BG_COLOUR)
                return
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        screen.fill(BG_COLOUR)
                        return
                 # quit
                if event.type == pygame.QUIT:
                    screen.fill(BG_COLOUR)
                    return

def single_player_checked(player_modes):
    for player in player_modes:
        if player.checked:
            if player.caption == CAPTION_1P:
                return True
            if player.caption == CAPTION_2P:
                return False

def mode_checker(game_modes):
    for mode in game_modes:
        if mode.checked:
            if mode.caption == CAPTION_REGULAR:
                return False, False
            if mode.caption == CAPTION_ULTIMATE:
                return True, False
            if mode.caption == CAPTION_MAX:
                return True, True

def switch_check_box(event, check_list):
    for mode in check_list:
        mode.update_checkbox(event)
        if mode.checked:
            for b in check_list:
                if b != mode:
                    b.checked = False

def render_checklist(modes):
    for mode in modes:
        mode.render_checkbox()

def load_img_btn(file_name, xpos, ypos, scale):
    file_directory = 'assets/' + file_name
    img = pygame.image.load(file_directory).convert_alpha()
    if file_name == 'game_icon.png':
        pygame.display.set_icon(img)
    return Button(xpos, ypos, img, scale)

if __name__ == '__main__':
    main = Main()
    main.menu()
