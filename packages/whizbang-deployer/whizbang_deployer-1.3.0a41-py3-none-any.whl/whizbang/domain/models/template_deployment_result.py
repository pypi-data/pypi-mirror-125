from whizbang.domain.models.json_serializable import JsonSerializable


class TemplateDeploymentResult:
    def __init__(self, result_json: str):
        super().__init__()
        self.result_json = result_json

    @property
    def outputs(self): return self.result_json['properties']['outputs']