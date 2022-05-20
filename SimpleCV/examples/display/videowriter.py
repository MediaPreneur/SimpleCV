#!/usr/bin/python

from SimpleCV import *
import time

c = Camera()
vs = VideoStream("foo.avi")

for _ in range(500):
    c.getImage().edges().invert().save(vs)
    time.sleep(0.05)
