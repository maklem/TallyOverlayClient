import sys
import tkinter as tk

from typing import Generator

import pytest

from tallyoverlayclient.models import AppDataModel
from tallyoverlayclient.ui import ConfigFrame, ConfigFrameViewModel, OverlayWindow, OverlayWindowViewModel


def tk_is_available() -> bool:
    try:
        tk.Tk().quit()
        return True
    except tk.TclError:
        return False


@pytest.fixture
def tk_root() -> Generator[tk.Tk, None, None]:
    root = tk.Tk()
    yield root
    root.quit()


@pytest.mark.skipif(not tk_is_available(), reason="Tkinter is not available")
def test_createConfigFrame(tk_root: tk.Tk) -> None:
    view_model = ConfigFrameViewModel(AppDataModel())
    frame = ConfigFrame(tk_root, view_model)
    assert frame is not None


@pytest.mark.skipif(not tk_is_available(), reason="Tkinter is not available")
@pytest.mark.skipif(
    sys.platform != "win32", reason="Overlay window uses Windows specific APIs"
)
def test_createOverlayWindow(tk_root: tk.Tk) -> None:
    view_model = OverlayWindowViewModel(AppDataModel())
    overlay = OverlayWindow(tk_root, view_model)
    assert overlay is not None
