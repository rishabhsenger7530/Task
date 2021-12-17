from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Codes import views


router = DefaultRouter()
router.register(r'create-user', views.CreateUserView),
router.register(r'code-type', views.CreateCodeType)
router.register(r'plans', views.CreateCodeType)


# urlpatterns = [
#     path('vouchers/apply/',views.VouchersApply.as_view(), name = "vouchers-apply"),
# ]
urlpatterns = router.urls