from rest_framework.routers import DefaultRouter


from borrowing.views import BorrowingViewSet


router = DefaultRouter()
router.register("", BorrowingViewSet)

app_name = "borrowing"
