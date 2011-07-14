#coding: utf-8

import pygame
import random
import time

from layout import FillLayout
class Visual(object):
    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((300, 600))

    def draw_iteration_boxes(self, iteration_count):
        white = 255, 255, 255
        black = 0, 0, 0
        self.iteration_count = iteration_count
        self.iteration_height = 600 / iteration_count
        for it in range(iteration_count):
            pygame.draw.rect(self.screen, white, ((0, it * self.iteration_height), (299, (it + 1) * self.iteration_height)))
            pygame.draw.rect(self.screen, black, ((1, it * self.iteration_height + 1), (298, (it + 1) * self.iteration_height - 1)))
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
        for shape in layout.shapes:
            pygame.draw.circle(self.screen, green, (int(shape.x), int(shape.y) + self.iteration_height * iteration), int(shape.radius), 1)
        pygame.display.flip()

