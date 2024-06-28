from cassandra.cluster import Cluster


class CassandraDataBaseController:

    def __init__(self):
        self.cluster = Cluster(["0.0.0.0"], port=9042)
        self.session = self.cluster.connect()
        self.session.execute(
            "CREATE KEYSPACE IF NOT EXISTS seeds_data WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };")
        self.session.set_keyspace("seeds_data")

        self.session.execute("CREATE TABLE IF NOT EXISTS seeds_data.seed_case (" +
                             "seed_id int PRIMARY KEY," +
                             "area float," +
                             "perimeter float," +
                             "compactness float," +
                             "kernel_length float," +
                             "kernel_width float," +
                             "asymmetry_coeff float," +
                             "kernel_groove float," +
                             "seed_type int," +
                             ");")
        self.session.execute("INSERT INTO seeds_data.seed_case "
                             "(seed_id, area, perimeter, compactness, "
                             "kernel_length, kernel_width, asymmetry_coeff, "
                             "kernel_groove, seed_type) "
                             "VALUES (1, 2.0, 2.0, 2.0, "
                             "2.0, 2.0, 2.0, "
                             "2.0, 2);")
        data = self.session.execute("SELECT * FROM seeds_data.seed_case;")
        for row in data:
            print(row)


if __name__ == "__main__":
    CassandraDataBaseController()
