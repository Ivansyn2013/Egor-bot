from models.subscribers import Subscriber


def test_create_user(create_connecting):
    db = create_connecting
    sub = Subscriber(
        user_id=12345678,
        user_name="test_user_name",
    )
    db.add(sub)
    db.commit()
    assert sub.user_name == "test_user_name"
    assert sub.user_id == 12345678
    assert db.query(Subscriber).first() is not None
