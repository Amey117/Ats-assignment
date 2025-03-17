from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from .views import Applicants,ATSHome

router = routers.DefaultRouter()

router.register(prefix="ats", viewset=ATSHome, basename="home")
router.register(prefix="applicants", viewset=Applicants, basename="applicant")

urlpatterns = [
        path("", include(router.urls)),
]