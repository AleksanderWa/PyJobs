from rest_framework import routers
from .views import JobsViewSet

router = routers.DefaultRouter()
router.register(
    r'jobs', JobsViewSet, basename='jobs'
)

urlpatterns = router.urls