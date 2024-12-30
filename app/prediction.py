import pandas as pd
import feature_extraction as fe
from sklearn.svm import SVC


def make_prediction(file_name):

    X_train = pd.read_csv("app/X.csv", sep=",")
    Y_train = pd.read_csv("app/Y.csv", sep=",")["0"]

    top_features = open("app/best_features.txt", "r").read().split(",")[:-1]

    X_selected = fe.calculate_selected_features(file_name)[top_features]
    X_train = X_train[top_features]

    svm = SVC(kernel='linear', C=1.0, random_state=42)
    svm.fit(X_train, Y_train)

    Y_pred = svm.predict(X_selected)
    return Y_pred[0]




