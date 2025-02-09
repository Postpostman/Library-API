from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from payment.views import PaymentViewSet

router = DefaultRouter()
router.register("", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "payment"
