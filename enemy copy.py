# game/enemy.py
import pygame
import random
from config.config import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)



class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.color = (255, 0, 0)  # Красный
        self.speed = 2
        self.hp = 2

        self.max_hp = 2

        self.image = None
        self.load_image()

    def load_image(self):
        for i in images:
            if i == 1:
                self.image = pygame.image.load(images[1]).convert_alpha()
            elif i == 2:
                self.image = pygame.image.load(images[2]).convert_alpha()
            elif i == 3:
                self.image = pygame.image.load(images[3]).convert_alpha()

        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def move_to_player(self, player_x, player_y):
        """Движется к игроку"""
        if self.x < player_x:
            self.x += self.speed
        elif self.x > player_x:
            self.x -= self.speed

        if self.y < player_y:
            self.y += self.speed
        elif self.y > player_y:
            self.y -= self.speed

    def hit(self):
        """Попадание по врагу"""
        self.hp -= 1
        return self.hp <= 0  # True если умер

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        bar_width = self.size
        bar_height = 5
        health_percentage = self.hp / self.max_hp
        pygame.draw.rect(screen, RED,(self.x, self.y - 10, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN,(self.x, self.y - 10, bar_width * health_percentage, bar_height))