from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Member, Subscription


class MemberSerializer(serializers.ModelSerializer):
    token = serializers.ReadOnlyField()
    username = serializers.CharField(required=True)

    class Meta:
        model = Member
        fields = ('username', 'token')


class SubscriptionSerializer(serializers.ModelSerializer):
    member = serializers.UUIDField(required=True, write_only=True)

    class Meta:
        model = Subscription
        fields = ('id', 'member', 'departure', 'destination', 'when')

    def create(self, validated_data):
        validated_data['member'] = get_object_or_404(Member, token=validated_data['member'])
        return Subscription.objects.create(**validated_data)
