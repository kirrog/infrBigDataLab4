import json
import time

from kafka import KafkaProducer
from flask import Flask, jsonify, request

from src.loggers import create_logger
from src.predict import Predictor
from src.seed_data import SeedData

ORDER_KAFKA_TOPIC = 'seeds_data'
KAFKA_SERVER_ADDRESS = 'broker:29092'
app = Flask(__name__)

cstm_logger = create_logger(__name__)

producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER_ADDRESS], security_protocol="PLAINTEXT",
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))


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
    result_instance =  {k: v for k, v in seed_data_instance.__dict__.items()}
    result_instance['time'] = time.time()
    producer.send(ORDER_KAFKA_TOPIC, result_instance)
    return jsonify(result_instance)


if __name__ == '__main__':
    app.run(debug=True, port=5003, host="0.0.0.0")
