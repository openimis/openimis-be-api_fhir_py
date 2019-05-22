class Element(object):

    resource_type = "Element"

    def __init__(self):
        self.id = None  # Type `str` (id)

        self.extension = None  # Type `Extension`

    class Meta:
        abstract = True
        app_label = 'api_fhir'
