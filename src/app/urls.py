from django.conf.urls import include, url
from rest_framework import routers

from .views import MemberViewSet

router = routers.DefaultRouter()
router.register('members', MemberViewSet, base_name='members-viewset')

urlpatterns = [
    url(r'', include(router.urls)),
]
