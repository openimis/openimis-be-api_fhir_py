from api_fhir.models.resource import Resource


class DomainResource(Resource):
    resource_type = "DomainResource"

    def __init__(self):
        self.contained = None  # List of `Resource` items (represented as `dict` in JSON).

        self.extension = None  # List of `Extension` items (represented as `dict` in JSON).

        self.modifierExtension = None  # List of `Extension` items (represented as `dict` in JSON).

        self.text = None  # Type `Narrative` (represented as `dict` in JSON).

        super(DomainResource, self).__init__()

    class Meta:
        app_label = 'api_fhir'
