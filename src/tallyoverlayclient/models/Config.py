from dataclasses import dataclass, asdict
import json


@dataclass
class Configuration:
    tally_ip: str
    tally_port: int
    device_id: str

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, data: str) -> 'Configuration':
        entries = json.loads(data)
        return cls(**entries)
