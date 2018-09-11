from push_notifications.models import GCMDevice
from rest_framework.test import APIClient

from core.celery import notify_members, group_members
from proj.models import Member, Subscription, Confirmation, Group


def test_notify_members(db):
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
    Subscription.objects.create(member=member, when='10:30', departure='DMIS', destination='KBTU')

    notify_members.apply(kwargs={'hour': 10, 'minute': 30})

    assert Confirmation.objects.count() == 1
    assert Confirmation.objects.last().member == member


def test_group_members(db):
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
    Subscription.objects.create(member=member, when='10:30', departure='DMIS', destination='KBTU')

    notify_members.apply(kwargs={'hour': 10, 'minute': 30})
    assert Confirmation.objects.count() == 1
    assert Confirmation.objects.last().member == member

    assert Confirmation.objects.last().confirmed is False
    response = APIClient().patch('/api/confirmations/{}/'.format(Confirmation.objects.last().id), {})
    assert response.status_code == 200
    assert Confirmation.objects.last().confirmed is True

    group_members.apply(kwargs={'hour': 10, 'minute': 30})
    assert Group.objects.count() == 1
    assert Group.objects.last().members.count() == 1
    assert Group.objects.last().members.last() == member


def test_group_members_8(db):
    test_count = 8
    for counter in range(test_count):
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
        Subscription.objects.create(member=member, when='10:30', departure='DMIS', destination='KBTU')

    assert GCMDevice.objects.count() == test_count

    notify_members.apply(kwargs={'hour': 10, 'minute': 30})
    assert Confirmation.objects.count() == test_count

    confirmations = Confirmation.objects.all()
    for confirmation in confirmations:
        response = APIClient().patch('/api/confirmations/{}/'.format(confirmation.id), {})
        assert response.status_code == 200

    group_members.apply(kwargs={'hour': 10, 'minute': 30})
    groups = Group.objects.all()
    assert groups.count() == 2
    for group in groups:
        assert group.members.count() == 4
        assert Member.objects.filter(group=group).count() == 4


def test_group_members_7(db):
    test_count = 7
    for counter in range(test_count):
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
        Subscription.objects.create(member=member, when='10:30', departure='DMIS', destination='KBTU')

    assert GCMDevice.objects.count() == test_count

    notify_members.apply(kwargs={'hour': 10, 'minute': 30})
    assert Confirmation.objects.count() == test_count

    confirmations = Confirmation.objects.all()
    for confirmation in confirmations:
        response = APIClient().patch('/api/confirmations/{}/'.format(confirmation.id), {})
        assert response.status_code == 200

    group_members.apply(kwargs={'hour': 10, 'minute': 30})
    groups = Group.objects.all()
    assert groups.count() == 2
    assert groups.first().members.count() == 4
    assert groups.last().members.count() == 3
    assert Member.objects.filter(group=groups.first()).count() == 4
    assert Member.objects.filter(group=groups.last()).count() == 3


def test_group_members_6(db):
    test_count = 6
    for counter in range(test_count):
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
        Subscription.objects.create(member=member, when='10:30', departure='DMIS', destination='KBTU')

    assert GCMDevice.objects.count() == test_count

    notify_members.apply(kwargs={'hour': 10, 'minute': 30})
    assert Confirmation.objects.count() == test_count

    confirmations = Confirmation.objects.all()
    for confirmation in confirmations:
        response = APIClient().patch('/api/confirmations/{}/'.format(confirmation.id), {})
        assert response.status_code == 200

    group_members.apply(kwargs={'hour': 10, 'minute': 30})
    groups = Group.objects.all()
    assert groups.count() == 2
    for group in groups:
        assert group.members.count() == 3
        assert Member.objects.filter(group=group).count() == 3


def test_group_members_5(db):
    test_count = 5
    for counter in range(test_count):
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
        Subscription.objects.create(member=member, when='10:30', departure='DMIS', destination='KBTU')

    assert GCMDevice.objects.count() == test_count

    notify_members.apply(kwargs={'hour': 10, 'minute': 30})
    assert Confirmation.objects.count() == test_count

    confirmations = Confirmation.objects.all()
    for confirmation in confirmations:
        response = APIClient().patch('/api/confirmations/{}/'.format(confirmation.id), {})
        assert response.status_code == 200

    group_members.apply(kwargs={'hour': 10, 'minute': 30})
    groups = Group.objects.all()
    assert groups.count() == 2
    assert groups.first().members.count() == 3
    assert groups.last().members.count() == 2
    assert Member.objects.filter(group=groups.first()).count() == 3
    assert Member.objects.filter(group=groups.last()).count() == 2


def test_group_members_4(db):
    test_count = 4
    for counter in range(test_count):
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
        Subscription.objects.create(member=member, when='10:30', departure='DMIS', destination='KBTU')

    assert GCMDevice.objects.count() == test_count

    notify_members.apply(kwargs={'hour': 10, 'minute': 30})
    assert Confirmation.objects.count() == test_count

    confirmations = Confirmation.objects.all()
    for confirmation in confirmations:
        response = APIClient().patch('/api/confirmations/{}/'.format(confirmation.id), {})
        assert response.status_code == 200

    group_members.apply(kwargs={'hour': 10, 'minute': 30})
    groups = Group.objects.all()
    assert groups.count() == 1
    assert groups.last().members.count() == 4
    assert Member.objects.filter(group=groups.last()).count() == 4
