# openIMIS Backend FHIR API reference module

| Note |
| --- |
|This repository currently supports basic functionality of FHIR API. This Don't use it (or even connect it) to a production database.|

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

[![Maintainability](https://img.shields.io/codeclimate/maintainability/openimis/openimis-be-api_fhir_py.svg)](https://codeclimate.com/github/openimis/openimis-be-api_fhir_py/maintainability)
[![Test Coverage](https://img.shields.io/codeclimate/coverage/openimis/openimis-be-api_fhir_py.svg)](https://codeclimate.com/github/openimis/openimis-be-api_fhir_py)

#Description
This repository holds the files of the openIMIS Backend FHIR API reference module. 
It is dedicated to be deployed as a module of [openimis-be_py](https://github.com/openimis/openimis-be_py).

The module can be used to mapping objects between OpenIMIS and FHIR representation.

##Documentation:
The documentation od this module can be found one the [OpenIMIS WIKI page](https://openimis.atlassian.net/wiki/spaces/OP/pages/868417563/The+OpenIMIS+API+FHIR+module).

#Example of usage:
The FHIR API will be available after the module will be deployed on the [openimis-be_py](https://github.com/openimis/openimis-be_py).

To fetch information about all OpenIMIS Insueree (FHIR Patient) available on server can be sent **GET** request on:
```bash
http://127.0.0.1:8000/api_fhir/Patient/
```
, where `127.0.0.1:8000` is the server address.

Examle of response ([mapping description](https://openimis.atlassian.net/wiki/spaces/OP/pages/814284864/openIMIS+tblInsuree+resource+FHIR+Patient)):
```json
{
    "resourceType": "Bundle",
    "entry": [
        {
            "fullUrl": "http://127.0.0.1:8000/api_fhir/Patient/4",
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
                "id": 4,
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
                        "value": "4"
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
                        "value": "chfid"
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
                        "value": "passport"
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
                        "value": "phoneNum"
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
