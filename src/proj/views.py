from rest_framework.viewsets import ModelViewSet

from .models import Member, Subscription
from .serializers import MemberSerializer, SubscriptionSerializer


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
