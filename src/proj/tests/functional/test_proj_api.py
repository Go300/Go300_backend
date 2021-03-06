from push_notifications.models import GCMDevice

from proj.models import Member, Subscription, Confirmation
from rest_framework.test import APIClient


def test_create_member(db):
    response = APIClient().post(
        '/api/members/',
        {
            'username': 'MuslimBeibytuly',
            'registration_id': 'c-VNO1n4oPI:'
                               'APA91bF7mS2twx1naJr5bax1-'
                               'Zr7JAmRux4zyDgJ3aKpEdqCIFBRF0Al5xSRadIUQKmQQMvE4mWVoibsxCd1yzu'
                               'PxQPLxDTT6Cw1wfZa1cEcI9m5bxfXTtWdjMHj4HhHQgJIx21EI9NZ'
        }
    )
    assert response.status_code == 201
    assert 'username' in response.data.keys()
    assert 'token' in response.data.keys()
    assert response.data['username'] == 'MuslimBeibytuly'
    assert Member.objects.count() == 1
    assert response.data['username'] == Member.objects.last().username
    assert response.data['token'] == Member.objects.last().token
    assert GCMDevice.objects.count() == 1
    assert GCMDevice.objects.last().user == Member.objects.last()


def test_create_device(db):
    member = Member.objects.create(username='MuslimBeibytuly')
    response = APIClient().post(
        '/api/devices/',
        {
            'user': member.token,
            'registration_id': 'c-VNO1n4oPI:'
                               'APA91bF7mS2twx1naJr5bax1-'
                               'Zr7JAmRux4zyDgJ3aKpEdqCIFBRF0Al5xSRadIUQKmQQMvE4mWVoibsxCd1yzu'
                               'PxQPLxDTT6Cw1wfZa1cEcI9m5bxfXTtWdjMHj4HhHQgJIx21EI9NZ'
        }
    )
    assert response.status_code == 201
    assert GCMDevice.objects.count() == 1


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


def test_patch_confirmation(db):
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

    confirmation = Confirmation.objects.create(
        subscription=Subscription.objects.last()
    )
    response = APIClient().patch('/api/confirmations/{}/'.format(confirmation.id), {})
    assert response.status_code == 200
    assert Confirmation.objects.last().confirmed is True


def test_delete_subscription(db):
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

    response = APIClient().delete('/api/subscriptions/{}/'.format(Subscription.objects.last().id))
    assert response.status_code == 204
    assert Subscription.objects.count() == 0
