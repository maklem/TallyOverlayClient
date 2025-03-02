import tkinter as tk
import pytest

from tallyoverlayclient.models import AppDataModel
from tallyoverlayclient.ui import ConfigFrame, ConfigFrameViewModel, OverlayWindow, OverlayWindowViewModel


def test_createConfigFrame() -> None:
    root = tk.Tcl()
    view_model = ConfigFrameViewModel(AppDataModel())
    frame = ConfigFrame(root, view_model)
    assert frame is not None


def test_createOverlayWindow() -> None:
    root = tk.Tcl()
    view_model = OverlayWindowViewModel(AppDataModel())
    overlay = OverlayWindow(root, view_model)
    assert overlay is not None
