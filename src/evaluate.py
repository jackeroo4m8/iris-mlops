import joblib

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

MODEL_PATH = "models/iris_model.pkl"
RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_data():
    iris = load_iris(as_frame=True)
    X = iris.data
    y = iris.target
    return X, y

def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )

    model = joblib.load(MODEL_PATH)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Evaluation Accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    main()