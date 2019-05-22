import copy

from core.datetimes.ad_datetime import datetime
from insuree.models import Insuree

from api_fhir.models import Patient, HumanName, Identifier, CodeableConcept
from api_fhir.serializers import BaseFHIRConverter, BaseFHIRSerializer

class ConverterInsuree(BaseFHIRConverter):
    @classmethod
    def toFhirObj(cls, imisInsuree):
        fhirPatient = Patient()
        cls.buildHumanNames(fhirPatient, imisInsuree)
        cls.buildFhirIdentifiers(fhirPatient, imisInsuree)
        return fhirPatient

    @classmethod
    def toImisObj(cls, fhirPatient):
        imisInsuree = Insuree()
        cls.buildImisNames(imisInsuree, fhirPatient)
        imisInsuree.dob = datetime.now()  # TODO can't be null (validate)
        imisInsuree.validity_from = datetime.now()  # TODO can't be null (validate)
        imisInsuree.validity_to = datetime.now()  # TODO can't be null (validate)
        imisInsuree.audit_user_id = 1  # TODO can't be null (validate)
        return imisInsuree

    @classmethod
    def buildHumanNames(cls, fhirPatient, imisInsuree):
        # last name
        name = HumanName()
        name.use = "usual"  # TODO add to constants
        name.family = imisInsuree.last_name
        name.given = [imisInsuree.other_names]
        fhirPatient.name = [name.__dict__]

    @classmethod
    def buildImisNames(cls, imisInsuree, fhirPatient):
        # assert fhirPatient.name is not None, '.validate() should return the validated data' # TODO remove
        for name in fhirPatient['name']:
            if name['use'] == "usual":
                imisInsuree.last_name = name['family']
                imisInsuree.other_names = name['given'][0]  # TODO verify if exists
                break

    @classmethod
    def buildFhirIdentifiers(cls, fhirPatient, imisInsuree):
        identifiers = []
        #InsureeID
        identifier = Identifier()
        identifier.use = "usual"  # TODO add constant
        code = CodeableConcept()  # TODO move to separate method
        code.system = "specify"  # TODO need to be specified
        code.code = "specify"
        identifier.type = code.__dict__
        identifier.value = imisInsuree.id
        identifiers.append(identifier.__dict__)

        # CHFID
        identifier = Identifier()
        identifier.use = "usual"  # TODO add constant
        code = CodeableConcept()  # TODO move to separate method
        code.system = "specify2"  # TODO need to be specified
        code.code = "specify2"
        identifier.type = code.__dict__
        identifier.value = imisInsuree.chf_id
        identifiers.append(identifier.__dict__)

        # passport
        identifier = Identifier()
        identifier.use = "usual"  # TODO add constant
        code = CodeableConcept()  # TODO move to separate method
        code.system = "specify3"  # TODO need to be specified
        code.code = "specify3"  # TODO TypeOfId need to be used
        identifier.type = code.__dict__
        identifier.value = imisInsuree.passport
        identifiers.append(identifier.__dict__)

        fhirPatient.identifier = identifiers

    @classmethod
    def buildImisIdentifiers(cls, imisInsuree, fhirPatient):
        # TODO validate if fhirPatient.identifier not null
        for identifier in fhirPatient['identifier']:
            pass


class PatientSerializer(BaseFHIRSerializer):
    fhirConverter = ConverterInsuree()

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return Insuree.objects.create(**copied_data)

    def update(self, instance, validated_data):
        pass

    class Meta:
        app_label = 'api_fhir'
