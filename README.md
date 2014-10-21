 
 An example of how to use a consumer:

    from kinesis_consumer import models, consumer

    from sqlalchemy import create_engine
    from sqlalchemy.engine.url import URL
    from boto import kinesis

    class TestConsumer(consumer.Consumer):
        def process_record(self, record):
            print record # do work here
            return True  # return False to stop processing after this record

    DB_CONNECTION = {
        "drivername": "postgresql",
        "kwargs": dict(
                username='dbuser', 
                password='dbpassword'
                host='dbhost'
                port=5432,
                database='db'
        )
    }

    engine = create_engine(URL(
        DB_CONNECTION['drivername'],
        **DB_CONNECTION['kwargs']
    ))

    session = models.Session(bind=engine)

    test_consumer = TestConsumer('arachnid', 'shardId-000000000000', session)
    test_consumer.process()
