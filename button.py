import pygame

class UI_Element:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def draw(self, surface):
        pass

    def handle_event(self, event):
        pass

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class Button(UI_Element):
    def __init__(self, x, y, image, scale):
        super().__init__(x, y)
        width = image.get_width()
        height = image.get_height()
        self._image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self._rect = self._image.get_rect()
        self._rect.topleft = (x, y)
        self._clicked = False

    def draw(self, surface):
        surface.blit(self._image, (self._rect.x, self._rect.y))

    def handle_event(self, event):
        action = False
        if event.type == pygame.MOUSEBUTTONDOWN and self._rect.collidepoint(event.pos):
            self._clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and self._clicked:
            self._clicked = False
            action = True
        return action

    @property
    def clicked(self):
        return self._clicked

    @clicked.setter
    def clicked(self, value):
        self._clicked = value
