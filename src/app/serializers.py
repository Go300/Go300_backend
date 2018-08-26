from rest_framework import serializers

from .models import Member, Subscription


class MemberSerializer(serializers.ModelSerializer):
    token = serializers.ReadOnlyField()
    username = serializers.CharField(required=True)

    class Meta:
        model = Member
        fields = ('username', 'token')


class SubscriptionSerializer(serializers.ModelSerializer):
    token = serializers.UUIDField(required=True, write_only=True)

    class Meta:
        model = Subscription
        fields = ('token', 'departure', 'destination', 'when')

    def create(self, validated_data):
        validated_data['member'] = Member.objects.filter(token=validated_data['token']).last()
        del validated_data['token']
        return Subscription.objects.create(**validated_data)
