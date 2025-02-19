from tkinter import Variable
from typing import Any, Optional


from .AppStage import AppStage


class AppStageVar(Variable):
    def __init__(
        self,
        master: Any = None,
        value: Optional[AppStage] = None,
        name: Optional[str] = None,
    ):
        value = value or AppStage.DISCONNECTED
        super().__init__(master=master, value=value.value, name=name)

    def set(self, value: AppStage) -> None:
        super().set(value.value)

    def get(self) -> AppStage:
        return AppStage(super().get())
