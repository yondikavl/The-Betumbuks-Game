import pygame

class HealthBar:
    def __init__(self, health, x, y):
        self.health = health
        self.max_health = health
        self.x = x
        self.y = y
        
    def update(self):
        pass
        
    def draw(self):
        pass
        
class GreenLegion_Health(HealthBar):
    def __init__(self, health, x, y):
        super().__init__(health, x, y)
        self.width = 400
        self.height = 12
        self.border_color = (255, 255, 255)
        self.health_color = (255, 0, 0)
        self.damage_color = (0, 255, 0)
    
    def update(self, health):
        self.health = health
        
    def draw(self, surface):
        ratio = self.health / self.max_health
        pygame.draw.rect(surface, self.border_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(surface, self.damage_color, (self.x, self.y, self.width * ratio, self.height)) # Decrease health from left to right
        pygame.draw.rect(surface, self.health_color, (self.x + self.width * ratio, self.y, self.width * (1 - ratio), self.height)) # Increase health from left to right

        
class LaSquadra_Health(HealthBar):
    def __init__(self, health, x, y):
        super().__init__(health, x, y)
        self.width = 400
        self.height = 12
        self.border_color = (255, 255, 255)
        self.health_color = (255, 0, 0)
        self.damage_color = (0, 255, 0)
    
    def update(self, health):
        self.health = health
        
    def draw(self, surface):
        ratio = self.health / self.max_health
        pygame.draw.rect(surface, self.border_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(surface, self.damage_color, (self.x + self.width * (1 - ratio), self.y, self.width * ratio, self.height)) # Decrease health from right to left
        pygame.draw.rect(surface, self.health_color, (self.x, self.y, self.width * (1 - ratio), self.height)) # Increase health from right to left


