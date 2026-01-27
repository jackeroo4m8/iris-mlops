import joblib
import pandas as pd
from sklearn.datasets import load_iris


MODEL_PATH = "models/iris_model.pkl"


def load_model(path):
    return joblib.load(path)


def load_metadata():
    """
    Loads dataset metadata (feature names and target names).
    This ensures inference stays aligned with training.
    """
    iris = load_iris(as_frame=True)
    return iris.feature_names, iris.target_names


def make_sample(feature_names):
    """
    Create a single iris sample with correct schema.
    """
    iris = load_iris(as_frame=True)
    return iris.data.sample(n=1, random_state=42)


def main():
    model = load_model(MODEL_PATH)

    feature_names, target_names = load_metadata()

    sample = make_sample(feature_names)
    prediction_index = model.predict(sample)[0]

    prediction_label = target_names[prediction_index]

    print(f"Prediction: {prediction_label} ({prediction_index})")


if __name__ == "__main__":
    main()
