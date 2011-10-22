#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Life game
"""
import Tkinter as Tk

from cellmap import CellMap


class LifeGame(Tk.Frame):
    """Lifegame widget
    """
    def __init__(self, master=None,
                 view_size=(256, 256), cell_size=(16, 16), map_size=(16, 16)):
        """
        Arguments:
            master -- parent widget
            view_size -- pixel count for viewport
            cell_size -- pixel count for draw cell
            map_size -- cell count for cellmap
        """
        self.cell_width = cell_size[0]
        self.cell_height = cell_size[1]
        self.map_width = map_size[0]
        self.map_height = map_size[1]

        view_width = view_size[0]
        view_height = view_size[1]

        Tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("LifeGame")

        self.cm = CellMap(self.map_width, self.map_height)
        self.buffer = []
        self.anime = False
        self.wait = 200
        self.button_down = False
        self.drag = False

        canvas_width = self.map_width * self.cell_width
        canvas_height = self.map_height * self.cell_height
        self.canvas = Tk.Canvas(self,
                                borderwidth=2,
                                background='#ddd',
                                width=view_width,
                                height=view_height,
                                scrollregion=(0, 0,
                                              canvas_width + 1,
                                              canvas_height + 1))
        self.vscroll = Tk.Scrollbar(self,
                                    command=self.canvas.yview,
                                    orient=Tk.VERTICAL)
        self.hscroll = Tk.Scrollbar(self,
                                    command=self.canvas.xview,
                                    orient=Tk.HORIZONTAL)
        self.canvas["xscrollcommand"] = self.hscroll.set
        self.canvas["yscrollcommand"] = self.vscroll.set

        self.canvas.bind("<Button-1>", self.cmd_press)
        self.canvas.bind("<ButtonRelease-1>", self.cmd_release)
        self.canvas.bind("<Motion>", self.cmd_motion)

        ctrl_panel = Tk.Frame(self)
        bt_start = Tk.Button(ctrl_panel, text="start", command=self.cmd_start)
        bt_stop = Tk.Button(ctrl_panel, text="stop", command=self.cmd_stop)
        bt_next = Tk.Button(ctrl_panel, text="next", command=self.cmd_next)
        bt_reset = Tk.Button(ctrl_panel, text="reset", command=self.cmd_reset)
        bt_quit = Tk.Button(ctrl_panel, text="quit", command=self.cmd_quit)

        bt_start.grid(row=0, column=0)
        bt_stop.grid(row=0, column=1)
        bt_next.grid(row=0, column=2)
        bt_reset.grid(row=0, column=3)
        bt_quit.grid(row=0, column=4)

        self.canvas.grid(row=0, column=0)
        self.vscroll.grid(row=0, column=1, sticky=Tk.N + Tk.S)
        self.hscroll.grid(row=1, column=0, sticky=Tk.E + Tk.W)
        ctrl_panel.grid(row=2)

        for y in range(0, canvas_height, self.cell_height):
            self.canvas.create_rectangle(
                0,
                y,
                canvas_width,
                y + self.cell_height,
                outline='#888')
        for x in range(0, canvas_width, self.cell_width):
            self.canvas.create_rectangle(
                x,
                0,
                x + self.cell_width,
                canvas_height,
                outline='#888')

    def clear(self):
        """Clear cellmap
        """
        self.cm.set_all(False)

    def put(self, ox, oy, pattern):
        """Set pattern on cellmap
        Arguments:
            ox -- offset coddinate
            oy -- offset coodinate
            pattern -- postion list
        """
        for (cx, cy) in pattern:
            self.cm.set_alive(cx + ox, cy + oy, True)

    def push(self):
        """Save current cellmap to buffer
        """
        self.buffer = self.cm.get_positions()

    def pop(self):
        """Restore cellmap from buffer
        """
        self.clear()
        self.cm.set_positions(self.buffer)

    def redraw(self):
        """Redraw cellmap
        """
        tag = 'life'
        self.canvas.delete(tag)
        for ty in range(self.cm.height):
            for tx in range(self.cm.width):
                cell = self.cm.get(tx, ty)
                if cell.is_alive():
                    x1 = tx * self.cell_width + 1
                    y1 = ty * self.cell_height + 1
                    x2 = (tx + 1) * self.cell_width - 1
                    y2 = (ty + 1) * self.cell_height - 1
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill='#444', tags=tag)

    def nextlife(self):
        """Shows next generation.
        """
        self.cm.change_next()
        self.redraw()

    def interval(self):
        """Chage generation automatically.
        """
        if self.anime:
            self.nextlife()
            self.after(self.wait, self.interval)

    #
    # Handlers
    #
    def cmd_press(self, event):
        """Handler: mouse press
        """
        self.button_down = True
        self.drag = False
        self.canvas.scan_mark(event.x, event.y)

    def cmd_release(self, event):
        """Handler: mouse release
        """
        self.button_down = False
        if self.drag:
            pass
        else:
            x = int(self.canvas.canvasx(event.x) // self.cell_width)
            y = int(self.canvas.canvasy(event.y) // self.cell_height)
            alive = self.cm.get(x, y).is_alive()
            self.cm.set_alive(x, y, not alive)
            self.redraw()
        self.drag = False

    def cmd_motion(self, event):
        """Handler: mouse move
        """
        if self.button_down:
            self.drag = True
            self.canvas.scan_dragto(event.x, event.y, 1)

    def cmd_start(self):
        """Handler: start button
        """
        if not self.anime:
            self.anime = True
            self.interval()

    def cmd_stop(self):
        """Handler: stop button
        """
        self.anime = False

    def cmd_next(self):
        """Handler: next button
        """
        self.anime = False
        self.nextlife()

    def cmd_reset(self):
        """Handler: reset button
        """
        self.anime = False
        self.pop()
        self.redraw()

    def cmd_quit(self):
        """Handler: quit button
        """
        self.anime = False
        self.master.destroy()

if __name__ == "__main__":
    lg = LifeGame(None, (320, 320), (16, 16), (32, 32))

    # set initial pattern
    glider = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    lg.put(0, 0, glider)
    lg.put(10, 5, glider)

    # save initial pattern for reset
    lg.push()

    # draw initial pattern
    lg.redraw()

    lg.mainloop()
