from proj.models import Member, Subscription
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


def test_create_subscription(db):
    member = Member.objects.create(username='MuslimBeibytuly')
    data = {
        'member': member.token,
        'when': '10:30',
        'departure': 'KBTU',
        'destination': 'DMIS'
    }
    response = APIClient().post('/api/subscriptions/', data)
    assert response.status_code == 201
    assert response.data['when'] == '10:30'
    assert response.data['departure'] == 'KBTU'
    assert response.data['destination'] == 'DMIS'
    assert response.data['when'] == Subscription.objects.last().when
    assert response.data['departure'] == Subscription.objects.last().departure
    assert response.data['destination'] == Subscription.objects.last().destination
