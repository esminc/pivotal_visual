#coding: utf-8

import pygame
import random
import time
import math
import datetime
import re

from layout import FillLayout

class Visual(object):
    BACKGROUND_COLOR = 255, 255, 255
    BOX_FRAME_COLOR = 64, 64, 64
    BOX_FILL_COLOR = 120, 120, 120

    STORY_ACCEPTED_COLOR = 92, 255, 64
    STORY_WIP_COLOR = 255, 255, 92
    STORY_UNSTARTED_COLOR = 64, 64, 64

    ITERATOIN_TEXT_COLOR = 0, 0, 0

    def start(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((500, 800))
        self.screen.fill(Visual.BACKGROUND_COLOR)
        self.drawings = {}

        self.iteration_area = pygame.Rect(100, 100, 300, 600)

    def draw_iteration_boxes(self, iteration_count):
        self.iteration_count = iteration_count
        self.iteration_height = self.iteration_area.height / iteration_count
        for it in range(iteration_count):
            frame_rect = pygame.Rect(self.iteration_area.left,
                                     self.iteration_area.top + it * self.iteration_height,
                                     self.iteration_area.width - 1,
                                     self.iteration_height + 1)
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
            r = int(((est * 5) ** 0.7) * 2) + 3
            layout.add_circle(s, r)
        layout.stabilize()

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
            state = shape.key['current_state']
            if state == 'accepted': color = Visual.STORY_ACCEPTED_COLOR
            elif state == 'unstarted': color = Visual.STORY_UNSTARTED_COLOR
            else: color = Visual.STORY_WIP_COLOR
            pygame.draw.circle(sprite.image, color+(192,), (shape.radius, shape.radius), int(shape.radius))
            pygame.draw.circle(sprite.image, color, (shape.radius, shape.radius), int(shape.radius), 1)

        group.draw(self.screen)
        pygame.display.flip()

    def draw_text(self, text, pos, size=20, color=(0,0,0), right_align=False):
        font = pygame.font.SysFont('', size)
        top = pos[1]
        for line in text.split('\n')
            text_surf = font.render(line, True, color)
            text_size = text_surf.get_size()
            if right_align:
                actual_pos = (pos[0] - text_size[0], top)
            else:
                actual_pos = (pos[0], top)
            self.screen.blit(text_surf, actual_pos)
            top += text_size[1]

    def draw_iteration_number(self, number, idx):
        right = self.iteration_area.left
        top = self.iteration_area.top + self.iteration_height * idx
        self.draw_text(number + " ", (right, top), size=28, color=Visual.ITERATOIN_TEXT_COLOR, right_align=True)

    def draw_iteration_dates(self, start_str, finish_str, idx):
        left = self.iteration_area.left + self.iteration_area.width
        top = self.iteration_area.top + self.iteration_height * idx
        start = datetime.datetime.strptime(self.strip_timezone(start_str), '%Y/%m/%d %H:%M:%S')
        finish = datetime.datetime.strptime(self.strip_timezone(finish_str), '%Y/%m/%d %H:%M:%S') - datetime.timedelta(seconds=1)
        text = "%04d/%02d/%02d\n - %02d/%02d"%(start.year, start.month, start.day, finish.month, finish.day)
        self.draw_text(text, (left, top), size=18, color=Visual.ITERATOIN_TEXT_COLOR)

    def strip_timezone(self, datetime):
        # datetime.strptime() cannot parse %Z in certain environments
        # ie. Python2.7 on Windows seems not be able to parse 'JST'
        if re.search(' [A-Z]{3}$', datetime):
            return datetime[:-4]
        else:
            return datetime
