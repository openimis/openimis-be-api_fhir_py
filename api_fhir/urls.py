from api_fhir import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Patient', views.InsureeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
