#coding: utf-8

import pygame
import random
import time

from layout import FillLayout

class Visual(object):
    BOX_FRAME_COLOR = 255, 255, 255
    BOX_FILL_COLOR = 0, 0, 0

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 800))
        self.drawings = {}

        self.iteration_area = pygame.Rect(100, 100, 300, 600)

    def draw_iteration_boxes(self, iteration_count):
        Visual.BOX_FRAME_COLOR = 255, 255, 255
        Visual.BOX_FILL_COLOR = 0, 0, 0
        self.iteration_count = iteration_count
        self.iteration_height = self.iteration_area.height / iteration_count
        for it in range(iteration_count):
            frame_rect = pygame.Rect(self.iteration_area.left,
                                     self.iteration_area.top + it * self.iteration_height,
                                     self.iteration_area.width - 1,
                                     self.iteration_height)
            inner_rect = pygame.Rect(frame_rect.left + 1, frame_rect.top + 1, frame_rect.width - 2, frame_rect.height - 2)
            pygame.draw.rect(self.screen, Visual.BOX_FRAME_COLOR, frame_rect)
            pygame.draw.rect(self.screen, Visual.BOX_FILL_COLOR, inner_rect)
        pygame.display.flip()

    def draw_stories_for_iteration(self, stories, iteration):
        rect = ((0, iteration * self.iteration_height), (299, (iteration + 1) * self.iteration_height))
        w = rect[1][0] - rect[0][0]
        h = rect[1][1] - rect[0][1]
        layout = FillLayout(width=w, height=h)
        for s in stories:
            est = int(s.get('estimate', 0))
            if est < 0: continue
            r = est * 5 + 2
            layout.add_circle(s, r)
        layout.stabilize()

        green = 0, 255, 0
        group = pygame.sprite.Group()
        for shape in layout.shapes:
            sprite = pygame.sprite.DirtySprite(group)
            sprite.image = pygame.Surface((shape.radius * 2, shape.radius * 2), flags=pygame.SRCALPHA)
            sprite.image.fill((0, 0, 0, 0))
            sprite.rect = pygame.Rect(int(shape.x - shape.radius),
                                      int(shape.y  - shape.radius + self.iteration_height * iteration),
                                      int(shape.x + shape.radius),
                                      int(shape.y + shape.radius + self.iteration_height * iteration))
            sprite.rect.left += self.iteration_area.left
            sprite.rect.top += self.iteration_area.top
            pygame.draw.circle(sprite.image, green, (shape.radius, shape.radius), int(shape.radius), 1)

        group.draw(self.screen)
        pygame.display.flip()

