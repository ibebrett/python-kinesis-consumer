from sqlalchemy import create_engine, Column, Integer, Boolean, String

Base = declarative_base()

class KinesisStream(Base):
    __tablename__ = 'kinesis_stream'

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
