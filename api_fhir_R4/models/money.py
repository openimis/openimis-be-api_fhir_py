from api_fhir_R4.models import Element, Property


class Money(Element):
    value = Property('value', float)
    currency = Property('currency', str)
