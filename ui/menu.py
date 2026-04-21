"""Menu panel class"""
import pygame
from ui.panel import Panel
from ui.button import Button
from config.config import *


class MenuPanel(Panel):
    def __init__(self, screen_width, screen_height):
        super().__init__(0, 0, screen_width, screen_height, (50, 50, 50))

        btn_width = 200
        btn_height = 50
        btn_x = screen_width // 2 - btn_width // 2
        btn_y = screen_height // 2 - btn_height // 2

        start_button = Button(btn_x, btn_y, btn_width, btn_height, "START", BLUE, (100, 150, 255))
        self.add_button(start_button)
