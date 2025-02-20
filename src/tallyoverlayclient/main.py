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
may_autoconnect = True


def onTallyConnected() -> None:
    tally_connection.set(AppStage.CONNECTED)

    if tally_autoconnect.get() and may_autoconnect:
        attach()
        hide()


def onDevicesChanged(devices: list[dict[str, Any]]) -> None:
    tally_devices.set([f"{d['id']} - {d['name']}" for d in devices])


def onStateChanged(state: TallyState) -> None:
    print("new state: ", state.name)
    overlay.setStatus(state)


def onTallyDisconnected() -> None:
    tally_connection.set(AppStage.DISCONNECTED)
    global may_autoconnect
    may_autoconnect = False


def save() -> None:
    config = Configuration(
        tally_ip=tally_hostname.get(),
        tally_port=tally_port.get(),
        device_id=tally_deviceid.get(),
        autoconnect=tally_autoconnect.get(),
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
    asyncio.create_task(tallyClient.connect(hostname=tally_hostname.get(), port=tally_port.get()))


def hide() -> None:
    root.iconify()


tallyClient = TallyClient(
    onStateChange=onStateChanged,
    onConnected=onTallyConnected,
    onDisconnected=onTallyDisconnected,
    onDevicesChanged=onDevicesChanged
)

root = tkinter.Tk()
tally_autoconnect = Property[bool](value=False)
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
    onHide=hide,
    onQuit=root.destroy,
    server=tally_hostname,
    port=tally_port,
    devices=tally_devices,
    device_id=tally_deviceid,
    autoconnect=tally_autoconnect,
    appstage=tally_connection,
)
overlay = ui.OverlayWindow(root)

if os.path.isfile(CONFIG_FILENAME):
    with open(CONFIG_FILENAME, "r") as f:
        config = Configuration.from_json(f.read())
        tally_hostname.set(config.tally_ip)
        tally_port.set(config.tally_port)
        tally_deviceid.set(config.device_id)
        tally_autoconnect.set(config.autoconnect)


if tally_autoconnect.get():
    root.after(0, connect)

root.focus_force()
async_mainloop(root)
