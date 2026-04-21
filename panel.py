"""Base panel class"""
import pygame


class Panel:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                if button.handle_event(event):
                    return button.text
        return None

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        for button in self.buttons:
            button.draw(screen, font)