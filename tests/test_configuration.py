from tallyoverlayclient.models import Configuration


def test_configuration_readsJson() -> None:
    data = '{"tally_ip": "localhost", "tally_port": 4455, "device_id": "dev", "autoconnect": true}'
    config = Configuration.from_json(data)

    assert config.tally_ip == "localhost"
    assert config.tally_port == 4455
    assert config.device_id == "dev"
    assert config.autoconnect is True


def test_configuration_generatesJsonString() -> None:
    config = Configuration(
        tally_ip="ip",
        tally_port=1234,
        device_id="dev",
        autoconnect=True,
    )
    data = config.to_json()

    assert data == '{"tally_ip": "ip", "tally_port": 1234, "device_id": "dev", "autoconnect": true}'
