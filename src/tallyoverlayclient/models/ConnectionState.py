from enum import Enum


class ConnectionState(Enum):
    DISCONNECTED = "disconnected",
    CONNECTING = "connecting",
    CONNECTED = "connected",
    LISTENING = "listening",
