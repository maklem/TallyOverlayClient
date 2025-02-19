from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk

from tallyoverlayclient.models import AppStage, AppStageVar


class ConfigFrame():
    def _onSave(self) -> None:
        if self._parentOnSave is not None:
            self._parentOnSave()

    def _onConnect(self) -> None:
        if self._parentOnConnect is not None:
            self._parentOnConnect()

    def _onQuit(self) -> None:
        if self._parentOnQuit is not None:
            self._parentOnQuit()

    def __init__(
        self,
        root: tk.Tk,
        onSave: Optional[Callable[[], None]] = None,
        onConnect: Optional[Callable[[], None]] = None,
        onQuit: Optional[Callable[[], None]] = None,
        server: Optional[tk.StringVar] = None,
        port: Optional[tk.IntVar] = None,
        device_id: Optional[tk.StringVar] = None,
        appstage: Optional[AppStageVar] = None,
    ):
        self._stage = appstage or AppStageVar()

        def onStageChanged(_1: str, _2: str, _3: str) -> None:
            print("new stage value:", self._stage)
            self._build_contents()

        self._stage.trace_add('write', onStageChanged)

        self._parent = root
        self._parentOnSave = onSave
        self._parentOnConnect = onConnect
        self._parentOnQuit = onQuit

        self._tally_server = server or tk.StringVar()
        self._tally_port = port or tk.IntVar()
        self._tally_deviceid = device_id or tk.StringVar()

        root.grid()
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        self._build_contents()

    def _build_contents(self) -> None:
        for item in self._parent.winfo_children():
            item.destroy()

        frm = ttk.Frame(self._parent, padding=10)
        frm.grid(sticky=tk.NSEW)
        frm.grid_columnconfigure(1, weight=1)

        connect_controls_state = "normal" if self._stage.get() == AppStage.DISCONNECTED else "disabled"
        row = 0
        ttk.Label(frm, text="Tally Server IP:").grid(column=0, row=row, sticky=tk.W)
        self._server = ttk.Entry(frm, textvariable=self._tally_server, state=connect_controls_state)
        self._server.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Label(frm, text="Tally Server Port:").grid(column=0, row=row, sticky=tk.W)
        self._port = ttk.Spinbox(frm, textvariable=self._tally_port, to=65500, state=connect_controls_state)
        self._port.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(
            frm,
            text="Connect",
            command=self._onConnect,
            state=connect_controls_state,
        ).grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Label(frm, text="Device ID:").grid(column=0, row=row, sticky=tk.W)
        self._identifier = ttk.Combobox(frm, textvariable=self._tally_deviceid, values=["A", "B", "C"])
        self._identifier.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(frm, text="Save", command=self._onSave).grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(frm, text="Quit", command=self._onQuit).grid(column=1, row=row, sticky=tk.EW)
