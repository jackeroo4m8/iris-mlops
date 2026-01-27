import joblib
import pandas as pd
from sklearn.datasets import load_iris
from src.logger import get_logger

logger = get_logger(__name__)


MODEL_PATH = "models/iris_model.pkl"

def load_model():
    return joblib.load(MODEL_PATH)


def load_metadata():
    """
    Load future names and target names from the same source 
    used during training
    """
    iris = load_iris(as_frame=True)
    return iris.feature_names, iris.target_names


def build_sample_from_input(input_dict: dict) -> pd.DataFrame:
    iris = load_iris(as_frame=True)
    feature_names = iris.feature_names
    
    return pd.DataFrame(
        [[
            input_dict["sepal_length"],
            input_dict["sepal_width"],
            input_dict["petal_length"],
            input_dict["petal_width"]   
        ]],
        columns=feature_names
    )


def predict(input_dict: dict):
    logger.info("Starting Inference")

    sample_df = build_sample_from_input(input_dict)

    model = load_model()
    _, target_names = load_metadata()

    prediction_index = model.predict(sample_df)[0]
    prediction_label = target_names[prediction_index]

    logger.info(
        "Prediction completed | index=%s label=%s",
        prediction_index,
        prediction_label
    )

    return {
        "class_index": int(prediction_index),
        "class_label": prediction_label
    }