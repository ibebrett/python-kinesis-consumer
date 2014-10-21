from sqlalchemy import  Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

