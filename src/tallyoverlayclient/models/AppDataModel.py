from .Property import Property
from .ConnectionState import ConnectionState
from .TallyState import TallyState
from .Configuration import Configuration


class AppDataModel:
    def __init__(self) -> None:
        self.server = Property[str](value="localhost")
        self.port = Property[int](value=4455)
        self.device_id = Property[str](value="")
        self.autoconnect = Property[bool](value=False)

        self.may_autoconnect = Property[bool](value=True)
        self.tally_state = Property[TallyState](value=TallyState.OFFLINE)

        self.devices = Property[list[str]](value=[])
        self.connection_state = Property[ConnectionState](value=ConnectionState.DISCONNECTED)
        self.visible = Property[bool](value=False)

    def load_config(self, filename: str) -> None:
        with open(filename, "r") as f:
            config = Configuration.from_json(f.read())
            self.server.set(config.tally_ip)
            self.port.set(config.tally_port)
            self.device_id.set(config.device_id)
            self.autoconnect.set(config.autoconnect)

    def save_config(self, filename: str) -> None:
        config = Configuration(
            tally_ip=self.server.get(),
            tally_port=self.port.get(),
            device_id=self.device_id.get(),
            autoconnect=self.autoconnect.get(),
        )

        with open(filename, "w") as f:
            f.write(config.to_json())
