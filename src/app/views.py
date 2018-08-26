from rest_framework.viewsets import ModelViewSet

from .serializers import MemberSerializer
from .models import Member


class MemberViewSet(ModelViewSet):
    class Meta:
        model = Member

    serializer_class = MemberSerializer
    queryset = Member.objects.all()
