from typing import Optional, Callable, Any
import asyncio
import socketio

from tallyoverlayclient.models import TallyState


class TallyClient:
    def __init__(
        self,
        onStateChange: Optional[Callable[[TallyState], None]] = None,
        onDevicesChanged: Optional[Callable[[list[dict[str, Any]]], None]] = None,
        onConnected: Optional[Callable[[], None]] = None,
        onDisconnected: Optional[Callable[[], None]] = None,
    ):
        self.devices: list[dict[str, Any]] = []
        self.bus_options: list[dict[str, Any]] = []
        self.onStateChange = onStateChange
        self.onConnected = onConnected
        self.onDisconnected = onDisconnected
        self.onDevicesChanged = onDevicesChanged
        self.client = socketio.AsyncClient()

        self.client.on('connect', self._on_connect)
        self.client.on('connect_error', self._on_connect_error)
        self.client.on('disconnect', self._on_disconnect)

        self.client.on('bus_options', self._on_bus_options)
        self.client.on('devices', self._on_devices)
        self.client.on('device_states', self._on_device_states)

    def _on_connect(self) -> None:
        if self.onConnected is not None:
            self.onConnected()
        asyncio.create_task(self.client.emit("devices"))

    def _on_connect_error(self, data: str) -> None:
        if self.onDisconnected is not None:
            self.onDisconnected()

    def _on_disconnect(self, reason: str) -> None:
        if self.onDisconnected is not None:
            self.onDisconnected()

    def _on_devices(self, data: list[dict[str, Any]]) -> None:
        self.devices = data
        if self.onDevicesChanged is not None:
            self.onDevicesChanged(self.devices)

    def _on_bus_options(self, data: list[dict[str, Any]]) -> None:
        self.bus_options = data

    def _on_device_states(self, data: list[dict[str, Any]]) -> None:
        if self.onStateChange is None:
            return

        active_busses = []
        for device in data:
            if len(device["sources"]) == 0:
                continue
            bus = [bus for bus in self.bus_options if bus["id"] == device["busId"]]
            if len(bus) == 1:
                active_busses.append(bus[0])
        if len(active_busses) == 0:
            self.onStateChange(TallyState.OFFLINE)
            return

        active_busses.sort(key=lambda x: x["priority"])
        match active_busses[0]["type"]:
            case "program":
                self.onStateChange(TallyState.PROGRAM)
            case "preview":
                self.onStateChange(TallyState.PREVIEW)
            case "aux":
                self.onStateChange(TallyState.AUX)
            case _:
                self.onStateChange(TallyState.OFFLINE)

    async def connect(self, hostname: str, port: int) -> None:
        if self.client.connected:
            raise Exception("Already connected!")

        url = f"http://{hostname}:{port}/"
        try:
            await self.client.connect(url)
        except socketio.exceptions.ConnectionError:
            # event connect_error is emitted implicitly
            pass

    async def attach_to_device(self, device_id: str) -> None:
        await self.client.emit(
            "listenerclient_connect",
            {
                "deviceId": device_id,
                "listenerType": "TallyOverlayClient",
                "canBeReassigned": False,
                "canBeFlashed": False,
                "supportsChat": False,
            },
        )
