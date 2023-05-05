from django.urls import path
from rest_framework.routers import SimpleRouter

from apis.views import ProductViewSet

router = SimpleRouter()
router.register("", ProductViewSet, basename="products")

urlpatterns = router.urls