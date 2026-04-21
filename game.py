"""The main class of the application"""

import pygame
import random
from config.config import *
from game.player import Player
from game.enemy import Enemy
from game.weapon import Weapon
from ui.menu import MenuPanel
from ui.panel import Panel
from ui.button import Button
from utils.sound import SoundManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.state = STATE_MENU
        self.font = pygame.font.Font(None, 36)

        # Игровые объекты
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.weapon = Weapon(self.player.x + 25, self.player.y + 25)
        self.enemies = []

        # Таймер для спавна врагов
        self.enemy_spawn_timer = 0
        self.score = 0

        # UI элементы
        self.top_panel = Panel(0, 0, SCREEN_WIDTH, 50, GRAY)
        menu_btn = Button(SCREEN_WIDTH - 100, 5, 90, 40, "MENU", BLUE, (100, 150, 255))
        self.top_panel.add_button(menu_btn)

        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)

        self.menu_panel = MenuPanel(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Создаём звуковой менеджер
        self.sound_manager = SoundManager()

        # Включаем музыку
        self.sound_manager.play_music()


    def handle_events(self):
        events = pygame.event.get()

        # ВАЖНО: отдельно обрабатываем события для стрельбы
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False

            # Стрельба в игре
            if self.state == STATE_GAME and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.weapon.shoot(mouse_x, mouse_y)

        # Обработка UI
        res = self.top_panel.handle_events(events)
        if res == "MENU":
            self.state = STATE_MENU

        if self.state == STATE_MENU:
            res = self.menu_panel.handle_events(events)
            if res == "START":
                self.reset_game()
                self.state = STATE_GAME

    def reset_game(self):
        """Сброс игры"""
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.weapon = Weapon(self.player.x + 25, self.player.y + 25)
        self.enemies = []
        self.score = 0
        self.enemy_spawn_timer = 0

    def spawn_enemy(self):
        """Создает врага на краю экрана"""
        side = random.randint(0, 3)

        if side == 0:  # Лево
            x = -50
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 1:  # Право
            x = SCREEN_WIDTH + 50
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # Верх
            x = random.randint(0, SCREEN_WIDTH)
            y = -50
        else:  # Низ
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 50

        enemy = Enemy(x, y)
        self.enemies.append(enemy)

    def check_collisions(self):
        """Проверяет попадания пуль во врагов"""
        for bullet in self.weapon.bullets[:]:  # Проходим по копии
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.size, bullet.size)

            for enemy in self.enemies[:]:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)

                if bullet_rect.colliderect(enemy_rect):
                    # Попадание!
                    if bullet in self.weapon.bullets:
                        self.weapon.bullets.remove(bullet)

                    if enemy.hit():
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                            self.score += 1
                    break

    def draw(self):
        if self.state == STATE_MENU:
            self.menu_panel.draw(self.screen, self.font)
        else:
            self.screen.fill(BLACK)

            # Рисуем игрока
            self.player.draw(self.screen)

            # Рисуем врагов
            for enemy in self.enemies:
                enemy.draw(self.screen)

            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (30, 22))

            hp_text = self.font.render(f"HP: {self.player.hp}", True, RED)
            self.screen.blit(hp_text, (170, 22))

            # Рисуем оружие (пули)
            self.weapon.draw(self.screen)

            # Рисуем счет
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))

            # Отладка: показываем количество пуль
            bullets_text = self.font.render(f"Bullets: {len(self.weapon.bullets)}", True, WHITE)
            self.screen.blit(bullets_text, (10, 50))

        self.top_panel.draw(self.screen, self.font)
        pygame.display.flip()

    def update(self):
        if self.state == STATE_GAME:
            # Движение игрока
            keys = pygame.key.get_pressed()
            self.player.move(keys)

            # Обновляем позицию оружия (центр игрока)
            self.weapon.update_position(self.player.x + 25, self.player.y + 25)

            # Обновляем пули
            self.weapon.update()

            # Движение врагов к игроку
            player_center_x = self.player.x + 25
            player_center_y = self.player.y + 25

            for enemy in self.enemies:
                enemy.move_to_player(player_center_x, player_center_y)

            # Спавн врагов
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer > 60:  # Каждую секунду
                self.spawn_enemy()
                self.enemy_spawn_timer = 0

            # Проверяем попадания
            self.check_collisions()

            # Проверяем столкновение игрока с врагом
            player_rect = pygame.Rect(self.player.x, self.player.y, 50, 50)
            for enemy in self.enemies:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)
                if player_rect.colliderect(enemy_rect):
                    if self.player.is_alive():
                        self.player.take_damage()
                    else:
                        self.state = STATE_MENU

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
