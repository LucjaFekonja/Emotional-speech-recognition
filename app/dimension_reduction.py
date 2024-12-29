import numpy as np
import scipy

def fisher_discriminator(X, y):
    """
    Implements the Fisher Discriminator as described in the provided equations.
    
    Parameters:
        X (numpy.ndarray): Feature matrix (n_samples x n_features).
        y (numpy.ndarray): Class labels (n_samples, ).
    
    Returns:
        F_r (numpy.ndarray): Fisher scores for each feature.
    """
    n_samples, n_features = X.shape
    classes = np.unique(y)

    # Initialize scatter matrices
    S_w = np.zeros((n_features, n_features))  # Within-class scatter matrix
    S_b = np.zeros((n_features, n_features))  # Between-class scatter matrix

    # Compute the mean of the entire dataset
    overall_mean = np.mean(X, axis=0)

    for cls in classes:
        # Extract samples belonging to class 'cls'
        X_c = X[y == cls]
        n_c = X_c.shape[0]  # Number of samples in class 'cls'
        mean_c = np.mean(X_c, axis=0)  # Mean of class 'cls'

        # Compute within-class scatter for class 'cls'
        for i in range(n_c):
            x = (X_c.iloc[i] - mean_c).to_numpy()
            S_w += (x.reshape(-1, 1) * x) / n_samples

        # Compute between-class scatter for class 'cls'
        mean_diff = (mean_c - overall_mean).to_numpy()
        S_b += n_c * (mean_diff.reshape(-1, 1) * mean_diff) / n_samples

    # Compute the Fisher scores (diagonal of S_b / S_w)
    F_r = np.diag(S_b / S_w)
    F_r = np.nan_to_num(F_r, nan=0)

    return F_r



def principal_component_analysis(X):
    n_samples, n_features = X.shape
    S_t = np.zeros((n_features, n_features))  # Within-class scatter matrix

    # Compute the mean of the entire dataset
    overall_mean = np.mean(X, axis=0)

    for i in range(n_samples):
        x = (X.iloc[i] - overall_mean).to_numpy()
        S_t += (x.reshape(-1, 1) * x) / n_samples

    S_t = np.nan_to_num(S_t, nan=0)
    _, S, _ = scipy.linalg.svd(S_t)
    return S
    