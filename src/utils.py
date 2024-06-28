import pickle
from pathlib import Path

import pandas as pd

from src.loggers import create_logger

path2models = Path("./experiments")

cstm_logger = create_logger(__name__)


def load_model(path: str = "svc"):
    with open(str(path2models / path / "model.pkl"), "rb") as f:
        model = pickle.load(f)
    return model


def load_data(path: str):
    data = pd.read_csv(path)
    return data


def load_train_data():
    train_data = load_data("./data/train_data.csv")
    return train_data


def load_test_data():
    test_data = load_data("./data/test_data.csv")
    return test_data


def load_valid_data():
    validation_data = load_data("./data/validation_data.csv")
    return validation_data


def save_data(data, path: str):
    data.to_csv(path)


def save_train_data(train_data):
    save_data(train_data, "./data/train_data.csv")


def save_test_data(test_data):
    save_data(test_data, "./data/test_data.csv")


def save_valid_data(validation_data):
    save_data(validation_data, "./data/validation_data.csv")


def split2x_y(data):
    x_data = []
    y_data = []
    for i, row in data.iterrows():
        x_data.append(list(row[["Area",
                                "Perimeter",
                                "Compactness",
                                "Kernel.Length",
                                "Kernel.Width",
                                "Asymmetry.Coeff",
                                "Kernel.Groove"]]))
        y_data.append(row["Type"])
    return x_data, y_data
