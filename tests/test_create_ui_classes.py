import tkinter as tk

from tallyoverlayclient.models import AppDataModel
from tallyoverlayclient.ui import ConfigFrame, ConfigFrameViewModel, OverlayWindow, OverlayWindowViewModel


def test_createConfigFrame() -> None:
    root = tk.Tk()
    view_model = ConfigFrameViewModel(AppDataModel())
    frame = ConfigFrame(root, view_model)
    assert frame is not None


def test_createOverlayWindow() -> None:
    root = tk.Tk()
    view_model = OverlayWindowViewModel(AppDataModel())
    overlay = OverlayWindow(root, view_model)
    assert overlay is not None
