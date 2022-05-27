import pygame
from sprites import BIRD_IMGS
import random


class Player:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.y = y
        self.x = x

        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y

        self.img_count = 0
        self.image = self.IMGS[0]

        self.color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))

        self.height = self.y

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def render(self, win):
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.image = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.image = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.image = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.image = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
        pygame.draw.rect(win, self.color, (new_rect.x,
                         new_rect.y, new_rect.width, new_rect.height), 2)

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        if d >= 16:
            d = 16
        if d < 0:
            d -= 2
        self.y += d
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
