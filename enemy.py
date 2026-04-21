# game/enemy.py
import pygame
import random
from config.config import images  # импортируем словарь с путями

RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Enemy:
    def __init__(self, x, y, enemy_type=None):
        self.x = x
        self.y = y
        self.size = 40
        self.speed = 2
        # Если тип не передан, выбираем случайно 1, 2 или 3
        self.enemy_type = enemy_type if enemy_type is not None else random.randint(1, 3)
        
        # Характеристики зависят от типа (опционально)
        if self.enemy_type == 1:
            self.hp = 2
            self.speed = 2
        elif self.enemy_type == 2:
            self.hp = 3
            self.speed = 1.5
        else:  # тип 3
            self.hp = 1
            self.speed = 3
        
        self.max_hp = self.hp
        self.image = None
        self.load_image()

    def load_image(self):
        """Загружает картинку в зависимости от типа врага"""
        try:
            # Берём путь из словаря по ключу self.enemy_type
            image_path = images.get(self.enemy_type)
            if image_path:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
            else:
                # Если пути нет – создаём заглушку
                self.image = pygame.Surface((self.size, self.size))
                self.image.fill((255, 0, 0))
        except (pygame.error, FileNotFoundError):
            # Если файл не найден – заглушка
            print(f"Не удалось загрузить картинку для типа {self.enemy_type}")
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((255, 0, 0))

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
        return self.hp <= 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
        # Полоска здоровья
        bar_width = self.size
        bar_height = 5
        health_percentage = self.hp / self.max_hp
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, bar_width * health_percentage, bar_height))