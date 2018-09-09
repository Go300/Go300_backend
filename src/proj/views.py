from push_notifications.models import GCMDevice
from rest_framework.viewsets import ModelViewSet

from .models import Member, Subscription, Confirmation
from .serializers import MemberSerializer, SubscriptionSerializer, DeviceSerializer, ConfirmationSerializer


class MemberViewSet(ModelViewSet):
    class Meta:
        model = Member

    serializer_class = MemberSerializer
    queryset = Member.objects.all()


class SubscriptionViewSet(ModelViewSet):
    class Meta:
        model = Subscription

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class DeviceViewSet(ModelViewSet):
    class Meta:
        model = GCMDevice

    serializer_class = DeviceSerializer
    queryset = GCMDevice.objects.all()


class ConfirmationViewSet(ModelViewSet):
    class Meta:
        model = Confirmation

    serializer_class = ConfirmationSerializer
    queryset = Confirmation.objects.all()
