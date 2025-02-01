from django.urls import path, include
from rest_framework.routers import DefaultRouter

from customer.views import UserViewSet

router = DefaultRouter()
router.register("", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "customer"
