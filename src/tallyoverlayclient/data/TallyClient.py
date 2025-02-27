from typing import Optional, Callable, Any
import asyncio
import socketio

from tallyoverlayclient.models import TallyState


def _do_nothing(*args: Any, **kwargs: Any) -> None:
    return


class TallyClient:
    def __init__(
        self,
        client: Optional[socketio.AsyncClient] = None,
        onStateChange: Optional[Callable[[TallyState], None]] = None,
        onDevicesChanged: Optional[Callable[[list[dict[str, Any]]], None]] = None,
        onConnected: Optional[Callable[[], None]] = None,
        onDisconnected: Optional[Callable[[], None]] = None,
    ):
        self._devices: list[dict[str, Any]] = []
        self._bus_options: list[dict[str, Any]] = []
        self._onStateChange = onStateChange
        self._onConnected = onConnected or _do_nothing
        self._onDisconnected = onDisconnected or _do_nothing
        self._onDevicesChanged = onDevicesChanged or _do_nothing
        self._client = client or socketio.AsyncClient()

        self._client.on('connect', self._on_connect)
        self._client.on('connect_error', self._on_connect_error)
        self._client.on('disconnect', self._on_disconnect)

        self._client.on('bus_options', self._on_bus_options)
        self._client.on('devices', self._on_devices)
        self._client.on('device_states', self._on_device_states)

    def _on_connect(self) -> None:
        if self._onConnected is not None:
            self._onConnected()
        asyncio.create_task(self._client.emit("devices"))

    def _on_connect_error(self, data: str) -> None:
        self._onDisconnected()

    def _on_disconnect(self, reason: str) -> None:
        self._onDisconnected()

    def _on_devices(self, data: list[dict[str, Any]]) -> None:
        self._devices = data
        self._onDevicesChanged(self._devices)

    def _on_bus_options(self, data: list[dict[str, Any]]) -> None:
        self._bus_options = data

    def _on_device_states(self, data: list[dict[str, Any]]) -> None:
        if self._onStateChange is None:
            return

        active_busses = []
        for device in data:
            if len(device["sources"]) == 0:
                continue
            bus = [bus for bus in self._bus_options if bus["id"] == device["busId"]]
            if len(bus) == 1:
                active_busses.append(bus[0])
        if len(active_busses) == 0:
            self._onStateChange(TallyState.OFFLINE)
            return

        active_busses.sort(key=lambda x: x["priority"])
        match active_busses[0]["type"]:
            case "program":
                self._onStateChange(TallyState.PROGRAM)
            case "preview":
                self._onStateChange(TallyState.PREVIEW)
            case "aux":
                self._onStateChange(TallyState.AUX)
            case _:
                self._onStateChange(TallyState.OFFLINE)

    async def connect(self, hostname: str, port: int) -> None:
        if self._client.connected:
            raise Exception("Already connected!")

        url = f"http://{hostname}:{port}/"
        try:
            await self._client.connect(url)
        except socketio.exceptions.ConnectionError:
            # event connect_error is emitted implicitly
            pass

    async def attach_to_device(self, device_id: str) -> None:
        await self._client.emit(
            "listenerclient_connect",
            {
                "deviceId": device_id,
                "listenerType": "TallyOverlayClient",
                "canBeReassigned": False,
                "canBeFlashed": False,
                "supportsChat": False,
            },
        )
