from typing import Callable, TypeVar
from tkinter import Variable

T = TypeVar('T')
P = TypeVar('P', bound=Variable)


class Property[T]:
    def __init__(self, value: T):
        self._callbacks: list[Callable[[T], None]] = []
        self._value = value

    def on_change(self, callback: Callable[[T], None]) -> Callable[[T], None]:
        self._callbacks.append(callback)
        return callback

    def bind_to_tkinter(self, variable: P) -> P:
        variable.set(self._value)
        variable.trace_add('write', lambda _, _2, _3: self.set(variable.get()))
        self.on_change(lambda new: variable.set(new))
        return variable

    def _notify(self) -> None:
        for callback in self._callbacks:
            callback(self._value)

    def set(self, value: T) -> None:
        if value == self._value:
            return
        self._value = value
        self._notify()

    def get(self) -> T:
        return self._value
