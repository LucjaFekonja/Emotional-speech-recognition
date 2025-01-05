import pandas as pd
import feature_extraction as fe
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier


def make_prediction_savee(file_name):

    X_train = pd.read_csv("data/X_savee.csv", sep=",")
    Y_train = pd.read_csv("data/Y_savee.csv", sep=",")["0"]

    top_features = open("data/best_features_savee.txt", "r").read().split(",")[:-1]

    X_selected = fe.calculate_selected_features_savee(file_name)[top_features]
    X_train = X_train[top_features]

    svm = SVC(kernel='rbf', C=1.0, random_state=42)
    svm.fit(X_train, Y_train)

    Y_pred = svm.predict(X_selected)
    return Y_pred[0]


def make_prediction_tess(file_name):

    X_train = pd.read_csv("data/X_tess.csv", sep=",")
    Y_train = pd.read_csv("data/Y_tess.csv", sep=",")["0"]

    top_features = open("data/best_features_tess.txt", "r").read().split(",")[:-1]

    X_selected = fe.calculate_selected_features_tess(file_name)[top_features]
    X_train = X_train[top_features]

    ann = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000, solver='adam', random_state=42)
    ann.fit(X_train, Y_train)
    Y_pred = ann.predict(X_selected)

    return Y_pred[0]


import os
path = "C:/School/RZP/vaje/Projekt/Emotional-speech-recognition/audio_savee/"

for filename in os.listdir(path):

    if filename[3] == "s":
        file_path = os.path.join(path, filename)
        pred = make_prediction_tess(file_path)
        print(filename, pred)
