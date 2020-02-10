import subprocess as sp
import tkinter as tk
from tkinter import ttk

topRow = 0
WHITE_COLOR = "#ffffff"


def on_mousewheel(event):
    if event.num == 5 or event.delta == -120:
        canvas.yview_scroll(1, "units")
    if event.num == 4 or event.delta == 120:
        canvas.yview_scroll(-1, "units")


class KeyLabel(tk.Label):
    def __init__(self, key, row, master=None, *cnf, **kw):
        super(KeyLabel, self).__init__(master=master, *cnf, **kw)
        self.key = key
        self.row = row
        self.backGroundColor = "#c4e8f2"
        self.bind("<Button-1>", self.renderValues)

    def renderValues(self, event):
        [row.configure(background=WHITE_COLOR)
         for row in scrollable_frame.grid_slaves(column=0)]
        self.configure(background=self.backGroundColor)
        [row.configure(text="", bg=WHITE_COLOR)
         for row in scrollable_frame.grid_slaves(column=1)]
        for e, i in enumerate(var_dict[self.key]):
            tk.Label(scrollable_frame, text=i, bg=WHITE_COLOR).grid(
                column=1, row=self.row+e)
            print(i)

    # list of all system variables
cmd = ["env"]
proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)

o, e = proc.communicate()

variables = str.split(str(o), "\\n")
var_dict = {}
for variable in variables:
    # get variable
    var = str.split(variable, "=")
    # get values
    if (len(var) < 2):
        continue
    val = str.split(var[1], ":")
    var_dict[var[0]] = val

print(var_dict['PATH'])

# GUI
root = tk.Tk()
root.title("System variables manager")
root.grid()
container = ttk.Frame(root)
container.configure(width=500)
canvas = tk.Canvas(container, bg=WHITE_COLOR)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=WHITE_COLOR)
scrollable_frame.grid()

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame,
                     anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set, width=1000)

root.bind("<Button-4>", on_mousewheel)
root.bind("<Button-5>", on_mousewheel)

for e, i in enumerate(var_dict.keys()):
    label = KeyLabel(i, e, scrollable_frame, text=i, bg=WHITE_COLOR)
    label.grid(row=e, column=0)

container.grid(sticky="S")
canvas.grid()
scrollbar.grid(row=0, column=1, sticky="NSW")

root.mainloop()
