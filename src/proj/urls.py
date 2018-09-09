from django.conf.urls import include, url
from rest_framework import routers

from .views import MemberViewSet, SubscriptionViewSet, DeviceViewSet, ConfirmationViewSet

router = routers.DefaultRouter()
router.register('members', MemberViewSet, base_name='members-viewset')
router.register('subscriptions', SubscriptionViewSet, base_name='subscriptions-viewset')
router.register('devices', DeviceViewSet, base_name='devices-viewset')
router.register('confirmations', ConfirmationViewSet, base_name='confirmations-viewset')

urlpatterns = [
    url(r'', include(router.urls)),
]
