from push_notifications.models import GCMDevice
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Member, Subscription, Confirmation


class DeviceSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(required=True, write_only=True)

    class Meta:
        model = GCMDevice
        fields = ('registration_id', 'cloud_message_type', 'user')

    def create(self, validated_data):
        validated_data['user'] = get_object_or_404(Member, token=validated_data['user'])
        return GCMDevice.objects.create(**validated_data)


class MemberSerializer(serializers.ModelSerializer):
    token = serializers.ReadOnlyField()
    username = serializers.CharField(required=True)
    registration_id = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Member
        fields = ('username', 'token', 'registration_id')
        extra_kwargs = {
            'registration_id': {'write_only': True}
        }

    def validate(self, attrs):
        self.registration_id = attrs.pop('registration_id', None)
        return attrs

    def create(self, validated_data):
        member = Member.objects.create(**validated_data)
        GCMDevice.objects.create(user=member, registration_id=self.registration_id)
        return member


class SubscriptionSerializer(serializers.ModelSerializer):
    member = serializers.UUIDField(required=True, write_only=True)

    class Meta:
        model = Subscription
        fields = ('id', 'member', 'departure', 'destination', 'when')

    def create(self, validated_data):
        validated_data['member'] = get_object_or_404(Member, token=validated_data['member'])
        return Subscription.objects.create(**validated_data)


class ConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Confirmation
        fields = ('id',)

    def update(self, instance, validated_data):
        instance.confirmed = True
        instance.save()
        return instance
