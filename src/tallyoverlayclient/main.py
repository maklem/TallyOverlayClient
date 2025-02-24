import os
import asyncio
import tkinter
import tkinter.ttk
from typing import Any

from async_tkinter_loop import async_mainloop

from tallyoverlayclient.ui import ConfigFrame, ConfigFrameViewModel, OverlayWindow, OverlayWindowViewModel
from tallyoverlayclient.models import AppDataModel, TallyState, ConnectionState
from tallyoverlayclient.data import TallyClient

CONFIG_FILENAME = "config.json"


class MainApp:
    def __init__(self) -> None:
        self._initial_connection_attempt = True
        self._model = AppDataModel()

        self._tally_client = TallyClient(
            onStateChange=self.onTallyStateChanged,
            onConnected=self.onTallyConnected,
            onDisconnected=self.onTallyDisconnected,
            onDevicesChanged=self.onTallyDevicesChanged,
        )
        self._config_view_model = ConfigFrameViewModel(
            model=self._model,
            onSave=self.onSave,
            onConnect=self.onConnect,
            onAttach=self.onAttach,
            onHide=self.onHide,
            onQuit=self.onQuit,
        )
        self._overlay_view_model = OverlayWindowViewModel(model=self._model)

    def onTallyConnected(self) -> None:
        self._model.connection_state.set(ConnectionState.CONNECTED)

        if self._model.autoconnect.get() and self._initial_connection_attempt:
            self.onAttach()
            self._model.visible.set(False)

    def onTallyDevicesChanged(self, devices: list[dict[str, Any]]) -> None:
        self._model.devices.set([f"{d['id']} - {d['name']}" for d in devices])

    def onTallyStateChanged(self, state: TallyState) -> None:
        self._model.tally_state.set(state)

    def onTallyDisconnected(self) -> None:
        self._model.connection_state.set(ConnectionState.DISCONNECTED)
        self._initial_connection_attempt = False

    def onSave(self) -> None:
        self._model.save_config(CONFIG_FILENAME)

    def onAttach(self) -> None:
        self._model.connection_state.set(ConnectionState.LISTENING)
        device = self._model.device_id.get().split(" - ", 1)[0]
        asyncio.create_task(self._tally_client.attach_to_device(device))
        pass

    def onConnect(self) -> None:
        self._model.connection_state.set(ConnectionState.CONNECTING)
        asyncio.create_task(self._tally_client.connect(hostname=self._model.server.get(), port=self._model.port.get()))

    def onHide(self) -> None:
        self._model.visible.set(False)
    
    def onQuit(self) -> None:
        self._root.destroy()

    def run(self) -> None:
        if os.path.exists(CONFIG_FILENAME):
            self._model.load_config(CONFIG_FILENAME)

        self._root = tkinter.Tk()
        self.configWindow = ConfigFrame(
            root=self._root,
            view_model=self._config_view_model
        )
        self.overlay = OverlayWindow(self._root, self._overlay_view_model)

        if self._config_view_model.autoconnect.get():
            self._root.after(0, self.onConnect)

        self._root.focus_force()
        async_mainloop(self._root)


if __name__ == "__main__":
    app = MainApp()
    app.run()
