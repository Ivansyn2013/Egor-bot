import pytest
from models.subscribers import Subscriber

def test_create_user(create_connecting):
    db = create_connecting
    sub = Subscriber(
        user_name="test_user_name",
    )
    db.add(sub)
    db.commit()
    assert sub.user_name == "test_user_name"
    assert db.query(Subscriber).first() is not None
