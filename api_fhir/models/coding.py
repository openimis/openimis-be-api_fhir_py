from api_fhir.models import Element, Property


class Coding(Element):

    code = Property('code', str)
    display = Property('display', str)
    system = Property('system', str)
    userSelected = Property('userSelected', bool)
    version = Property('version', str)
