from typing import Optional, Callable, Any

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

        @self.client.event
        async def connect() -> None:
            if self.onConnected is not None:
                self.onConnected()
            await self.client.emit("devices")

        @self.client.event
        async def connect_error(data: str) -> None:
            if self.onDisconnected is not None:
                self.onDisconnected()

        @self.client.event
        async def disconnect(reason: str) -> None:
            if self.onDisconnected is not None:
                self.onDisconnected()

        @self.client.on('devices')
        async def onDevices(data: list[dict[str, Any]]) -> None:
            self.devices = data
            print(data)
            if self.onDevicesChanged is not None:
                self.onDevicesChanged(self.devices)

        @self.client.on('bus_options')
        async def onBusOptions(data: list[dict[str, Any]]) -> None:
            self.bus_options = data

        @self.client.on('device_states')
        async def onDeviceStates(data: list[dict[str, Any]]) -> None:
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
