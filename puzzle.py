#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import Tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

im = Image.open("image.png")
size = 100
image = [[None]*5 for _ in xrange(5)]

for x in xrange(5):
    for y in xrange(5):
        x0 = x * size
        y0 = y * size
        x1 = x0 + size
        y1 = y0 + size
        print (x0, y0, x1, y1)
        image[x][y] = im.crop((x0, y0, x1, y1))

[random.shuffle(image[i]) for i in xrange(5)]
random.shuffle(image)

images = []
for x in xrange(5):
    for y in xrange(5):
        images.append(ImageTk.PhotoImage(image[x][y]))
        canvas.create_image((x*size)+50, (y*size)+50, image=images[-1])

root.mainloop()
