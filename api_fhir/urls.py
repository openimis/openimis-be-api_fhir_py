from api_fhir import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Patient', views.InsureeViewSet, base_name="Patient")
router.register(r'Location', views.HFViewSet)
router.register(r'PractitionerRole', views.PractitionerRoleViewSet, base_name="PractitionerRole")
router.register(r'Practitioner', views.PractitionerViewSet)
router.register(r'Claim', views.ClaimViewSet)
router.register(r'ClaimResponse', views.ClaimResponseViewSet, base_name="ClaimResponse")
router.register(r'CommunicationRequest', views.CommunicationRequestViewSet)
router.register(r'EligibilityRequest', views.EligibilityRequestViewSet, base_name="EligibilityRequest")
router.register(r'Coverage', views.CoverageRequestQuerySet)

urlpatterns = [
    path('', include(router.urls)),
]
