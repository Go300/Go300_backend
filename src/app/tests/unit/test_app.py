from app.models import Member, Subscription


def test_member_create(db):
    member = Member.objects.create(username='MuslimBeibytuly')

    assert member.username == 'MuslimBeibytuly'
    assert member.token is not None
    assert member.token == Member.objects.last().token
    assert Member.objects.count() == 1
    assert str(member) == str(member.id)


def test_subscription_create(db):
    member = Member.objects.create(username='MuslimBeibytuly')
    subscription = Subscription.objects.create(member=member, when='10:30', departure='DMIS', destination='KBTU')

    assert subscription.member == member
    assert subscription.when == '10:30'
    assert subscription.departure == 'DMIS'
    assert subscription.destination == 'KBTU'
