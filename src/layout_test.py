#coding: utf-8

import unittest
import math

from layout import *

LOOP_FOR_RANDOM_DISTRIBUTION = 30

class FillLayoutTest(unittest.TestCase):

    def test_fill_empty(self):
        layout = FillLayout(width=100, height=100)
        self.assertEqual(layout.shapes, [])

    def test_fill_single(self):
        for i in range(LOOP_FOR_RANDOM_DISTRIBUTION):
            layout = FillLayout(width=100, height=100)
            r = 10
            layout.add_circle('key!', r)
            layout.stabilize(minimum=0.0)

            self.assertEquals(1, len(layout.shapes))
            self.assertEqual(layout.shapes[0].key, 'key!')
            self.assertEqual(layout.shapes[0].radius, r)
            self.assertTrue((0) <= layout.shapes[0].x <= (100))
            self.assertTrue((0) <= layout.shapes[0].y <= (100))

    def test_fill_multi(self):
        layout = FillLayout(width=200, height=200)
        r = 10
        epsilon = 2.0
        count = 10
        for i in range(count):
            layout.add_circle('key%02d'%(i), r + i)
        layout.stabilize(minimum=0.0)

        self.assertEquals(count, len(layout.shapes))
        for i, s in enumerate(layout.shapes):
            self.assertEqual(s.key, 'key%02d'%(i))
            self.assertEqual(s.radius, r + i)
            self.assertTrue((0 + s.radius - epsilon) <= s.x <= (200 - s.radius + epsilon))
            self.assertTrue((0 + s.radius - epsilon) <= s.y <= (200 - s.radius + epsilon))

            for s2 in layout.shapes:
                if s == s2: continue
                d = math.sqrt(abs(s.x - s2.x) ** 2 + abs(s.y - s2.y) ** 2)
                self.assertTrue(d + epsilon >= s.radius + s2.radius)




if __name__=='__main__':
    unittest.main()
