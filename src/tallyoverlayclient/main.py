import os
import asyncio
import tkinter

from async_tkinter_loop import async_mainloop

from tallyoverlayclient import ui
from tallyoverlayclient.models import Configuration, TallyState
from tallyoverlayclient.data import TallyClient

CONFIG_FILENAME = "config.json"


def onStateChange(state: TallyState) -> None:
    print("Setting state:", state.name)
    overlay.setStatus(state)


def save(config: Configuration) -> None:
    with open(CONFIG_FILENAME, "w") as f:
        f.write(config.to_json())


def connect(config: Configuration) -> None:
    asyncio.create_task(tallyClient.connect(config))


tallyClient = TallyClient(
    onStateChange=onStateChange
)

root = tkinter.Tk()
configWindow = ui.ConfigFrame(
    root=root,
    onSave=save,
    onConnect=connect,
    onQuit=root.destroy,
)
overlay = ui.OverlayWindow(root)

if os.path.isfile(CONFIG_FILENAME):
    with open(CONFIG_FILENAME, "r") as f:
        config = Configuration.from_json(f.read())
    configWindow.load(config)

root.focus_force()
async_mainloop(root)
