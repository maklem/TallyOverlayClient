import tkinter as tk
from tallyoverlayclient.models import Property


def test_whenPropertyChanges_boundVariableUpdates() -> None:
    property = Property[str]("test")
    bound_variable = property.bind_to_tkinter(tk.StringVar())
    assert bound_variable.get() == "test"

    property.set("new value")
    assert bound_variable.get() == "new value"


def test_whenVariableChanges_propertyIsUpdated() -> None:
    property = Property[str]("test")
    bound_variable = property.bind_to_tkinter(tk.StringVar())

    bound_variable.set("new value")
    assert property.get() == "new value"
