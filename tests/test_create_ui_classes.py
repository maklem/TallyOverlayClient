import tkinter as tk
import pytest

from tallyoverlayclient.models import AppDataModel
from tallyoverlayclient.ui import ConfigFrame, ConfigFrameViewModel, OverlayWindow, OverlayWindowViewModel


def can_use_tcl() -> bool:
    try:
        tk.Tk().destroy()
        return True
    except tk.TclError:
        return False


@pytest.mark.skipif(not can_use_tcl(), reason="Cannot use TCL")
def test_createConfigFrame() -> None:
    root = tk.Tk()
    view_model = ConfigFrameViewModel(AppDataModel())
    frame = ConfigFrame(root, view_model)
    assert frame is not None


@pytest.mark.skipif(not can_use_tcl(), reason="Cannot use TCL")
def test_createOverlayWindow() -> None:
    root = tk.Tk()
    view_model = OverlayWindowViewModel(AppDataModel())
    overlay = OverlayWindow(root, view_model)
    assert overlay is not None
