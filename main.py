from cassandra.cluster import NoHostAvailable
from flask import Flask, request

from src.database_service import DatabaseService
from src.loggers import create_logger
from src.predict import Predictor
from src.seed_data import SeedData

cstm_logger = create_logger(__name__)

app = Flask(__name__)
cstm_logger.info("Check connect ability")
try:
    db_serv = DatabaseService(cstm_logger)
    res = db_serv.check_readability()
    cstm_logger.exception(f"Logger Successfully connect to cassandra. Data: {res}")
except NoHostAvailable as e:
    cstm_logger.exception(f"Can't connect to cassandra: {e}")
    exit(1)


@app.route('/')
def check():
    return 'Flask is running!'


@app.route('/predict', methods=['POST'])
def predict_by_model():
    data = request.json
    model = Predictor()
    seed_data_instance = SeedData(data)
    floats = [seed_data_instance.return_floats()]
    y_result_data = int(model.predict_by_model(floats)[0])
    cstm_logger.warning(f"Prediction result is: {y_result_data}")
    seed_data_instance.set_prediction(y_result_data)
    db_serv.save_seed_data(seed_data_instance)
    return f'{y_result_data}'


@app.route('/get_last', methods=['POST'])
def get_last_seed_data():
    return [x.__dict__ for x in db_serv.get_last_seeds_data()]


if __name__ == '__main__':
    app.run(debug=True, port=5555, host="0.0.0.0")
