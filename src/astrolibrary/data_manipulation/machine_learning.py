import numpy as np
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix as sk_confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class MachineLearning:
    def __init__(self):
        self.model = Pipeline(
            [
                ("scalar", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(multi_class="auto", max_iter=1000),
                ),
            ]
        )

    def fit(self, A, b):
        # Check if the lengths of A and b are consistent
        if len(A) != len(b):
            raise ValueError("Input arrays should have the same length")

        # Check if both A and b are non-empty
        if len(A) > 0 and len(b) > 0:
            self.model.fit(A, b)
        else:
            # Handle the case of empty arrays
            raise ValueError("Input arrays are empty")

    def predict(self, A):
        if self.model:
            return self.model.predict(A)
        else:
            raise NotFittedError("Must train model by calling fit() first.")

    def predict_proba(self, A):
        if self.model:
            return self.model.predict_proba(A)
        else:
            raise NotFittedError("Must train model by calling fit() first.")

    def report_confusion_matrix(self, true_labels, predicted_labels):
        # Generate and return the confusion matrix
        return sk_confusion_matrix(true_labels, predicted_labels)
