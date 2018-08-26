from rest_framework import serializers

from .models import Member


class MemberSerializer(serializers.ModelSerializer):
    token = serializers.ReadOnlyField()
    username = serializers.CharField(required=True)

    class Meta:
        model = Member
        fields = ('username', 'token')
