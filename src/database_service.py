import os
import socket
from logging import Logger
from typing import Dict, List

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

from src.seed_data import SeedData


def is_cassandra_connectable(ip: str, port: int) -> bool:
    test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        test.connect((ip, int(port)))
        test.shutdown(1)
        return True
    except:
        return False


class DatabaseService:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.port = os.environ.get('CASSANDRA_PORT', 9042)
        self.keyspace = os.environ.get('CASSANDRA_KEYSPACE', "sampledata")
        ips = self.balance_fake_load()
        self.cluster = Cluster(ips, port=self.port,
                               auth_provider=PlainTextAuthProvider(username=os.environ.get('CASSANDRA_USERNAME'),
                                                                   password=os.environ.get('CASSANDRA_PASSWORD')))
        self.session = self.cluster.connect(self.keyspace, wait_for_all_pools=False)
        self.session.execute(f'USE {self.keyspace}')

    def check_readability(self) -> Dict[int, str]:
        result = self.session.execute('SELECT * FROM months')
        rows = {}
        for row in result:
            rows[row.id] = row.name
        return rows

    def balance_fake_load(self) -> List[str]:
        ips = []
        for ip in os.environ.get('CASSANDRA_SEEDS').split(','):
            if is_cassandra_connectable(ip, self.port):
                ips.append(ip)
        return ips

    def save_seed_data(self, seed_data_instance: SeedData):
        id_value = int(seed_data_instance.__hash__()) % 2147483647

        prepared = self.session.prepare("""
                insert into sampledata.seeds_data 
                ( id, area_val, perimeter_val, compactness_val, kernel_length_val, 
                kernel_width_val, asymmetry_coeff_val, kernel_groove_val, type_val) 
                VALUES(?,?,?,?,?,?,?,?,?);
                """)

        self.session.execute(prepared,
                             [id_value] + seed_data_instance.return_floats() + [seed_data_instance.prediction])

    def get_last_seeds_data(self) -> List[SeedData]:
        cql_query = ("SELECT * FROM sampledata.seeds_data;")
        result_set = self.session.execute(cql_query)
        resutls_seeds = []
        for elem in result_set.all():
            self.logger.exception(f"Get elem: {elem}")

            elem_dict = {
                "area": elem[1],
                "perimeter": elem[2],
                "compactness": elem[3],
                "kernel_length": elem[4],
                "kernel_width": elem[5],
                "asymmetry_coeff": elem[6],
                "kernel_groove": elem[7],
            }

            prediction = int(elem[-1])
            seed_data = SeedData(elem_dict)
            seed_data.set_prediction(prediction)
            resutls_seeds.append(seed_data)
        return resutls_seeds
