from app.models import Member


def test_member_create(db):
    member = Member.objects.create(username='MuslimBeibytuly')

    assert member.username == 'MuslimBeibytuly'
    assert member.token is not None
    assert member.token == Member.objects.last().token
    assert Member.objects.count() == 1
