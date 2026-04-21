"""Sound manager"""
import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sound('shoot', 'assets/sounds/shoot.mp3')
        try:
            pygame.mixer.music.load('assets/sounds/background.mp3')
            self.music_loaded = True
        except:
            self.music_loaded = False

    def load_sound(self, name, path):
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
        except:
            self.sounds[name] = None

    def play(self, name):
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()

    def play_music(self):
        if self.music_loaded:
            pygame.mixer.music.play()  # -1 = бесконечное повторение

    def stop_music(self):
        pygame.mixer.music.stop()
