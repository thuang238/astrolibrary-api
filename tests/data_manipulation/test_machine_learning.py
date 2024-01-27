import numpy as np
import pytest
from sklearn.exceptions import NotFittedError

from astrolibrary import MachineLearning


@pytest.fixture
def machine_learning_model():
    return MachineLearning()


def test_fit_valid_case(machine_learning_model):
    # Create dummy data for testing
    A = np.array([[1, 2], [3, 4], [5, 6]])
    b = np.array([0, 1, 0])

    # Ensure fit function doesn't raise errors
    machine_learning_model.fit(A, b)


def test_fit_not_valid_case(machine_learning_model):
    # Create dummy data for testing
    A = np.array([[1, 2], [3, 4]])
    b = np.array([0, 1, 0])  # Mismatched length

    # Ensure fit function raises ValueError for not valid case
    with pytest.raises(
        ValueError, match="Input arrays should have the same length"
    ):
        machine_learning_model.fit(A, b)


def test_predict_not_fitted(machine_learning_model):
    # Create dummy data for testing
    A = np.array([[1, 2], [3, 4], [5, 6]])

    # Ensure predict function raises NotFittedError when the model is not fitted
    with pytest.raises(NotFittedError):
        machine_learning_model.predict(A)


def test_predict_valid_case(machine_learning_model):
    # Create dummy data for testing
    A = np.array([[1, 2], [3, 4], [5, 6]])
    b = np.array([0, 1, 0])

    # Fit the model
    machine_learning_model.fit(A, b)

    # Ensure predict function works for valid case
    result = machine_learning_model.predict(A)
    assert result.shape == (
        3,
    )  # Adjust the shape based on your expected output


def test_predict_proba_not_fitted(machine_learning_model):
    # Create dummy data for testing
    A = np.array([[1, 2], [3, 4], [5, 6]])

    # Ensure predict_proba function raises NotFittedError when the model is not fitted
    with pytest.raises(NotFittedError):
        machine_learning_model.predict_proba(A)


def test_predict_proba_valid_case(machine_learning_model):
    # Create dummy data for testing
    A = np.array([[1, 2], [3, 4], [5, 6]])
    b = np.array([0, 1, 0])

    # Fit the model
    machine_learning_model.fit(A, b)

    # Ensure predict_proba function works for valid case
    result = machine_learning_model.predict_proba(A)
    assert result.shape == (
        3,
        2,
    )  # Adjust the shape based on your expected output


def test_fit_edge_cases(machine_learning_model):
    # Test with empty array for A
    with pytest.raises(
        ValueError, match="Input arrays should have the same length"
    ):
        machine_learning_model.fit(np.array([]), np.array([1, 2]))

    # Test with empty array for b
    with pytest.raises(
        ValueError, match="Input arrays should have the same length"
    ):
        machine_learning_model.fit(np.array([[1, 2], [3, 4]]), np.array([]))


def test_confusion_matrix_valid_case(machine_learning_model):
    # Create dummy data for testing
    A = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    b = np.array([0, 1, 0, 1])  # True labels

    # Fit the model
    machine_learning_model.fit(A, b)

    # Predict the labels
    predictions = machine_learning_model.predict(A)

    # Generate confusion matrix
    confusion_matrix = machine_learning_model.report_confusion_matrix(
        b, predictions
    )

    # Check the shape of the confusion matrix
    assert confusion_matrix.shape == (
        2,
        2,
    ), "Confusion matrix should be 2x2 for binary classification"
