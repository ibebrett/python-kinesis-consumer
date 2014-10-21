from sqlalchemy import create_engine, Column, Integer, String

Base = declarative_base()

class KinesisShard(Base):
    __tablename__ = 'kinesis_shard'

    id          = Column(Integer, primary_key=True)
    stream      = Column(String)
    shard_id    = Column(String)
    last_record = Column(String)

Session = sessionmaker()

def create(engine):
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--create', action='store_true')

    args = parser.parse_args()

    if args.create:
        create()
