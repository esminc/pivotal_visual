# coding: utf-8

import math
import random

class Shape(object):
    pass

class FillLayout(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.shapes = []

    def add_circle(self, key, radius, seed=None):
        shape = Shape()
        shape.key = key
        shape.radius = radius
        if seed:
            random.seed(seed)
        shape.x = int(random.random() * self.width)
        shape.y = int(random.random() * self.height)
        self.shapes.append(shape)

    def stabilize(self, max_trial=100, minimum=1.0):
        for i in xrange(max_trial):
            d = self.shift_apart()
            if d <= minimum:
                return

    def shift_apart(self):
        total_shift_dist = 0.0
        for s in self.shapes:
            fx = fy = 0.0

            # apply strong forth to be within rect
            if s.x - s.radius < 0:
                fx += -(s.x - s.radius)
            if self.width < s.x + s.radius:
                fx += self.width - (s.x + s.radius)
            if s.y - s.radius < 0:
                fy += -(s.y - s.radius)
            if self.height < s.y + s.radius:
                fy += self.height - (s.y + s.radius)

            # apply weak forth to be within rect
            if 0 < s.x - s.radius < s.radius:
                fx += -(s.x - 2 * s.radius) / 8.0
            if self.width - s.radius < s.x + s.radius < self.width:
                fx += (self.width - (s.x + 2 * s.radius)) / 8.0
            if 0 < s.y - s.radius < s.radius:
                fy += -(s.y - 2 * s.radius) / 8.0
            if self.height - s.radius < s.y + s.radius < self.height:
                fy += (self.height - (s.y + 2 * s.radius)) / 8.0

            # apply mid forth to separate with each other
            for s2 in self.shapes:
                if s == s2: continue
                dist = math.sqrt((s.x - s2.x) ** 2 + (s.y - s2.y) ** 2)
                minimum_dist = (s.radius + s2.radius) * 1.2
                if dist >= minimum_dist: continue
                f = ((minimum_dist) - dist) / (minimum_dist)
                fx += (s.x - s2.x) * f / 4.0
                fy += (s.y - s2.y) * f / 4.0
            s.x += fx
            s.y += fy
            total_shift_dist += abs(fx) + abs(fy)
        return total_shift_dist
