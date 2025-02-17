from typing import Optional, Callable, Any

import socketio

from tallyoverlayclient.models import TallyState, Configuration


class TallyClient:
    def __init__(
        self,
        onStateChange: Optional[Callable[[TallyState], None]] = None
    ):
        self.config = Configuration("", 0, "")
        self.bus_options: list[dict[str, Any]] = []
        self.onStateChange = onStateChange
        self.client = socketio.AsyncClient()

        @self.client.on('connect')
        async def onConnected() -> None:
            await self.client.emit(
                "listenerclient_connect",
                {
                    "deviceId": self.config.device_id,
                    "listenerType": "TallyOverlayClient",
                    "canBeReassigned": False,
                    "canBeFlashed": False,
                    "supportsChat": False,
                },
            )

        @self.client.on('bus_options')
        async def onBusOptions(data: list[dict[str, Any]]) -> None:
            self.bus_options = data
            print(data)

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

    async def connect(self, config: Configuration) -> None:
        if self.client.connected:
            raise Exception("Already connected!")

        self.config = config
        url = f"http://{config.tally_ip}:{config.tally_port}/"
        await self.client.connect(url)
