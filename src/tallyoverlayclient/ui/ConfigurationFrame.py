from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk

from tallyoverlayclient.models import Configuration


class ConfigFrame():
    def _build_config(self) -> Configuration:
        return Configuration(
            tally_ip=self.server.get(),
            tally_port=int(self.port.get()),
            device_id=self.identifier.get()
        )

    def onSave(self) -> None:
        if self.parentOnSave is None:
            return
        try:
            self.parentOnSave(self._build_config())
        except ValueError:
            pass

    def onConnect(self) -> None:
        if self.parentOnConnect is None:
            return
        try:
            self.parentOnConnect(self._build_config())
        except ValueError:
            pass

    def onQuit(self) -> None:
        if self.parentOnQuit is None:
            return
        self.parentOnQuit()

    def __init__(
        self,
        root: tk.Tk,
        onSave: Optional[Callable[[Configuration], None]] = None,
        onConnect: Optional[Callable[[Configuration], None]] = None,
        onQuit: Optional[Callable[[], None]] = None,
    ):

        self.parentOnSave = onSave
        self.parentOnConnect = onConnect
        self.parentOnQuit = onQuit

        root.grid()
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        frm = ttk.Frame(root, padding=10)
        frm.grid(sticky=tk.NSEW)
        frm.grid_columnconfigure(1, weight=1)

        row = 0
        ttk.Label(frm, text="Tally Server IP:").grid(column=0, row=row, sticky=tk.W)
        self.server = ttk.Entry(frm)
        self.server.insert(0, "127.0.0.1")
        self.server.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Label(frm, text="Tally Server Port:").grid(column=0, row=row, sticky=tk.W)
        self.port = ttk.Entry(frm)
        self.port.insert(0, "4455")
        self.port.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Label(frm, text="Device ID:").grid(column=0, row=row, sticky=tk.W)
        self.identifier = ttk.Entry(frm)
        self.identifier.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(frm, text="Save", command=self.onSave).grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(frm, text="Connect", command=self.onConnect).grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(frm, text="Quit", command=self.onQuit).grid(column=1, row=row, sticky=tk.EW)
