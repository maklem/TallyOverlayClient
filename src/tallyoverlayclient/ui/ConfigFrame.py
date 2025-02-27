import tkinter as tk
from tkinter import ttk
from typing import Any

from tallyoverlayclient.models import ConnectionState
from .ConfigFrameViewModel import ConfigFrameViewModel


class ConfigFrame():
    def __init__(
        self,
        root: tk.Tk,
        view_model: ConfigFrameViewModel,
    ) -> None:
        self._parent = root
        self._view_model = view_model
        self._visible = True

        @self._view_model.connection_state.on_change
        def onStageChanged(new_stage: ConnectionState) -> None:
            self._build_contents()

        @self._view_model.devices.on_change
        def onDevicesChanged(tally_devices: list[str]) -> None:
            self._tally_devices = tally_devices
            self._build_contents()

        @self._view_model.visible.on_change
        def onVisibleChanged(visible: bool) -> None:
            if self._visible == visible:
                return
            if visible:
                self._parent.deiconify()
            else:
                self._parent.iconify()
            self._visible = visible

        self._parent.bind('<Map>', self._on_tk_map)
        self._parent.bind('<Unmap>', self._on_tk_unmap)

        self._tally_server = view_model.server.bind_to_tkinter(tk.StringVar(self._parent))
        self._tally_port = view_model.port.bind_to_tkinter(tk.IntVar(self._parent))
        self._tally_deviceid = view_model.device_id.bind_to_tkinter(tk.StringVar(self._parent))
        self._tally_autoconnect = view_model.autoconnect.bind_to_tkinter(tk.BooleanVar(self._parent))
        self._tally_devices = view_model.devices.get()

        self._parent.grid()
        self._parent.grid_columnconfigure(0, weight=1)
        self._parent.grid_rowconfigure(0, weight=1)

        self._frame = ttk.Frame(self._parent, padding=10)
        self._frame.grid(sticky=tk.NSEW)
        self._frame.grid_columnconfigure(1, weight=1)

        self._build_contents()

    def _on_tk_map(self, _: 'tk.Event[Any]') -> None:
        self._visible = True
        self._view_model.visible.set(True)

    def _on_tk_unmap(self, _: 'tk.Event[Any]') -> None:
        self._visible = False
        self._view_model.visible.set(False)

    def _build_contents(self) -> None:
        for item in self._frame.winfo_children():
            item.destroy()

        connect_controls_state = (
            "normal" if self._view_model.connection_state.get() == ConnectionState.DISCONNECTED else "disabled")
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
            command=self._view_model.onConnect,
            state=connect_controls_state,
        ).grid(column=1, row=row, sticky=tk.EW)
        row+=1

        device_controls_state = (
            "normal" if self._view_model.connection_state.get() == ConnectionState.CONNECTED else "disabled")

        ttk.Label(self._frame, text="Device ID:").grid(column=0, row=row, sticky=tk.W)
        self._identifier = ttk.Combobox(self._frame, textvariable=self._tally_deviceid, values=self._tally_devices,
                                        state=device_controls_state)
        self._identifier.grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(self._frame, text="Attach", command=self._view_model.onAttach, state=device_controls_state)\
            .grid(column=1, row=row, sticky=tk.EW)
        row+=1

        storage_controls_state = (
            "normal" if self._view_model.connection_state.get() == ConnectionState.LISTENING else "disabled")

        ttk.Checkbutton(self._frame,
                        text="autoconnect",
                        variable=self._tally_autoconnect,
                        state=storage_controls_state)\
            .grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(self._frame, text="Save", command=self._view_model.onSave, state=storage_controls_state)\
            .grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(self._frame,
                   text="Listening... - Hide?",
                   command=self._view_model.onHide,
                   state=storage_controls_state)\
            .grid(column=1, row=row, sticky=tk.EW)
        row+=1

        ttk.Button(self._frame, text="Quit", command=self._view_model.onQuit).grid(column=1, row=row, sticky=tk.EW)
