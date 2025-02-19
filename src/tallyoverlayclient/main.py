import os
import asyncio
import tkinter
import tkinter.ttk
from typing import Any

from async_tkinter_loop import async_mainloop

from tallyoverlayclient import ui
from tallyoverlayclient.models import Configuration, TallyState, AppStage, Property
from tallyoverlayclient.data import TallyClient

CONFIG_FILENAME = "config.json"


def onTallyConnected() -> None:
    tally_connection.set(AppStage.CONNECTED)


def onDevicesChanged(devices: list[dict[str, Any]]) -> None:
    tally_devices.set([f"{d['id']} - {d['name']}" for d in devices])


def onStateChanged(state: TallyState) -> None:
    print("new state: ", state.name)
    overlay.setStatus(state)


def onTallyDisconnected() -> None:
    tally_connection.set(AppStage.DISCONNECTED)


def save() -> None:
    config = Configuration(
        tally_ip=tally_hostname.get(),
        tally_port=tally_port.get(),
        device_id=tally_deviceid.get()
    )

    with open(CONFIG_FILENAME, "w") as f:
        f.write(config.to_json())


def attach() -> None:
    tally_connection.set(AppStage.LISTENING)
    device = tally_deviceid.get().split(" - ", 1)[0]
    asyncio.create_task(tallyClient.attach_to_device(device))
    pass


def connect() -> None:
    tally_connection.set(AppStage.CONNECTING)
    config = Configuration(
        tally_ip=tally_hostname.get(),
        tally_port=tally_port.get(),
        device_id=""
    )
    asyncio.create_task(tallyClient.connect(config))


tallyClient = TallyClient(
    onStateChange=onStateChanged,
    onConnected=onTallyConnected,
    onDisconnected=onTallyDisconnected,
    onDevicesChanged=onDevicesChanged
)

root = tkinter.Tk()
tally_connection = Property[AppStage](value=AppStage.DISCONNECTED)
tally_hostname = Property[str](value="localhost")
tally_port = Property[int](value=4455)
tally_devices = Property[list[str]](value=[])
tally_deviceid = Property[str](value="")

configWindow = ui.ConfigFrame(
    root=root,
    onSave=save,
    onConnect=connect,
    onAttach=attach,
    onQuit=root.destroy,
    server=tally_hostname,
    port=tally_port,
    devices=tally_devices,
    device_id=tally_deviceid,
    appstage=tally_connection,
)
overlay = ui.OverlayWindow(root)

if os.path.isfile(CONFIG_FILENAME):
    with open(CONFIG_FILENAME, "r") as f:
        config = Configuration.from_json(f.read())
        tally_hostname.set(config.tally_ip)
        tally_port.set(config.tally_port)
        tally_deviceid.set(config.device_id)


root.focus_force()
async_mainloop(root)
