FROM python:3.9
RUN pip install -U pip
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./experiments/svc/model.pkl ./experiments/svc/model.pkl
COPY ./src ./src
COPY ./backend_producer.py ./backend_producer.py

EXPOSE 5003
ENTRYPOINT ["python", "backend_producer.py"]
