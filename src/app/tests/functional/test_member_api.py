from app.models import Member
from rest_framework.test import APIClient


def test_create_member(db):
    response = APIClient().post('/api/members/', {'username': 'MuslimBeibytuly'})
    assert response.status_code == 201
    assert 'username' in response.data.keys()
    assert 'token' in response.data.keys()
    assert response.data['username'] == 'MuslimBeibytuly'
    assert response.data['username'] == Member.objects.last().username
    assert response.data['token'] == Member.objects.last().token
    assert Member.objects.count() == 1
