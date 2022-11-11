from contextlib import contextmanager

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Image(Base):
    __tablename__ = 'image'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)


class Topic(Base):
    __tablename__ = 'topic'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.Text, nullable=False)
    image_id = sa.Column(sa.Integer, sa.ForeignKey('image.id'), nullable=False)
    image = sa.orm.relationship(Image)  # innerjoin=True для JOIN
    questions = sa.orm.relationship('Question')

    users = sa.orm.relationship('User', secondary='topic_user')
    # association
    # users = sa.orm.relationship('TopicUser', back_populates='topic')


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)

    # association
    # topics = sa.orm.relationship('TopicUser', back_populates='user')


class TopicUser(Base):
    __tablename__ = 'topic_user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    topic_id = sa.Column(sa.Integer, sa.ForeignKey('topic.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    role = sa.Column(sa.Text)

    # association
    # user = sa.orm.relationship(User, back_populates='topics')
    # topic = sa.orm.relationship(Topic, back_populates='users')


class Question(Base):
    __tablename__ = 'question'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    text = sa.Column(sa.Text)
    topic_id = sa.Column(sa.Integer, sa.ForeignKey('topic.id'), nullable=False)
    topic = sa.orm.relationship(Topic)  # innerjoin=True для использования
    # JOIN вместо LEFT JOIN




import os

BD_PASS = os.getenv('BD_PASS')

connect_url = fr'mysql+asyncmy://test:{BD_PASS}@192.168.0.110:3300/egor_db' \
               r'?charset=utf8mb4'

engine = sa.create_engine(connect_url, echo=True)

DBSession = sessionmaker(
    binds={
        Base: engine,
    },
    expire_on_commit=False,
)


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations."""
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

if __name__ == '__main__':
    with session_scope() as s:
        questions = s.query(Question).filter(
            Question.Common == 3,
        ).order_by(Question.id.desc()).limit(10).all()



#
# def use_inspector(conn):
#     inspector = inspect(conn)
#     # use the inspector
#     print(inspector.get_view_names())
#     # return any value to the caller
#     return inspector.get_table_names()
#
#
# async def async_main():
#     async with engine.connect() as conn:
#         tables = await conn.run_sync(use_inspector)
#         print(tables)
#
#
# asyncio.run(async_main())
#
#
#
# # async with engine.begin() as conn:
# #     result = await conn.execute(text('SHOW TABLES'))
# #     print(result)
#
#


# metadata = sqlalchemy.MetaData()
# metadata.bind=engine
# if metadata.is_bound():
#     print("Connetion ok")
#
# print(metadata.tables.keys())