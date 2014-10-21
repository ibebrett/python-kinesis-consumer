import time
from boto.kinesis.layer1 import KinesisConnection

from . import models

class Consumer(object):
    def __init__(self, stream, shard_id, session, limit=None):
        self.stream   = stream
        self.shard_id = shard_id
        self.limit    = limit
        self.session  = session

        self.connection = KinesisConnection()

        self.shard = self.session.query(models.KinesisShard).filter(
            models.KinesisShard.stream==self.stream,
            models.KinesisShard.shard_id==self.shard_id
        ).first()

        if not self.shard:
            self.shard = models.KinesisShard(
                stream=self.stream,
                shard_id=self.shard_id
            )

    def get_current_record(self):
        if self.shard.last_record:
            return self.shard.last_record

        return None

    def save_current_record(self, current_record):
        self.shard.last_record = current_record
        self.session.add(self.shard)
        self.session.commit()

    def process(self, sleep=True):
        stream_desc = self.connection.describe_stream(self.stream)

        shard_dict = {
            shard['ShardId']: shard
            for shard in stream_desc['StreamDescription']['Shards']
        }

        shard = shard_dict[self.shard_id]

        last_record = self.get_current_record()
        if last_record is None:
            last_record = shard['SequenceNumberRange']['StartingSequenceNumber']
            shard_iterator_result = self.connection.get_shard_iterator(
                self.stream,
                self.shard_id,
                'AT_SEQUENCE_NUMBER',
                last_record)
        else:
             shard_iterator_result = self.connection.get_shard_iterator(
                self.stream,
                self.shard_id,
                'AFTER_SEQUENCE_NUMBER',
                last_record)

        shard_iterator = shard_iterator_result['ShardIterator']

        times = 0
        processing = True
        while True:
            records_result = self.connection.get_records(shard_iterator)

            records = records_result['Records']

            for record in records:
                processing = self.process_record(record['Data'])

                if processing:
                    self.save_current_record(record['SequenceNumber'])
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
