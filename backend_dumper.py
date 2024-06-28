import json

from cassandra.cluster import NoHostAvailable
from kafka import KafkaConsumer

from src.database_service import DatabaseService
from src.loggers import create_logger
from src.seed_data import SeedData

ORDER_KAFKA_TOPIC = 'seeds_data'
KAFKA_SERVER_ADDRESS = 'broker:29092'

cstm_logger = create_logger(__name__)

consumer = KafkaConsumer(ORDER_KAFKA_TOPIC, bootstrap_servers=[KAFKA_SERVER_ADDRESS], security_protocol="PLAINTEXT",
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

cstm_logger.info("Check connect ability")
try:
    db_serv = DatabaseService(cstm_logger)
    res = db_serv.check_readability()
    cstm_logger.exception(f"Logger Successfully connect to cassandra. Data: {res}")
except NoHostAvailable as e:
    cstm_logger.exception(f"Can't connect to cassandra: {e}")
    exit(1)

while True:
    for message in consumer:
        cstm_logger.exception("Received order details: {}".format(message.value))
        seed_data_instance = SeedData(message.value)
        seed_data_instance.set_prediction(message.value["prediction"])

        db_serv.save_seed_data(seed_data_instance)
        cstm_logger.exception(f"Save message: {message}")
