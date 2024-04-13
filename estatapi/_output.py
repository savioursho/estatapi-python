import dataclasses

import requests


@dataclasses.dataclass
class ApiOutput:
    response: requests.Response

    def to_json(self) -> dict:
        return self.response.json()

    @property
    def root_key(self) -> str:
        return list(self.to_json().keys())[0]

    def get_result(self) -> dict:
        return self.to_json()[self.root_key]["RESULT"]

    def get_parameter(self) -> dict:
        return self.to_json()[self.root_key]["PARAMETER"]

    def get_data(self) -> dict:

        data_key = next(
            k
            for k in self.to_json()[self.root_key].keys()
            if k not in ["RESULT", "PARAMETER"]
        )
        return self.to_json()[self.root_key][data_key]
