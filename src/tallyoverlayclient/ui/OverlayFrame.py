from enum import Enum
import tkinter as tk
from tkinter import ttk


class OverlayState(Enum):
    PROGRAM = "overlay.program.TFrame"
    PREVIEW = "overlay.preview.TFrame"
    AUX = "overlay.aux.TFrame"
    OFFLINE = "overlay.offline.TFrame"


class OverlayFrame():
    def __init__(self, root: tk.Tk):

        self.style = ttk.Style()
        self.style.configure("overlay.program.TFrame", background="red")
        self.style.configure("overlay.preview.TFrame", background="green")
        self.style.configure("overlay.aux.TFrame", background="blue")
        self.style.configure("overlay.offline.TFrame", background="purple")

        self.overlay = tk.Toplevel(root)
        self.overlay.wm_attributes("-topmost", True)
        self.overlay.wm_attributes("-fullscreen", True)
        self.overlay.wm_attributes("-transparentcolor", "purple")
        self.overlay.grid()
        self.overlay.grid_columnconfigure(0, weight=1)
        self.overlay.grid_rowconfigure(0, weight=1)
        self.frame = ttk.Frame(self.overlay, padding=5, borderwidth=2, style=OverlayState.AUX.value)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.label = ttk.Label(self.frame, text="")
        self.label.configure(background="purple")
        self.label.grid(row=0, column=0, sticky=tk.NSEW)

    def setStatus(self, state: OverlayState) -> None:
        self.frame.configure(style=state.value)
