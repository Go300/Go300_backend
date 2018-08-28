from django.conf.urls import include, url
from rest_framework import routers

from .views import MemberViewSet, SubscriptionViewSet

router = routers.DefaultRouter()
router.register('members', MemberViewSet, base_name='members-viewset')
router.register('subscriptions', SubscriptionViewSet, base_name='subscriptions-viewset')

urlpatterns = [
    url(r'', include(router.urls)),
]
