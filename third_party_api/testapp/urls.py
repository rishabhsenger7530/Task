from django.urls import path, include
from rest_framework.routers import DefaultRouter
from testapp import views


router = DefaultRouter()
router.register(r'telecom', views.CreateTelecomeView),
urlpatterns = router.urls


