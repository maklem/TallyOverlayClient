import os
import asyncio
import tkinter
import tkinter.ttk

from async_tkinter_loop import async_mainloop

from tallyoverlayclient import ui
from tallyoverlayclient.models import Configuration, TallyState, AppStage, AppStageVar
from tallyoverlayclient.data import TallyClient

CONFIG_FILENAME = "config.json"


def onStateChange(state: TallyState) -> None:
    overlay.setStatus(state)


def onTallyConnected() -> None:
    tally_connection.set(AppStage.CONNECTED)


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


def connect() -> None:
    tally_connection.set(AppStage.CONNECTING)
    asyncio.create_task(tallyClient.connect(config))


tallyClient = TallyClient(
    onStateChange=onStateChange,
    onConnected=onTallyConnected,
    onDisconnected=onTallyDisconnected,
)

root = tkinter.Tk()
tally_connection = AppStageVar()
tally_hostname = tkinter.StringVar(master=root, value="localhost")
tally_port = tkinter.IntVar(master=root)
tally_deviceid = tkinter.StringVar(master=root)

configWindow = ui.ConfigFrame(
    root=root,
    onSave=save,
    onConnect=connect,
    onQuit=root.destroy,
    server=tally_hostname,
    port=tally_port,
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
