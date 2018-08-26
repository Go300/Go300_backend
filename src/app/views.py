from rest_framework.viewsets import ModelViewSet

from .models import Member
from .serializers import MemberSerializer


class MemberViewSet(ModelViewSet):
    class Meta:
        model = Member

    serializer_class = MemberSerializer
    queryset = Member.objects.all()
