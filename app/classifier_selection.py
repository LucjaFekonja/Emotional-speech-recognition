import numpy as np
import pandas as pd
import dimension_reduction as dr
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier


def SVM(X, Y, n, dimension_reduction_technique):
    """ 
    n ... number of selected features
    dimension_reduction_techniwue ... either "fisher" or "PCA"
    """

    if dimension_reduction_technique == "fisher":
        rates = dr.fisher_discriminator(X, Y)

    if dimension_reduction_technique == "PCA":
        rates = dr.principal_component_analysis(X)


    top_features_indices = np.argsort(rates)[-n:]  # Indices of top features
    X_selected = X.iloc[:, top_features_indices]

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_selected, Y, test_size=0.2, random_state=42)
    X_train, X_test, y_train, y_test = X_train.to_numpy(), X_test.to_numpy(), y_train.to_numpy(), y_test.to_numpy() 

    # Train SVM Classifier
    svm = SVC(kernel='linear', C=1.0, random_state=42)
    svm.fit(X_train, y_train)

    # Predict and Evaluate
    y_pred = svm.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy




def ann(X, Y, n, dimension_reduction_technique):
    
    if dimension_reduction_technique == "fisher":
        rates = dr.fisher_discriminator(X, Y)
    if dimension_reduction_technique == "PCA":
        rates = dr.principal_component_analysis(X)

    # Select Top Features Based on Fisher Scores
    top_features_indices = np.argsort(rates)[-n:]  # Indices of top features
    X_selected = X.iloc[:, top_features_indices]

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_selected, Y, test_size=0.2, random_state=42)

    # Define and Train ANN with Multi-Layer Perceptron (MLP)
    ann = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000, solver='lbfgs', random_state=42)

    # Train the model
    ann.fit(X_train, y_train)

    # Predict and Evaluate Performance
    y_pred = ann.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy