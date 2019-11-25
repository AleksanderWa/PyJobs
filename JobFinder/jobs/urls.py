from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from .views import JobsViewSet, MainPageView

router = routers.DefaultRouter()
router.register(
    r'jobs', JobsViewSet, basename='jobs'
)

urlpatterns = [
    url(r'^main/$', MainPageView.as_view()),
    url(r'^', include(router.urls))
]
