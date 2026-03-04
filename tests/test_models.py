from models.subscribers import Subscriber, UserRequest


def test_create_user_request(create_connecting):
    db = create_connecting
    sub = Subscriber(
        user_id=12345,
        user_name="test_user",
    )
    db.add(sub)
    db.commit()

    req = UserRequest(text="Help me with foodmap", subscriber_id=sub.id)
    db.add(req)
    db.commit()

    assert req.text == "Help me with foodmap"
    assert req.user.user_name == "test_user"
    assert len(sub.user_requests) == 1
    assert sub.user_requests[0].text == "Help me with foodmap"


def test_subscriber_relationship(create_connecting):
    db = create_connecting
    sub = Subscriber(user_id=111, user_name="Alice")
    db.add(sub)
    db.commit()

    req1 = UserRequest(text="Request 1", subscriber_id=sub.id)
    req2 = UserRequest(text="Request 2", subscriber_id=sub.id)
    db.add_all([req1, req2])
    db.commit()

    db.refresh(sub)
    assert len(sub.user_requests) == 2
    assert any(r.text == "Request 1" for r in sub.user_requests)
    assert any(r.text == "Request 2" for r in sub.user_requests)
