# game/bullet.py
import pygame


class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.size = 8
        self.color = (255, 255, 0)  # Желтый
        self.speed = 7

        # Направление к цели
        if target_x > x:
            self.dx = self.speed
        elif target_x < x:
            self.dx = -self.speed
        else:
            self.dx = 0

        if target_y > y:
            self.dy = self.speed
        elif target_y < y:
            self.dy = -self.speed
        else:
            self.dy = 0

    def move(self):
        """Летит по прямой"""
        self.x += self.dx
        self.y += self.dy

        # Проверка выхода за экран (пуля исчезает)
        if self.x < -100 or self.x > 900 or self.y < -100 or self.y > 700:
            return True  # Пуля улетела
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))