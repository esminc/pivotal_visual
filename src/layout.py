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

    def add_circle(self, key, radius):
        shape = Shape()
        shape.key = key
        shape.radius = radius
        shape.x = random.randint(0, self.width - 1)
        shape.y = random.randint(0, self.height - 1)
        self.shapes.append(shape)

    def stabilize(self, max_trial=100, minimum=1.0):
        for i in xrange(max_trial):
            d = self.shift_apart()
            if d < minimum:
                return

    def shift_apart(self):
        total_shift_dist = 0.0
        for s in self.shapes:
            fx = fy = 0
            if s.x - s.radius < 0:
                fx += -(s.x - s.radius)
            if self.width <= s.x + s.radius:
                fx += self.width - (s.x + s.radius)
            if s.y - s.radius < 0:
                fy += -(s.y - s.radius)
            if self.height <= s.y + s.radius:
                fy += self.height - (s.y + s.radius)

            for s2 in self.shapes:
                if s == s2: continue
                d = math.sqrt((s.x - s2.x) ** 2 + (s.y - s2.y) ** 2)
                if d >= s.radius + s2.radius: continue
                f = ((s.radius + s2.radius) - d) / (s.radius + s2.radius)
                fx += (s.x - s2.x) * f
                fy += (s.y - s2.y) * f
            s.x += fx / 4.0
            s.y += fy / 4.0
            total_shift_dist += abs(fx) + abs(fy)
        return total_shift_dist
