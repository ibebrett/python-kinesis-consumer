from . import models

class Consumer(object):
    def __init__(self, stream, shard_id, limit=None):
        self.stream   = stream
        self.shard_id = shard_id

    def process(self):
        pass

    def process_record(self, record):
        pass
