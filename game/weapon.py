import pygame
from utils.sound import SoundManager


class Weapon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []
        self.shoot_cooldown = 0

        self.image = None
        self.original_image = None
        self.load_image()

        self.sound_manager = SoundManager()

    def load_image(self):
        self.original_image = pygame.image.load("assets/images/gun.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (30, 20))
        self.image = self.original_image

    def update_position(self, x, y):
        """Следит за игроком"""
        self.x = x
        self.y = y

    def shoot(self, target_x, target_y):
        """Стреляет, если можно"""
        if self.shoot_cooldown <= 0:
            from game.bullet import Bullet
            self.bullets.append(Bullet(self.x, self.y, target_x, target_y))
            self.shoot_cooldown = 4  # Задержка в кадрах

            # Просто вызываем звук
            if self.sound_manager:
                self.sound_manager.play('shoot')


    def update(self):
        """Обновляет пули"""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Двигаем пули и удаляем улетевшие
        bullets_to_remove = []
        for i, bullet in enumerate(self.bullets):
            if bullet.move():
                bullets_to_remove.append(i)

        for i in reversed(bullets_to_remove):
            self.bullets.pop(i)

    def draw(self, screen):
        rotated_rect = self.image.get_rect(center=(self.x + 15, self.y + 10))
        screen.blit(self.image, rotated_rect)

        # Рисуем пули
        for bullet in self.bullets:
            bullet.draw(screen)
