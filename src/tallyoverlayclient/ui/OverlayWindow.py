import tkinter as tk
from tkinter import ttk

from tallyoverlayclient.models import TallyState
from .OverlayWindowViewModel import OverlayWindowViewModel


class OverlayWindow():
    def __init__(self, root: tk.Tk, view_model: OverlayWindowViewModel) -> None:
        self._view_model = view_model

        @self._view_model.tally_state.on_change
        def onStateChanged(new_state: TallyState) -> None:
            self._frame.configure(style=new_state.value)

        self._style = ttk.Style()
        self._style.configure("overlay.program.TFrame", background="red")
        self._style.configure("overlay.preview.TFrame", background="green")
        self._style.configure("overlay.aux.TFrame", background="blue")
        self._style.configure("overlay.offline.TFrame", background="purple")

        self._overlay = tk.Toplevel(root)
        self._overlay.wm_attributes("-topmost", True)
        self._overlay.wm_attributes("-fullscreen", True)
        self._overlay.wm_attributes("-transparentcolor", "purple")
        self._overlay.grid()
        self._overlay.grid_columnconfigure(0, weight=1)
        self._overlay.grid_rowconfigure(0, weight=1)
        self._frame = ttk.Frame(self._overlay, padding=2, style=TallyState.AUX.value)
        self._frame.grid(row=0, column=0, sticky=tk.NSEW)
        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_rowconfigure(0, weight=1)
        self._label = ttk.Label(self._frame, text="")
        self._label.configure(background="purple")
        self._label.grid(row=0, column=0, sticky=tk.NSEW)
