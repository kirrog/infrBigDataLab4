from typing import Dict, List


class SeedData:
    def __init__(self, data: Dict):
        self.area = float(data["area"])
        self.perimeter = float(data["perimeter"])
        self.compactness = float(data["compactness"])
        self.kernel_length = float(data["kernel_length"])
        self.kernel_width = float(data["kernel_width"])
        self.asymmetry_coeff = float(data["asymmetry_coeff"])
        self.kernel_groove = float(data["kernel_groove"])
        self.prediction = None

    def set_prediction(self, prediction: int):
        self.prediction = prediction

    def return_floats(self) -> List[float]:
        floats = [self.area, self.perimeter,
                  self.compactness, self.kernel_length,
                  self.kernel_width, self.asymmetry_coeff,
                  self.kernel_groove]
        return floats
