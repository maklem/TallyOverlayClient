from dataclasses import dataclass


@dataclass
class Configuration:
    tally_ip: str
    tally_port: int
    device_id: str
