import tkinter as tk
from typing import Generator
import pytest
from tallyoverlayclient.models import Property


@pytest.fixture
def tcl() -> Generator[tk.Tk, None, None]:
    tcl = tk.Tcl()
    yield tcl
    tcl.quit()


def test_whenPropertyChanges_boundVariableUpdates(tcl: tk.Tk) -> None:
    property = Property[str]("test")
    bound_variable = property.bind_to_tkinter(tk.StringVar(master=tcl))
    assert bound_variable.get() == "test"

    property.set("new value")
    assert bound_variable.get() == "new value"


def test_whenVariableChanges_propertyIsUpdated(tcl: tk.Tk) -> None:
    property = Property[str]("test")
    bound_variable = property.bind_to_tkinter(tk.StringVar(master=tcl))

    bound_variable.set("new value")
    assert property.get() == "new value"
