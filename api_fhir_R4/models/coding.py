from api_fhir_R4.models import Element, Property


class Coding(Element):

    system = Property('system', str)
    version = Property('version', str)
    code = Property('code', str)
    display = Property('display', str)
    userSelected = Property('userSelected', bool)
