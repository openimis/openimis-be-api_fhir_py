from api_fhir_R4.models import Element, Property


class ContactDetail(Element):

    name = Property('name', str)
    telecom = Property('telecom', 'ContactPoint', count_max='*')
