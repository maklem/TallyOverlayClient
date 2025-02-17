import tkinter

from async_tkinter_loop import async_mainloop

from tallyoverlayclient import ui
from tallyoverlayclient.models import Configuration


def save(config: Configuration) -> None:
    overlay.setStatus(ui.OverlayState.AUX)


def connect(config: Configuration) -> None:
    overlay.setStatus(ui.OverlayState.PROGRAM)


root = tkinter.Tk()
configWindow = ui.ConfigFrame(
    root=root,
    onSave=save,
    onConnect=connect,
    onQuit=root.destroy,
)
overlay = ui.OverlayFrame(root)

root.focus_force()
async_mainloop(root)
