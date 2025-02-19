from enum import Enum


class AppStage(Enum):
    DISCONNECTED = "disconnected",
    CONNECTING = "connecting",
    CONNECTED = "connected",
    LISTENING = "listening",
