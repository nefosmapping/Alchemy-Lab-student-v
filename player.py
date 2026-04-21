import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = (0, 255, 0)
        self.speed = 5

        self.hp = 100

        self.image = None
        self.load_image()

    def load_image(self):
        self.image = pygame.image.load("assets/images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def is_alive(self):
        if self.hp <= 0:
            return False        
        return True

    def take_damage(self):
        self.hp -= 1
    
    def move(self, keys):
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))