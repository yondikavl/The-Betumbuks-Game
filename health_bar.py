from abc import ABC, abstractmethod
import pygame

class HealthBar(ABC):
    def __init__(self, health, x, y):
        self._health = health
        self._max_health = health
        self._x = x
        self._y = y
        
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass
        
class GreenLegion_Health(HealthBar):
    def __init__(self, health, x, y):
        super().__init__(health, x, y)
        self.width = 400
        self.height = 12
        self.border_color = (255, 255, 255)
        self._health_color = (255, 0, 0)
        self.damage_color = (0, 255, 0)
    
    def update(self, health):
        self._health = health
        
    def draw(self, surface):
        ratio = self._health / self._max_health
        pygame.draw.rect(surface, self.border_color, (self._x - 2, self._y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(surface, self.damage_color, (self._x, self._y, self.width * ratio, self.height)) # Decrease health from left to right
        pygame.draw.rect(surface, self._health_color, (self._x + self.width * ratio, self._y, self.width * (1 - ratio), self.height)) # Increase health from left to right

        
class LaSquadra_Health(HealthBar):
    def __init__(self, health, x, y):
        super().__init__(health, x, y)
        self.width = 400
        self.height = 12
        self.border_color = (255, 255, 255)
        self._health_color = (255, 0, 0)
        self.damage_color = (0, 255, 0)
    
    def update(self, health):
        self._health = health
        
    def draw(self, surface):
        ratio = self._health / self._max_health
        pygame.draw.rect(surface, self.border_color, (self._x - 2, self._y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(surface, self.damage_color, (self._x + self.width * (1 - ratio), self._y, self.width * ratio, self.height)) # Decrease health from right to left
        pygame.draw.rect(surface, self._health_color, (self._x, self._y, self.width * (1 - ratio), self.height)) # Increase health from right to left


