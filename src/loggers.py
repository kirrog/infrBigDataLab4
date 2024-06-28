import logging
import sys
from pathlib import Path


def create_logger(name):
    cstm_logger = logging.getLogger(name)
    cstm_logger.setLevel(logging.INFO)
    path2logs = Path(f"./logs/")
    path2logs.mkdir(exist_ok=True, parents=True)
    handler = logging.FileHandler(str(path2logs / f"{name}.log"), mode='w')
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    cstm_logger.addHandler(handler)

    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    cstm_logger.addHandler(handler)

    return logging.Logger(name)
