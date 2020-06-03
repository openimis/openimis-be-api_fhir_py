from api_fhir_R4.models import Element, Property


class Period(Element):

    end = Property('end', 'FHIRDate')
    start = Property('start', 'FHIRDate')
