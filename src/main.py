import tkinter
from tkinter import Tk, Toplevel, ttk

root = Tk()
root.grid()
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
frm = ttk.Frame(root, padding=10)
frm.grid(sticky=tkinter.NSEW)
frm.grid_columnconfigure(1, weight=1)


def save() -> None:
    print("Server:", server.get())
    frame.configure(style="program.TFrame")


def connect() -> None:
    print("Server:", server.get())
    frame.configure(style="offline.TFrame")


row = 0
ttk.Label(frm, text="Tally Server IP:").grid(column=0, row=row, sticky=tkinter.W)
server = ttk.Entry(frm)
server.insert(0, "127.0.0.1")
server.grid(column=1, row=row, sticky=tkinter.EW)
row+=1

ttk.Label(frm, text="Tally Server Port:").grid(column=0, row=row, sticky=tkinter.W)
port = ttk.Entry(frm)
port.insert(0, "4455")
port.grid(column=1, row=row, sticky=tkinter.EW)
row+=1

ttk.Label(frm, text="Device ID:").grid(column=0, row=row, sticky=tkinter.W)
identifier = ttk.Entry(frm)
identifier.grid(column=1, row=row, sticky=tkinter.EW)
row+=1

ttk.Button(frm, text="Save", command=save).grid(column=1, row=row, sticky=tkinter.EW)
row+=1

ttk.Button(frm, text="Connect", command=connect).grid(column=1, row=row, sticky=tkinter.EW)
row+=1

ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=row, sticky=tkinter.EW)

style = ttk.Style()
style.configure("program.TFrame", background="red")
style.configure("preview.TFrame", background="green")
style.configure("aux.TFrame", background="blue")
style.configure("offline.TFrame", background="purple")

overlay = Toplevel(root)
overlay.wm_attributes("-topmost", True)
overlay.wm_attributes("-fullscreen", True)
overlay.wm_attributes("-transparentcolor", "purple")
overlay.grid()
overlay.grid_columnconfigure(0, weight=1)
overlay.grid_rowconfigure(0, weight=1)
frame = ttk.Frame(overlay, padding=5, borderwidth=2, style="program.TFrame")
frame.grid(row=0, column=0, sticky=tkinter.NSEW)
frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
label = ttk.Label(frame, text="")
label.configure(background="purple")
label.grid(row=0, column=0, sticky=tkinter.NSEW)

root.focus_force()
root.mainloop()
