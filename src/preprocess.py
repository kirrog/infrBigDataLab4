import pandas as pd

from src.loggers import create_logger
from src.utils import save_train_data, save_valid_data, save_test_data

cstm_logger = create_logger(__name__)


class Preprocessor:
    def __init__(self, split_coef_train: float = 0.8,
                 split_coef_test: float = 0.1,
                 split_coef_validation: float = 0.1):
        self.split_coef_train = split_coef_train
        self.split_coef_test = split_coef_test
        self.split_coef_validation = split_coef_validation
        assert 1.0 == sum([self.split_coef_train, self.split_coef_test, self.split_coef_validation])
        self.train_data = None
        self.test_data = None
        self.validation_data = None

    def prepare_data(self, path2data: str):
        dataset = pd.read_csv(path2data)
        length = len(dataset)

        self.train_data = dataset.loc[:int(length * self.split_coef_train)]
        self.test_data = dataset.loc[:int(length * self.split_coef_test)]
        self.validation_data = dataset.loc[:int(length * self.split_coef_validation)]

        save_train_data(self.train_data)
        save_test_data(self.test_data)
        save_valid_data(self.validation_data)


if __name__ == "__main__":
    preprocessor = Preprocessor()
    preprocessor.prepare_data("./data/seeds.csv")
