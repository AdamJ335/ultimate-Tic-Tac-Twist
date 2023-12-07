import pygame

from const import FONT_SIZE
from const import FONT_COLOUR
from const import OUTLINE_COLOUR
from const import CIRCLE_COLOUR
from const import CROSS_COLOUR
from const import CHECKBOX_LINE_COLOUR
from const import TEXT_OFFSET
from const import FONT_TYPE

pygame.font.init()

class Checkbox:
    def __init__(self, surface, x, y, caption="", cross_filled=False):
        self.surface = surface
        self.x = x
        self.y = y
        self.caption = caption
        self.cross_filled = cross_filled

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 20, 20)
        self.checkbox_outline = self.checkbox_obj.copy()

        self.checked = False

    def _draw_button_text(self):
        self.font = pygame.font.SysFont(FONT_TYPE, FONT_SIZE)
        self.font_surf = self.font.render(self.caption, True, FONT_COLOUR)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + TEXT_OFFSET[0], self.y + 12 / 2 - h / 2 + TEXT_OFFSET[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, CHECKBOX_LINE_COLOUR, self.checkbox_obj)
            pygame.draw.rect(self.surface, OUTLINE_COLOUR, self.checkbox_outline, 1)

            if self.cross_filled:
                pygame.draw.line(self.surface, CROSS_COLOUR, (self.x+2, self.y+1), (self.x+16, self.y+18), 4)
                pygame.draw.line(self.surface, CROSS_COLOUR, (self.x+2, self.y+18), (self.x+16, self.y+1), 4)
            else:    
                pygame.draw.circle(self.surface, CIRCLE_COLOUR, (self.x + 10, self.y + 10), 8, 3)

        elif not self.checked:
            pygame.draw.rect(self.surface, CHECKBOX_LINE_COLOUR, self.checkbox_obj)
            pygame.draw.rect(self.surface, OUTLINE_COLOUR, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update()