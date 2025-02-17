from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk

from tallyoverlayclient.models import Configuration


class ConfigFrame():
    def _build_config(self) -> Configuration:
        return Configuration(
            tally_ip=self._server.get(),
            tally_port=int(self._port.get()),
            device_id=self._identifier.get()
        )

    def _onSave(self) -> None:
        if self._parentOnSave is None:
            return
        try:
            self._parentOnSave(self._build_config())
        except ValueError:
            pass

    def _onConnect(self) -> None:
        if self._parentOnConnect is None:
            return
        try:
            self._parentOnConnect(self._build_config())
        except ValueError:
            pass

    def _onQuit(self) -> None:
        if self._parentOnQuit is None:
            return
        self._parentOnQuit()

    def load(self, config: Configuration) -> None:
        self._server.delete(0, tk.END)
        self._server.insert(0, config.tally_ip)
        self._port.delete(0, tk.END)
        self._port.insert(0, f"{config.tally_port}")
        self._identifier.delete(0, tk.END)
        self._identifier.insert(0, config.device_id)

    def __init__(
        self,
        root: tk.Tk,
        onSave: Optional[Callable[[Configuration], None]] = None,
        onConnect: Optional[Callable[[Configuration], None]] = None,
        onQuit: Optional[Callable[[], None]] = None,
    ):

        self._parentOnSave = onSave
        self._parentOnConnect = onConnect
        self._parentOnQuit = onQuit

        root.grid()
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        frm = ttk.Frame(root, padding=10)
        frm.grid(sticky=tk.NSEW)
        frm.grid_columnconfigure(1, weight=1)

        row = 0
        ttk.Label(frm, text="Tally Server IP:").grid(column=0, row=row, sticky=tk.W)
        self._server = ttk.Entry(frm)
        self._server.insert(0, "127.0.0.1")
        self._server.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Label(frm, text="Tally Server Port:").grid(column=0, row=row, sticky=tk.W)
        self._port = ttk.Entry(frm)
        self._port.insert(0, "4455")
        self._port.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Label(frm, text="Device ID:").grid(column=0, row=row, sticky=tk.W)
        self._identifier = ttk.Entry(frm)
        self._identifier.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(frm, text="Save", command=self._onSave).grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(frm, text="Connect", command=self._onConnect).grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(frm, text="Quit", command=self._onQuit).grid(column=1, row=row, sticky=tk.EW)
