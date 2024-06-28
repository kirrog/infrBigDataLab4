import argparse

from src.loggers import create_logger
from src.utils import load_model, load_valid_data, split2x_y

cstm_logger = create_logger(__name__)


class Predictor:

    def __init__(self):
        self.model = load_model()

    def predict_by_model(self, x_cases):
        y_cases = self.model.predict(x_cases)
        return y_cases


def start_predict_process(interactive_mod=False):
    model = Predictor()
    x_data, y_data = split2x_y(load_valid_data())
    y_results = model.predict_by_model(x_data)
    cstm_logger.info("Right")
    cstm_logger.info(y_data)
    cstm_logger.info("Predicted")
    cstm_logger.info(y_results)
    if interactive_mod:
        while True:
            text_area = float(input("Enter Area value in range {10.59 - 21.18}: "))
            text_perimeter = float(input("Enter Perimeter value in range {12.41 - 17.25}: "))
            text_compactness = float(input("Enter Compactness value in range {0.8081 - 0.9183}: "))
            text_kernel_length = float(input("Enter Kernel.Length value in range {4.899 - 6.675}: "))
            text_kernel_width = float(input("Enter Kernel.Width value in range {2.63 - 4.033}: "))
            text_asymmetry_coeff = float(input("Enter Asymmetry.Coeff value in range {0.7651 - 8.315}: "))
            text_kernel_groove = float(input("Enter Kernel.Groove value in range {4.519 - 6.55}: "))
            floats = [[text_area, text_perimeter,
                       text_compactness, text_kernel_length,
                       text_kernel_width, text_asymmetry_coeff,
                       text_kernel_groove]]
            y_result_data = model.predict_by_model(floats)
            cstm_logger.info(y_result_data)
            stop = input("Stop: ")
            if stop != "":
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Prediction',
        description='Predict by model')
    parser.add_argument('-i', "--interactive", action="store_true")
    args = parser.parse_args()
    start_predict_process(args.interactive)
