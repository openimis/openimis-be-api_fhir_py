# openIMIS Backend FHIR API reference module

| Note |
| --- |
|This repository currently supports basic functionality of FHIR API and might miss some openIMIS specific validations. Please use it with caution if you want to connect it to a production database.|

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

[![Maintainability](https://img.shields.io/codeclimate/maintainability/openimis/openimis-be-api_fhir_py.svg)](https://codeclimate.com/github/openimis/openimis-be-api_fhir_py/maintainability)
[![Test Coverage](https://img.shields.io/codeclimate/coverage/openimis/openimis-be-api_fhir_py.svg)](https://codeclimate.com/github/openimis/openimis-be-api_fhir_py)

## Description
This repository holds the files of the openIMIS Backend FHIR API reference module. 
It is dedicated to be deployed as a module of [openimis-be_py](https://github.com/openimis/openimis-be_py).

The module is mapping objects between openIMIS and FHIR representation, 
and allows external applications to use HL7 FHIR standardised communication protocol 
when interacting with openIMIS.

## Documentation
The documentation for this module can be found at [openIMIS Wiki page](https://openimis.atlassian.net/wiki/spaces/OP/pages/868417563).

## Implementation setup
This module is published on Python Package Index as [openimis-be-api-fhir](https://pypi.org/project/openimis-be-api-fhir).

The FHIR API will be available after the module is deployed on [openimis-be_py](https://github.com/openimis/openimis-be_py). 
Check the [openimis-be_py](https://github.com/openimis/openimis-be_py)'s readme file on how to activate the module 
(add the 'api_fhir' module to [openimis.json](https://github.com/openimis/openimis-be_py/blob/master/openimis.json)) 
and start the openIMIS backend. 

## Configurations Options
| Configuration key                              | Description                                                                              | Default value                                                                                                                                                                                                                                                                                                                                                                              |
|------------------------------------------------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| default_audit_user_id                          | default value which will be used for 'audit_user_id' field                               | "default_audit_user_id": 1                                                                                                                                                                                                                                                                                                                                                                 |
| gender_codes                                   | configuration of codes used by the openIMIS to represent gender (male, female, other)    | "gender_codes": {     "male": "M",     "female": "F",     "other": "O" }                                                                                                                                                                                                                                                                                                                   |
| stu3_fhir_identifier_type_config               | configuration of system and codes used to represent the specific types of identifiers    | "stu3_fhir_identifier_type_config":{    "system":"https://hl7.org/fhir/valueset-identifier-type.html",    "fhir_code_for_imis_db_id_type":"ACSN",    "fhir_code_for_imis_chfid_type":"SB",    "fhir_code_for_imis_passport_type":"PPN",    "fhir_code_for_imis_facility_id_type":"FI",    "fhir_code_for_imis_claim_admin_code_type":"FILL",    "fhir_code_for_imis_claim_code_type":"MR"} |
| stu3_fhir_marital_status_config                | configuration of system and codes used to represent the specific types of marital status | "stu3_fhir_marital_status_config":{    "system":"https://www.hl7.org/fhir/STU3/valueset-marital-status.html",    "fhir_code_for_married":"M",    "fhir_code_for_never_married":"S","fhir_code_for_divorced":"D","fhir_code_for_widowed":"W","fhir_code_for_unknown":"U"},                                                                                                                  |
| default_value_of_patient_head_attribute        | default value for 'head' attribute used for creating new Insuree object                  | "default_value_of_patient_head_attribute": False,                                                                                                                                                                                                                                                                                                                                          |
| default_value_of_patient_card_issued_attribute | default value for 'card_issued' attribute used for creating new Insuree object           | "default_value_of_patient_card_issued_attribute": False,                                                                                                                                                                                                                                                                                                                                   |

## Example of usage
To fetch information about all openIMIS Insurees (as FHIR Patients), send a  **GET** request on:
```bash
http://127.0.0.1:8000/api_fhir/Patient/
```
`127.0.0.1:8000` is the server address (if run on your local host).

Example of response ([mapping description](https://openimis.atlassian.net/wiki/spaces/OP/pages/929562664)):
```json
{
    "resourceType": "Bundle",
    "entry": [
        {
            "fullUrl": "http://127.0.0.1:8000/api_fhir/Patient/1D464C09-5334-407F-9882-14C097B89BBD",
            "resource": {
                "resourceType": "Patient",
                "address": [
                    {
                        "text": "address",
                        "type": "physical",
                        "use": "home"
                    },
                    {
                        "text": "geolocation",
                        "type": "both",
                        "use": "home"
                    }
                ],
                "birthDate": "2000-01-02",
                "gender": "female",
                "id": "1D464C09-5334-407F-9882-14C097B89BBD",
                "identifier": [
                    {
                        "type": {
                            "coding": [
                                {
                                    "code": "ACSN",
                                    "system": "https://hl7.org/fhir/valueset-identifier-type.html"
                                }
                            ]
                        },
                        "use": "usual",
                        "value": "1D464C09-5334-407F-9882-14C097B89BBD"
                    },
                    {
                        "type": {
                            "coding": [
                                {
                                    "code": "SB",
                                    "system": "https://hl7.org/fhir/valueset-identifier-type.html"
                                }
                            ]
                        },
                        "use": "usual",
                        "value": "Insuree ID (e.g. 123456789)"
                    },
                    {
                        "type": {
                            "coding": [
                                {
                                    "code": "PPN",
                                    "system": "https://hl7.org/fhir/valueset-identifier-type.html"
                                }
                            ]
                        },
                        "use": "usual",
                        "value": "passport number"
                    }
                ],
                "maritalStatus": {
                    "coding": [
                        {
                            "code": "U",
                            "system": "https://www.hl7.org/fhir/STU3/valueset-marital-status.html"
                        }
                    ]
                },
                "name": [
                    {
                        "family": "test patient",
                        "given": [
                            "test patient"
                        ],
                        "use": "usual"
                    }
                ],
                "telecom": [
                    {
                        "system": "phone",
                        "use": "home",
                        "value": "phone number"
                    },
                    {
                        "system": "email",
                        "use": "home",
                        "value": "email@email.com"
                    }
                ]
            }
        }
    ],
    "link": [
        {
            "relation": "self",
            "url": "http://127.0.0.1:8000/api_fhir/Patient/?_count=2"
        },
        {
            "relation": "next",
            "url": "http://127.0.0.1:8000/api_fhir/Patient/?_count=2&amp;page-offset=2"
        }
    ],
    "total": 9,
    "type": "searchset"
}
```

#Dependencies:
All required dependencies can be found in the [setup.py](https://github.com/openimis/openimis-be-claim_py/blob/master/setup.py) file.
