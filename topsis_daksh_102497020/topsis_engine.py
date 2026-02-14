import pandas as pd
import numpy as np
import os


class TopsisCalculator:

    def __init__(self, input_path, weights, impacts, output_path):
        self.input_path = input_path
        self.weights = [float(w.strip()) for w in weights.split(",")]
        self.impacts = [i.strip() for i in impacts.split(",")]
        self.output_path = output_path

    def _validate(self, df):

        if df.shape[1] < 3:
            raise ValueError("Input file must contain at least 3 columns.")

        numeric_df = df.iloc[:, 1:]

        try:
            numeric_df = numeric_df.astype(float)
        except:
            raise ValueError("All criteria columns must be numeric.")

        if len(self.weights) != numeric_df.shape[1]:
            raise ValueError("Weights count must match number of criteria.")

        if len(self.impacts) != numeric_df.shape[1]:
            raise ValueError("Impacts count must match number of criteria.")

        for impact in self.impacts:
            if impact not in ["+", "-"]:
                raise ValueError("Impacts must be '+' or '-'.")

        return numeric_df

    def execute(self):

        if not os.path.exists(self.input_path):
            raise FileNotFoundError("Input file not found.")

        df = pd.read_csv(self.input_path)

        numeric_df = self._validate(df)

        matrix = numeric_df.values

        # Step 1: Normalize
        norm_matrix = matrix / np.sqrt((matrix**2).sum(axis=0))

        # Step 2: Apply weights
        weighted_matrix = norm_matrix * self.weights

        # Step 3: Ideal best and worst
        ideal_best = []
        ideal_worst = []

        for i in range(len(self.impacts)):
            if self.impacts[i] == "+":
                ideal_best.append(np.max(weighted_matrix[:, i]))
                ideal_worst.append(np.min(weighted_matrix[:, i]))
            else:
                ideal_best.append(np.min(weighted_matrix[:, i]))
                ideal_worst.append(np.max(weighted_matrix[:, i]))

        ideal_best = np.array(ideal_best)
        ideal_worst = np.array(ideal_worst)

        # Step 4: Distances
        dist_best = np.sqrt(((weighted_matrix - ideal_best)**2).sum(axis=1))
        dist_worst = np.sqrt(((weighted_matrix - ideal_worst)**2).sum(axis=1))

        # Step 5: Score
        scores = dist_worst / (dist_best + dist_worst)

        df["Topsis Score"] = scores
        df["Rank"] = df["Topsis Score"].rank(ascending=False, method="max")

        df.to_csv(self.output_path, index=False)
