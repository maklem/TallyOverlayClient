import tkinter as tk
import pytest
from tallyoverlayclient.models import Property


def can_use_ui() -> bool:
    try:
        tk.Tk().destroy()
        return True
    except tk.TclError:
        return False


@pytest.mark.skipif(not can_use_ui(), reason="Cannot use UI")
def test_whenPropertyChanges_boundVariableUpdates() -> None:
    property = Property[str]("test")
    bound_variable = property.bind_to_tkinter(tk.StringVar())
    assert bound_variable.get() == "test"

    property.set("new value")
    assert bound_variable.get() == "new value"


@pytest.mark.skipif(not can_use_ui(), reason="Cannot use UI")
def test_whenVariableChanges_propertyIsUpdated() -> None:
    property = Property[str]("test")
    bound_variable = property.bind_to_tkinter(tk.StringVar())

    bound_variable.set("new value")
    assert property.get() == "new value"
