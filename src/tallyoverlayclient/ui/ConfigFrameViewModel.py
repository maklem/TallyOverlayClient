from typing import Callable, Optional

from tallyoverlayclient.models import AppDataModel


def do_nothing() -> None:
    print("Doing nothing")
    pass


class ConfigFrameViewModel:
    def __init__(
        self,
        model: AppDataModel,
        onSave: Optional[Callable[[], None]] = None,
        onConnect: Optional[Callable[[], None]] = None,
        onAttach: Optional[Callable[[], None]] = None,
        onHide: Optional[Callable[[], None]] = None,
        onQuit: Optional[Callable[[], None]] = None,
    ) -> None:
        self.onSave = onSave or do_nothing
        self.onConnect = onConnect or do_nothing
        self.onAttach = onAttach or do_nothing
        self.onHide = onHide or do_nothing
        self.onQuit = onQuit or do_nothing

        self.server = model.server
        self.port = model.port
        self.device_id = model.device_id
        self.autoconnect = model.autoconnect

        self.devices = model.devices
        self.connection_state = model.connection_state
        self.visible = model.visible
