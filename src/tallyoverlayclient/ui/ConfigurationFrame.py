from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk

from tallyoverlayclient.models import AppStage, Property


class ConfigFrame():
    def _onSave(self) -> None:
        if self._parentOnSave is not None:
            self._parentOnSave()

    def _onConnect(self) -> None:
        if self._parentOnConnect is not None:
            self._parentOnConnect()

    def _onAttach(self) -> None:
        if self._parentOnAttach is not None:
            self._parentOnAttach()

    def _onQuit(self) -> None:
        if self._parentOnQuit is not None:
            self._parentOnQuit()

    def _onHide(self) -> None:
        if self._parentOnHide is not None:
            self._parentOnHide()

    def __init__(
        self,
        root: tk.Tk,
        onSave: Optional[Callable[[], None]] = None,
        onConnect: Optional[Callable[[], None]] = None,
        onAttach: Optional[Callable[[], None]] = None,
        onHide: Optional[Callable[[], None]] = None,
        onQuit: Optional[Callable[[], None]] = None,
        server: Property[str] = Property[str](value="localhost"),
        port: Property[int] = Property[int](value=4455),
        devices: Property[list[str]] = Property(value=[]),
        device_id: Property[str] = Property[str](value=""),
        autoconnect: Property[bool] = Property[bool](value=False),
        appstage: Property[AppStage] = Property[AppStage](value=AppStage.DISCONNECTED),
    ):
        @appstage.on_change
        def onStageChanged(new_stage: AppStage) -> None:
            print("new stage value:", self._stage.get().name)
            self._build_contents()

        @devices.on_change
        def onDevicesChanged(tally_devices: list[str]) -> None:
            self._tally_devices = tally_devices
            self._build_contents()

        self._stage = appstage

        self._parent = root
        self._parentOnSave = onSave
        self._parentOnConnect = onConnect
        self._parentOnAttach = onAttach
        self._parentOnQuit = onQuit
        self._parentOnHide = onHide

        self._tally_server = server.bind_to_tkinter(tk.StringVar(self._parent))
        self._tally_port = port.bind_to_tkinter(tk.IntVar(self._parent))
        self._tally_deviceid = device_id.bind_to_tkinter(tk.StringVar(self._parent))
        self._tally_autoconnect = autoconnect.bind_to_tkinter(tk.BooleanVar(self._parent))
        self._tally_devices = devices.get()

        root.grid()
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self._frame = ttk.Frame(self._parent, padding=10)
        self._frame.grid(sticky=tk.NSEW)
        self._frame.grid_columnconfigure(1, weight=1)

        self._build_contents()

    def _build_contents(self) -> None:
        for item in self._frame.winfo_children():
            item.destroy()

        connect_controls_state = "normal" if self._stage.get() == AppStage.DISCONNECTED else "disabled"
        row = 0
        ttk.Label(self._frame, text="Tally Server IP:").grid(column=0, row=row, sticky=tk.W)
        self._server = ttk.Entry(self._frame, textvariable=self._tally_server, state=connect_controls_state)
        self._server.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Label(self._frame, text="Tally Server Port:").grid(column=0, row=row, sticky=tk.W)
        self._port = ttk.Spinbox(self._frame, textvariable=self._tally_port, to=65500, state=connect_controls_state)
        self._port.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(
            self._frame,
            text="Connect",
            command=self._onConnect,
            state=connect_controls_state,
        ).grid(column=1, row=row, sticky=tk.EW)
        row+=1

        device_controls_state = "normal" if self._stage.get() == AppStage.CONNECTED else "disabled"

        ttk.Label(self._frame, text="Device ID:").grid(column=0, row=row, sticky=tk.W)
        self._identifier = ttk.Combobox(self._frame, textvariable=self._tally_deviceid, values=self._tally_devices,
                                        state=device_controls_state)
        self._identifier.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(self._frame, text="Attach", command=self._onAttach, state=device_controls_state)\
            .grid(column=1, row=row, sticky=tk.EW)
        row+=1

        storage_controls_state = "normal" if self._stage.get() == AppStage.LISTENING else "disabled"

        ttk.Checkbutton(self._frame,
                        text="autoconnect",
                        variable=self._tally_autoconnect,
                        state=storage_controls_state)\
            .grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(self._frame, text="Save", command=self._onSave, state=storage_controls_state)\
            .grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(self._frame, text="Listening... - Hide?", command=self._onHide, state=storage_controls_state)\
            .grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(self._frame, text="Quit", command=self._onQuit).grid(column=1, row=row, sticky=tk.EW)
