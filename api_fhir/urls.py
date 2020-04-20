from api_fhir import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Patient', views.InsureeViewSet, basename="Patient")
router.register(r'Location', views.HFViewSet, basename="Location")
router.register(r'PractitionerRole', views.PractitionerRoleViewSet, basename="PractitionerRole")
router.register(r'Practitioner', views.PractitionerViewSet, basename="Practitioner")
router.register(r'Claim', views.ClaimViewSet, basename="Claim")
router.register(r'ClaimResponse', views.ClaimResponseViewSet, basename="ClaimResponse")
router.register(r'CommunicationRequest', views.CommunicationRequestViewSet, basename="CommunicationRequest")
router.register(r'EligibilityRequest', views.EligibilityRequestViewSet, basename="EligibilityRequest")
router.register(r'Coverage', views.CoverageRequestQuerySet, basename="Coverage")

urlpatterns = [
    path('', include(router.urls))
    ]
