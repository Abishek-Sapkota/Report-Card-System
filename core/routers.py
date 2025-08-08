from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    StudentModelViewSet, SubjectModelViewSet, ReportCardModelViewSet, MarkModelViewSet
)

router = DefaultRouter()
router.register(r"students", StudentModelViewSet, basename="student")
router.register(r"subjects", SubjectModelViewSet, basename="subject")
router.register(r"report-cards", ReportCardModelViewSet, basename="report-card")
router.register(r"marks", MarkModelViewSet, basename="mark")

urlpatterns = [
    path("", include(router.urls)),
]