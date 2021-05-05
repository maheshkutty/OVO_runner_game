import pygame
import glob


class CoinSprite(pygame.sprite.Sprite):
    def __init__(self, wtoshow):
        super(CoinSprite, self).__init__()
        self.count = 0
        self.images = [pygame.image.load(img) for img in glob.glob("coin_sprite\\*.png")]
        self.images = [pygame.transform.smoothscale(img, (20,20)) for img in self.images]
        self.index = 0
        self.rect = pygame.Rect(wtoshow[0], wtoshow[1], 10, 10)

    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        if self.count>3:
            self.index += 1
            self.count = 0
        self.count = self.count + 1
