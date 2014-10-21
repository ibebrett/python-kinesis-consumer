import time
from boto import kinesis

from . import models

class Consumer(object):
    def __init__(self, stream, shard_id, session, limit=None):
        self.stream   = stream
        self.shard_id = shard_id
        self.limit    = limit
        self.session  = session

        self.connection = kinesis.layer1.KinesisConnection()

        self.shard = self.session.query(models.KinesisShard).filter(
            stream=self.stream,
            shard_id=self.shard_id
        ).first()

    def get_current_record(self):
        if self.stream.last_record:
            return stream.last_record

        return None

    def save_current_record(self, current_record):
        self.stream.last_record = current_record
        self.session.add(self.stream)
        self.session.commit()

    def process(self, sleep=True):
        stream_desc = self.connection.describe_stream(self.stream)
        shard = desc['StreamDescription']['Shards'][0]

        last_record = self.get_last_record()
        if last_record is None:
            last_record = shard['SequenceNumberRange']['StartingSequenceNumber']
            shard_iterator_result = self.connection.get_shard_iterator(
                self.stream,
                self.shard_id,
                'AT_SEQUENCE_NUMBER')
        else:
             shard_iterator_result = self.connection.get_shard_iterator(
                self.stream,
                self.shard_id,
                'AFTER_SEQUENCE_NUMBER')

        shard_iterator = shard_iterator_result['ShardIterator']

        times = 0
        processing = True
        while True:
            records_result = self.connection.get_records(shard_iterator)

            records = get_records['Records']

            for record in records:
                processing = self.process_record(record)

                if processing:
                    self.save_current_record(record)
                    pass
                else:
                    break

            shard_iterator = records_result['NextShardIterator']

            times += 1
            if not processing or (self.limit and times > self.limit):
                break

            if sleep:
                time.sleep(1)

    def process_record(self, record):
        return True
