from api_fhir_R4.models import BackboneElement, Property, DomainResource


class DosageDoseAndRate(BackboneElement):

    type = Property('type', 'CodeableConcept')
    doseRange = Property('doseRange', 'Range')
    doseSimpleQuantity = Property('doseSimpleQuantity', 'Quantity')
    rateRatio = Property('rateRatio', 'Ratio')
    rateRange = Property('rateRange', 'Range')
    rateSimpleQuantity = Property('rateSimpleQuantity', 'Quantity')


class Dosage(DomainResource):

    sequence = Property('sequence', int)
    text = Property('text', str)
    additionalInstruction = Property('additionalInstruction', 'CodeableConcept', count_max='*')
    patientInstruction = Property('patientInstruction', str)
    timing = Property('timing', 'Timing')
    asNeededBoolean = Property('asNeededBoolean', bool)
    asNeededCodeableConcept = Property('asNeededCodeableConcept', 'CodeableConcept')
    site = Property('site', 'CodeableConcept')
    route = Property('route', 'CodeableConcept')
    method = Property('method', 'CodeableConcept')
    doseAndRate = Property('doseAndRate', 'DosageDoseAndRate', count_max='*')
    maxDosePerPeriod = Property('maxDosePerPeriod', 'Ratio')
    maxDosePerAdministration = Property('maxDosePerAdministration', 'Quantity')
    maxDosePerLifetime = Property('maxDosePerLifetime', 'Quantity')