from enum import Enum


class TallyState(Enum):
    PROGRAM = "overlay.program.TFrame"
    PREVIEW = "overlay.preview.TFrame"
    AUX = "overlay.aux.TFrame"
    OFFLINE = "overlay.offline.TFrame"
