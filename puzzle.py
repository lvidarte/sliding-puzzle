#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import Tkinter as tk
from PIL import Image, ImageTk


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.size = 125
        self.grid = 4
        self.steps = 0
        self.create_widgets()
        self.create_events()
        self.load_image()
        self.show()

    def create_widgets(self):
        width = self.size * self.grid
        height = width
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.grid()

    def create_events(self):
        self.canvas.bind_all('<KeyPress-Up>', self.move_crop)
        self.canvas.bind_all('<KeyPress-Down>', self.move_crop)
        self.canvas.bind_all('<KeyPress-Left>', self.move_crop)
        self.canvas.bind_all('<KeyPress-Right>', self.move_crop)
        self.canvas.bind_all('<KeyPress-h>', self.help)

    def help(self, event):
        if getattr(self, '_img_help_id', None) is None:
            self._img_help = ImageTk.PhotoImage(self._image)
            self._img_help_id = self.canvas.create_image(0, 0,
                    image=self._img_help, anchor=tk.NW)
        else:
            state = self.canvas.itemcget(self._img_help_id, 'state')
            if state == 'hidden':
                state = ''
            else:
                state = 'hidden'
            self.canvas.itemconfigure(self._img_help_id, state=state)


    def move_crop(self, event):
        slides = self.get_slides_around()

        if event.keysym == 'Up' and slides['bottom']:
                self.canvas.move(slides['bottom']['id'], 0, -self.size)
                aux = slides['bottom']['pos_a']
                slides['bottom']['pos_a'] = slides['center']['pos_a']
                slides['center']['pos_a'] = aux
                self.steps += 1
        if event.keysym == 'Down' and slides['top']:
                self.canvas.move(slides['top']['id'], 0, self.size)
                aux = slides['top']['pos_a']
                slides['top']['pos_a'] = slides['center']['pos_a']
                slides['center']['pos_a'] = aux
                self.steps += 1
        if event.keysym == 'Left' and slides['right']:
                self.canvas.move(slides['right']['id'], -self.size, 0)
                aux = slides['right']['pos_a']
                slides['right']['pos_a'] = slides['center']['pos_a']
                slides['center']['pos_a'] = aux
                self.steps += 1
        if event.keysym == 'Right' and slides['left']:
                self.canvas.move(slides['left']['id'], self.size, 0)
                aux = slides['left']['pos_a']
                slides['left']['pos_a'] = slides['center']['pos_a']
                slides['center']['pos_a'] = aux
                self.steps += 1

    def get_slides_around(self):
        slides = {'center': None,
                  'right' : None,
                  'left'  : None,
                  'top'   : None,
                  'bottom': None}

        for crop in self.image:
            if not crop['visible']:
                slides['center'] = crop
                break

        x0, y0 = slides['center']['pos_a']

        for crop in self.image:
            x1, y1 = crop['pos_a']
            if y0 == y1 and x1 == x0+1:
                slides['right'] = crop
            if y0 == y1 and x1 == x0-1:
                slides['left'] = crop
            if x0 == x1 and y1 == y0-1:
                slides['top'] = crop
            if x0 == x1 and y1 == y0+1:
                slides['bottom'] = crop

        return slides

    def load_image(self):
        self._image = Image.open("image.png")
        self.image = []

        for x in xrange(self.grid):
            for y in xrange(self.grid):
                x0 = x * self.size
                y0 = y * self.size
                x1 = x0 + self.size
                y1 = y0 + self.size
                image = ImageTk.PhotoImage(self._image.crop((x0, y0, x1, y1)))
                crop = {'id'     : None,
                        'image'  : image,
                        'pos_o'  : (x, y),
                        'pos_a'  : None,
                        'visible': True}
                self.image.append(crop)

        self.image[-1]['visible'] = False

    def show(self):
        random.shuffle(self.image)

        index = 0
        for x in xrange(self.grid):
            for y in xrange(self.grid):
                self.image[index]['pos_a'] = (x, y)
                if self.image[index]['visible']:
                    x1 = x * self.size
                    y1 = y * self.size
                    image = self.image[index]['image']
                    id = self.canvas.create_image(x1, y1, image=image, anchor=tk.NW)
                    self.image[index]['id'] = id
                index += 1


if __name__ == '__main__':

#   from optparse import OptionParser
#   parser = OptionParser(description="Random maze game")
#   parser.add_option('-W', '--width', type=int, default=21,
#                     help="maze width (must be odd)")
#   parser.add_option('-H', '--height', type=int, default=21,
#                     help="maze height (must be odd)")
#   parser.add_option('-s', '--size', type=int, default=10,
#                     help="cell size")
#   args, _ = parser.parse_args()

    app = Application()
    app.master.title('Sliding puzzle')
    app.mainloop()

