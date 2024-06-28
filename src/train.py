import json
import pickle
from pathlib import Path

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

from src.loggers import create_logger
from src.utils import load_train_data, load_test_data, split2x_y

cstm_logger = create_logger(__name__)


class Trainer:
    def __init__(self, dual: str = "auto", random_state: int = 0, tol: float = 1e-5):
        self.dual = dual
        self.random_state = random_state
        self.tol = tol
        self.model = self.create_new_model(dual, random_state, tol)

    def create_new_model(self, dual: str, random_state: int, tol: float):
        return make_pipeline(StandardScaler(), LinearSVC(dual=dual, random_state=random_state, tol=tol))

    def train_model(self, reinit: bool = True):
        if reinit:
            self.model = self.create_new_model(self.dual, self.random_state, self.tol)
        x_train, y_train = split2x_y(load_train_data())
        x_test, y_test = split2x_y(load_test_data())

        self.model.fit(x_train, y_train)
        scores = dict()

        score = self.model.score(x_train, y_train)
        cstm_logger.info(f"Result score of trained model on train data: {score}")
        scores["train_acc"] = score

        score = self.model.score(x_test, y_test)
        cstm_logger.info(f"Result score of trained model on test data: {score}")
        scores["test_acc"] = score

        p = Path("./experiments/svc")

        p.mkdir(exist_ok=True, parents=True)

        with open(str(p / "model.pkl"), "wb") as f:
            pickle.dump(self.model, f)

        with open(str(p / "metrics.json"), "w", encoding="UTF-8") as f:
            json.dump(scores, f)


if __name__ == "__main__":
    trainer = None
    try:
        with open("./config.ini", "r") as f:
            args = json.load(f)
        trainer = Trainer(args["dual"], args["random_state"], args["tol"])
    except:
        trainer = Trainer()
    trainer.train_model()
