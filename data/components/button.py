import pygame as pg

from .. import prepare
from .label import Label


class Button:
    def __init__(self, text, topleft, callback, font_size=35, *args):
        self.text = text
        self.callback = callback
        self.font_size = font_size
        self.args = args
        self.create_images()
        self.image = self.image_idle
        self.rect = self.image.get_rect(topleft=topleft)
        self.hovered = False

    def calculate_size(self):
        label = Label(self.text, self.font_size)
        width = label.rect.width + 20
        height = label.rect.height + 10
        return width, height

    def create_images(self):
        width, height = self.calculate_size()
        rect = pg.rect.Rect(0, 0, width, height)
        label = Label(self.text, self.font_size, center=rect.center)
        self.image_idle = pg.transform.scale(
            prepare.GFX['ui']['button_idle'], (width, height))
        label.draw(self.image_idle)
        self.image_hover = pg.transform.scale(
            prepare.GFX['ui']['button_hover'], (width, height))
        label.draw(self.image_hover)

    def hover(self):
        self.hovered = True
        self.image = self.image_hover

    def unhover(self):
        self.hovered = False
        self.image = self.image_idle

    def click(self):
        if self.hovered:
            self.callback(*self.args)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        if self.rect.collidepoint(pg.mouse.get_pos()) and not self.hovered:
            self.hover()
        elif not self.rect.collidepoint(pg.mouse.get_pos()) and self.hovered:
            self.unhover()
