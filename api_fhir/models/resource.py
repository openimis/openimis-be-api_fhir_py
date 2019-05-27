class Resource(object):
    def __init__(self):
        self.id = None  # Type `str` (id)

        self.meta = None  # Type `Meta`

        self.implicitRules = None  # Type `str`

        self.language = None  # Type `str` (code)

    class Meta:
        app_label = 'api_fhir'
