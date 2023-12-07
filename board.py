import logging
import pygame

from const import ALPHA
from const import BG_COLOUR
from const import CROSS_COLOUR
from const import CIRCLE_COLOUR
from const import DIM
from const import HEIGHT
from const import LINE_COLOUR
from const import WIDTH

from boardDims import Board_Dim

class Board:
    """Board object for each tic-tac-toe game"""
    def __init__(self, dims=None, linewidth=15, ultimate=False, max_mode=False):
        self.squares = [ [0, 0, 0] for row in range(DIM)]
        self.dims = dims

        if not dims:
            self.dims = Board_Dim(WIDTH, 0, 0)

        self.linewidth = linewidth
        self.offset = self.dims.sqsize * 0.2
        self.radius = (self.dims.sqsize // 2) * 0.7
        self.max_mode = max_mode

        if ultimate:
            self.create_ultimate()

        self.active = True

    def __str__(self):
        s = ''
        for row in range(DIM):
            for col in range(DIM):
                sqr = self.squares[row][col]
                s += str(sqr)
        return s

    def create_ultimate(self):
        for row in range(DIM):
            for col in range(DIM):

                size = self.dims.sqsize
                xcor, ycor = self.dims.xcor + (col * self.dims.sqsize), self.dims.ycor + (row * self.dims.sqsize)
                dims = Board_Dim(size=size, xcor=xcor, ycor=ycor)
                linewidth = self.linewidth - 7
                ultimate = self.max_mode

                self.squares[row][col] = Board(dims=dims, linewidth=linewidth, ultimate=ultimate, max_mode=False)
    
    def render(self, surface):
        for row in range(DIM):
            for col in range(DIM):
                sqr = self.squares[row][col]

                if isinstance(sqr, Board): sqr.render(surface)
        
        # vertical lines
        pygame.draw.line(surface, LINE_COLOUR, 
                        (self.dims.xcor + self.dims.sqsize, self.dims.ycor),
                        (self.dims.xcor + self.dims.sqsize, self.dims.ycor + self.dims.size),
                        self.linewidth)
        pygame.draw.line(surface, LINE_COLOUR, 
                        (self.dims.xcor + self.dims.size - self.dims.sqsize, self.dims.ycor),
                        (self.dims.xcor + self.dims.size - self.dims.sqsize, self.dims.ycor + self.dims.size),
                        self.linewidth)
        
        # horizontal lines
        pygame.draw.line(surface, LINE_COLOUR, (self.dims.xcor, self.dims.ycor + self.dims.sqsize),                  
                         (self.dims.xcor + self.dims.size, self.dims.ycor + self.dims.sqsize), self.linewidth)
        pygame.draw.line(surface, LINE_COLOUR, (self.dims.xcor, self.dims.ycor + self.dims.size - self.dims.sqsize), 
                         (self.dims.xcor + self.dims.size, self.dims.ycor + self.dims.size - self.dims.sqsize), self.linewidth)
    
    def highlight_valid_move (self, surface, next_cell, player):

        sqr = self.squares[next_cell[1]][next_cell[0]]
        outer_sqr = pygame.Rect(0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(surface, BG_COLOUR, outer_sqr, 4)
        
        self.render(surface)
        
        if player == 2:
            turn_colour = CIRCLE_COLOUR
        else:
            turn_colour = CROSS_COLOUR
        
        if self.free_move(next_cell):
            pygame.draw.rect(surface, turn_colour, outer_sqr, 4)
        else:
            pygame.draw.rect(surface, turn_colour, pygame.Rect(sqr.dims.xcor, sqr.dims.ycor, sqr.dims.size, sqr.dims.size), 4)
        return
        
    def next_board_full(self, next_cell, ultimate):
        if not ultimate :
            logging.info("Not relevant variable checking, set to True to validate next move")
            return True
        
        # Get Board at next cell co-ordinates. and check if active=True
        next_grid = self.squares[next_cell[1]][next_cell[0]]

        if next_grid == 1 or next_grid == 2:
            return True
        return False
        
    def fetch_valid_moves(self, next_cell, ultimate, max_mode):
        
        next_moves = []
        if self.free_move(next_cell):
            next_grid = self.squares
        else:
            next_grid = self.squares[next_cell[1]][next_cell[0]]

        if not ultimate and not max_mode:
            xcor = 0
            ycor = 0
            for col in range(3):
                for row in range(3):
                    if next_grid[col][row] == 0:
                        next_move = [col, row]
                        next_moves.append(next_move)
            next_move_pos = [xcor, ycor]
            next_moves.append(next_move_pos)
            return next_moves

        if self.free_move(next_cell):
            for grid_x in range(3):
                for grid_y in range(3):
                    next_grid = self.squares[grid_x][grid_y]
                    if next_grid != 1 and next_grid != 2:
                        if next_grid.active:
                            if next_grid.squares[grid_x][grid_y] == 0:
                                next_move = [grid_x, grid_y]
                                next_moves.append(next_move)
                                xcor = next_grid.dims.xcor
                                ycor = next_grid.dims.ycor
                                next_move_pos = [xcor, ycor]
                                next_moves.append(next_move_pos)
                                return next_moves

        xcor = next_grid.dims.xcor
        ycor = next_grid.dims.ycor
        next_grid = next_grid.squares
        if max_mode:
            for grid_x in range(3):
                for grid_y in range(3):
                    for col in range(3):
                        for row in range (3):
                            current_grid = next_grid[grid_x][grid_y]
                            if current_grid.squares[col][row] == 0:
                                next_move = [grid_x, grid_y, col, row]
                                next_moves.append(next_move)
            
            next_move_pos = [xcor, ycor]
            next_moves.append(next_move_pos)
            return next_moves
        
        for col in range(3):
            for row in range(3):
                if next_grid[col][row] == 0:
                    next_move = [col, row]
                    next_moves.append(next_move)
        next_move_pos = [xcor, ycor]
        next_moves.append(next_move_pos)
        return next_moves

    def valid_sqr(self, xclick, yclick, next_cell, max_mode):
        
        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2: row %= DIM
        if col > 2: col %= DIM

        logging.info('Validating... (xclick, row, yclick, col) -> (%s, %s, %s,  %s)', xclick, col, yclick, row)

        sqr = self.squares[row][col]
        # base case
        if not isinstance(sqr, Board) and not max_mode:
            logging.info('sqr: %s self.active %s', sqr, self.active)
            return sqr == 0 and self.active
        else:
            if self.free_move(next_cell) :
                logging.info('Ignore next move check -> Free move')
                next_cell = [col,row]
                return True
            if next_cell[0] != col or next_cell[1] != row :
                return False
            if next_cell[0] == col and next_cell[1] == row and max_mode:
                return True
        # recursive step
        return sqr.valid_sqr(xclick, yclick, next_cell, max_mode)

    def mark_sqr(self, xclick, yclick, player, next_cell):
        
        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2: row %= DIM
        if col > 2: col %= DIM

        sqr = self.squares[row][col]

        logging.info('Marking Cell -> (%s, %s)', row, col)

        # base case
        if not isinstance(sqr, Board):
            logging.info('Inner Cell found -> (%s,%s)', row, col)
            self.squares[row][col] = player
            next_cell = [col, row]
            logging.info('returning %s', next_cell)

            return next_cell

        # recursive step
        return sqr.mark_sqr(xclick, yclick, player, next_cell)


    def draw_fig(self, surface, xclick, yclick):
        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2: row %= DIM
        if col > 2: col %= DIM

        sqr = self.squares[row][col]

        # base case
        if not isinstance(sqr, Board):

            # cross
            if sqr == 1:
                # desc line
                ipos = (self.dims.xcor + (col * self.dims.sqsize) + self.offset, 
                        self.dims.ycor + (row * self.dims.sqsize) + self.offset)
                fpos = (self.dims.xcor + self.dims.sqsize * (1 + col) - self.offset, 
                        self.dims.ycor + self.dims.sqsize * (1 + row) - self.offset)
                pygame.draw.line(surface, CROSS_COLOUR, ipos, fpos, self.linewidth)

                # asc line
                ipos = (self.dims.xcor + (col * self.dims.sqsize) + self.offset, 
                        self.dims.ycor + self.dims.sqsize * (1 + row) - self.offset)
                fpos = (self.dims.xcor + self.dims.sqsize * (1 + col) - self.offset, 
                        self.dims.ycor + (row * self.dims.sqsize) + self.offset)
                pygame.draw.line(surface, CROSS_COLOUR, ipos, fpos, self.linewidth)
            
            # circle
            elif sqr == 2:
                center = (self.dims.xcor + self.dims.sqsize * (0.5 + col),
                        self.dims.ycor + self.dims.sqsize * (0.5 + row))

                pygame.draw.circle(surface, CIRCLE_COLOUR, center, self.radius, self.linewidth)

            return
        # recursive step
        sqr.draw_fig(surface, xclick, yclick)

    def manage_win(self, surface, winner, onmain=False):
        # transparent screen
        transparent = pygame.Surface( (self.dims.size, self.dims.size) )
        transparent.set_alpha( ALPHA )
        if winner == 1:
            transparent.fill(CROSS_COLOUR)
        if winner == 2:
            transparent.fill(CIRCLE_COLOUR)
        
        if onmain: 
            surface.blit(transparent, (self.dims.xcor, self.dims.ycor))
            surface.blit(transparent, (self.dims.xcor, self.dims.ycor))
        surface.blit(transparent, (self.dims.xcor, self.dims.ycor))
        
        # draw win
        if not onmain:
            logging.info("WINNER IS -> %s", winner)
            # cross
            if winner == 1:
                # desc line
                ipos = (self.dims.xcor + self.offset, 
                        self.dims.ycor + self.offset)
                fpos = (self.dims.xcor + self.dims.size - self.offset, 
                        self.dims.ycor + self.dims.size - self.offset)
                pygame.draw.line(surface, CROSS_COLOUR, ipos, fpos, self.linewidth + 7)

                # asc line
                ipos = (self.dims.xcor + self.offset, 
                        self.dims.ycor + self.dims.size - self.offset)
                fpos = (self.dims.xcor + self.dims.size - self.offset, 
                        self.dims.ycor + self.offset)
                pygame.draw.line(surface, CROSS_COLOUR, ipos, fpos, self.linewidth + 7)

            # circle
            if winner == 2:
                center = (self.dims.xcor + self.dims.size * 0.5,
                        self.dims.ycor + self.dims.size * 0.5)

                pygame.draw.circle(surface, CIRCLE_COLOUR, center, self.dims.size * 0.4, self.linewidth + 7)

        # inactive board
        self.active = False

    def check_draw_win(self, surface):
        for row in range(DIM):
            for col in range(DIM):

                # base case sqr should have numbers                    
                sqr = self.squares[row][col]

                if isinstance(sqr, Board) and sqr.active:
                    # other board win
                    winner = sqr.check_draw_win(surface)
                    if winner: # recursive step
                        self.squares[row][col] = winner
                        sqr.manage_win(surface, winner)

                # main
                # vertical wins
                for c in range(DIM):
                    if self.squares[0][c] == self.squares[1][c] == self.squares[2][c] != 0:
                        colour = CROSS_COLOUR if self.squares[0][c] == 1 else CIRCLE_COLOUR
                        # draw win
                        ipos = (self.dims.xcor + self.dims.sqsize * (0.5 + c), 
                                self.dims.ycor + self.offset)
                        fpos = (self.dims.xcor + self.dims.sqsize * (0.5 + c), 
                                self.dims.ycor + self.dims.size - self.offset)
                        pygame.draw.line(surface, colour, ipos, fpos, self.linewidth)

                        return self.squares[0][c]

                # horizontal wins
                for r in range(DIM):
                    if self.squares[r][0] == self.squares[r][1] == self.squares[r][2] != 0:
                        colour = CROSS_COLOUR if self.squares[r][0] == 1 else CIRCLE_COLOUR
                        # draw win
                        ipos = (self.dims.xcor + self.offset, 
                                self.dims.ycor + self.dims.sqsize * (r + 0.5))
                        fpos = (self.dims.xcor + self.dims.size - self.offset, 
                                self.dims.ycor + self.dims.sqsize * (r + 0.5))
                        pygame.draw.line(surface, colour, ipos, fpos, self.linewidth)

                        return self.squares[r][0]

                # diagonal wins
                # desc
                if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
                    colour = CROSS_COLOUR if self.squares[1][1] == 1 else CIRCLE_COLOUR
                    # draw win
                    ipos = (self.dims.xcor + self.offset, 
                            self.dims.ycor + self.offset)
                    fpos = (self.dims.xcor + self.dims.size - self.offset, 
                            self.dims.ycor + self.dims.size - self.offset)
                    pygame.draw.line(surface, colour, ipos, fpos, self.linewidth)

                    return self.squares[1][1]

                # asc
                if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
                    colour = CROSS_COLOUR if self.squares[1][1] == 1 else CIRCLE_COLOUR
                    # draw win
                    ipos = (self.dims.xcor + self.offset, 
                            self.dims.ycor + self.dims.size - self.offset)
                    fpos = (self.dims.xcor + self.dims.size - self.offset, 
                            self.dims.ycor + self.offset)
                    pygame.draw.line(surface, colour, ipos, fpos, self.linewidth)

                    return self.squares[1][1]
    def free_move(self, next_cell):
        return next_cell == [-1,-1]