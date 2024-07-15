from models import Base


def create_all(engine):
    Base.metadata.create_all(engine)


def drop_all(engine):
    Base.metadata.drop_all(engine)
    return engine

if __name__ == '__main__':
    from models import Base, engine
    #create_all(engine)
    drop_all(engine)
