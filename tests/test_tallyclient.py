import pytest
import socketio
from unittest.mock import AsyncMock, MagicMock
from typing import Any

from tallyoverlayclient.data import TallyClient
from tallyoverlayclient.models import TallyState


def fake_event(client: socketio.AsyncClient, name: str, *args: Any) -> None:
    client.handlers['/'][name](*args)


@pytest.mark.asyncio
async def test_onConnect_requestsDevices() -> None:
    onConnected = MagicMock()
    sio = socketio.AsyncClient()
    tally_client = TallyClient(client=sio, onConnected=onConnected)  # noqa: F841
    sio.emit = AsyncMock()  # type: ignore

    fake_event(sio, 'connect')

    sio.emit.assert_called_once_with("devices")


@pytest.mark.asyncio
async def test_onConnect_emitsEvent() -> None:
    onConnected = MagicMock()
    sio = socketio.AsyncClient()
    tally_client = TallyClient(client=sio, onConnected=onConnected)  # noqa: F841

    fake_event(sio, 'connect')

    onConnected.assert_called_once()


def test_onDisconnect_emitsEvent() -> None:
    onDisconnected = MagicMock()
    sio = socketio.AsyncClient()
    tally_client = TallyClient(client=sio, onDisconnected=onDisconnected)  # noqa: F841

    fake_event(sio, 'disconnect', "reason")

    onDisconnected.assert_called_once()


def test_onDevices_emitsEvent() -> None:
    onDevicesChanged = MagicMock()
    sio = socketio.AsyncClient()
    tally_client = TallyClient(client=sio, onDevicesChanged=onDevicesChanged)  # noqa: F841
    devices = [{"id": "device1", "name": "Device 1"}]

    fake_event(sio, 'devices', devices)

    onDevicesChanged.assert_called_once_with(devices)


def test_withBusOptionsSet_onDeviceStates_emitsStateProgram() -> None:
    onStateChange = MagicMock()
    sio = socketio.AsyncClient()
    tally_client = TallyClient(client=sio, onStateChange=onStateChange)  # noqa: F841

    fake_event(sio, 'bus_options', [{"id": "bus1", "type": "program", "priority": 1}])
    fake_event(sio, 'device_states', [{"busId": "bus1", "sources": ["source1"]}])

    onStateChange.assert_called_once_with(TallyState.PROGRAM)


def test_withBusOptionsUnset_onDeviceStates_emitsStateOffline() -> None:
    onStateChange = MagicMock()
    sio = socketio.AsyncClient()
    tally_client = TallyClient(client=sio, onStateChange=onStateChange)  # noqa: F841

    fake_event(sio, 'bus_options', [])
    fake_event(sio, 'device_states', [{"busId": "bus1", "sources": ["source1"]}])

    onStateChange.assert_called_once_with(TallyState.OFFLINE)


def test_withEmptyDeviceStates_onDeviceStates_emitsStateOffline() -> None:
    onStateChange = MagicMock()
    tally_client = TallyClient(onStateChange=onStateChange)  # noqa: F841

    tally_client._on_bus_options([{"id": "bus1", "type": "program", "priority": 1}])
    tally_client._on_device_states([])

    onStateChange.assert_called_once_with(TallyState.OFFLINE)
