import os
import joblib


from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


MODEL_PATH = "models/iris_model.pkl"
RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_data():
    iris = load_iris(as_frame=True)
    X = iris.data
    y = iris.target
    return X, y


def train_model(X_train, y_train):
    model = RandomForestClassifier(random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    return model

def main():
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )

    model = train_model(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Training completed")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Model saved to {MODEL_PATH}")

    
if __name__ == "__main__":
    main()