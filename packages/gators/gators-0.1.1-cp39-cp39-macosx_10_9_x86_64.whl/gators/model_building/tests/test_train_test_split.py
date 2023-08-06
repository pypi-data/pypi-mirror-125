# License: Apache-2.0
from gators.model_building.train_test_split import TrainTestSplit
import pytest
import numpy as np
import pandas as pd
import databricks.koalas as ks


@pytest.fixture()
def data_ordered():
    X = pd.DataFrame(np.arange(40).reshape(8, 5), columns=list("ABCDE"))
    y_name = "TARGET"
    y = pd.Series([0, 1, 2, 0, 1, 2, 0, 1], name=y_name)
    test_ratio = 0.5
    obj = TrainTestSplit(test_ratio=test_ratio, strategy="ordered")
    X_train_expected = pd.DataFrame(
        {
            "A": {0: 0, 1: 5, 2: 10, 3: 15},
            "B": {0: 1, 1: 6, 2: 11, 3: 16},
            "C": {0: 2, 1: 7, 2: 12, 3: 17},
            "D": {0: 3, 1: 8, 2: 13, 3: 18},
            "E": {0: 4, 1: 9, 2: 14, 3: 19},
        }
    )
    X_test_expected = pd.DataFrame(
        {
            "A": {4: 20, 5: 25, 6: 30, 7: 35},
            "B": {4: 21, 5: 26, 6: 31, 7: 36},
            "C": {4: 22, 5: 27, 6: 32, 7: 37},
            "D": {4: 23, 5: 28, 6: 33, 7: 38},
            "E": {4: 24, 5: 29, 6: 34, 7: 39},
        }
    )
    y_train_expected = pd.Series({0: 0, 1: 1, 2: 2, 3: 0}, name=y_name)
    y_test_expected = pd.Series({4: 1, 5: 2, 6: 0, 7: 1}, name=y_name)
    return (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    )


@pytest.fixture()
def data_random():
    X = pd.DataFrame(np.arange(40).reshape(8, 5), columns=list("ABCDE"))
    y_name = "TARGET"
    y = pd.Series([0, 1, 2, 0, 1, 2, 0, 1], name=y_name)
    test_ratio = 0.5
    obj = TrainTestSplit(test_ratio=test_ratio, strategy="random", random_state=0)
    X_train_expected = pd.DataFrame(
        {
            "A": {0: 0, 3: 15, 4: 20, 5: 25},
            "B": {0: 1, 3: 16, 4: 21, 5: 26},
            "C": {0: 2, 3: 17, 4: 22, 5: 27},
            "D": {0: 3, 3: 18, 4: 23, 5: 28},
            "E": {0: 4, 3: 19, 4: 24, 5: 29},
        }
    )
    X_test_expected = pd.DataFrame(
        {
            "A": {6: 30, 2: 10, 1: 5, 7: 35},
            "B": {6: 31, 2: 11, 1: 6, 7: 36},
            "C": {6: 32, 2: 12, 1: 7, 7: 37},
            "D": {6: 33, 2: 13, 1: 8, 7: 38},
            "E": {6: 34, 2: 14, 1: 9, 7: 39},
        }
    )
    y_train_expected = pd.Series({0: 0, 3: 0, 4: 1, 5: 2}, name=y_name)
    y_test_expected = pd.Series({6: 0, 2: 2, 1: 1, 7: 1}, name=y_name)
    return (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    )


@pytest.fixture()
def data_stratified():
    X = pd.DataFrame(np.arange(40).reshape(8, 5), columns=list("ABCDE"))
    y_name = "TARGET"
    y = pd.Series([0, 1, 2, 0, 1, 2, 0, 1], name=y_name)
    test_ratio = 0.5
    obj = TrainTestSplit(test_ratio=test_ratio, strategy="stratified", random_state=0)

    X_train_expected = pd.DataFrame(
        {
            "A": {0: 0, 1: 5, 2: 10},
            "B": {0: 1, 1: 6, 2: 11},
            "C": {0: 2, 1: 7, 2: 12},
            "D": {0: 3, 1: 8, 2: 13},
            "E": {0: 4, 1: 9, 2: 14},
        }
    )
    X_test_expected = pd.DataFrame(
        {
            "A": {6: 30, 3: 15, 7: 35, 4: 20, 5: 25},
            "B": {6: 31, 3: 16, 7: 36, 4: 21, 5: 26},
            "C": {6: 32, 3: 17, 7: 37, 4: 22, 5: 27},
            "D": {6: 33, 3: 18, 7: 38, 4: 23, 5: 28},
            "E": {6: 34, 3: 19, 7: 39, 4: 24, 5: 29},
        }
    )
    y_train_expected = pd.Series({0: 0, 1: 1, 2: 2}, name=y_name)
    y_test_expected = pd.Series({6: 0, 3: 0, 7: 1, 4: 1, 5: 2}, name=y_name)
    return (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    )


@pytest.fixture()
def data_ordered_ks():
    X = ks.DataFrame(np.arange(40).reshape(8, 5), columns=list("ABCDE"))
    y_name = "TARGET"
    y = ks.Series([0, 1, 2, 0, 1, 2, 0, 1], name=y_name)
    test_ratio = 0.5
    obj = TrainTestSplit(test_ratio=test_ratio, strategy="ordered")
    X_train_expected = pd.DataFrame(
        {
            "A": {0: 0, 1: 5, 2: 10, 3: 15},
            "B": {0: 1, 1: 6, 2: 11, 3: 16},
            "C": {0: 2, 1: 7, 2: 12, 3: 17},
            "D": {0: 3, 1: 8, 2: 13, 3: 18},
            "E": {0: 4, 1: 9, 2: 14, 3: 19},
        }
    )
    X_test_expected = pd.DataFrame(
        {
            "A": {4: 20, 5: 25, 6: 30, 7: 35},
            "B": {4: 21, 5: 26, 6: 31, 7: 36},
            "C": {4: 22, 5: 27, 6: 32, 7: 37},
            "D": {4: 23, 5: 28, 6: 33, 7: 38},
            "E": {4: 24, 5: 29, 6: 34, 7: 39},
        }
    )
    y_train_expected = pd.Series({0: 0, 1: 1, 2: 2, 3: 0}, name=y_name)
    y_test_expected = pd.Series({4: 1, 5: 2, 6: 0, 7: 1}, name=y_name)
    return (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    )


@pytest.fixture()
def data_random_ks():
    X = ks.DataFrame(np.arange(40).reshape(8, 5), columns=list("ABCDE"))
    y_name = "TARGET"
    y = ks.Series([0, 1, 2, 0, 1, 2, 0, 1], name=y_name)
    test_ratio = 0.5
    obj = TrainTestSplit(test_ratio=test_ratio, strategy="random", random_state=0)
    X_train_expected = pd.DataFrame(
        {
            "A": {0: 0, 7: 35, 3: 15, 2: 10},
            "B": {0: 1, 7: 36, 3: 16, 2: 11},
            "C": {0: 2, 7: 37, 3: 17, 2: 12},
            "D": {0: 3, 7: 38, 3: 18, 2: 13},
            "E": {0: 4, 7: 39, 3: 19, 2: 14},
        }
    )
    X_test_expected = pd.DataFrame(
        {
            "A": {6: 30, 5: 25, 1: 5, 4: 20},
            "B": {6: 31, 5: 26, 1: 6, 4: 21},
            "C": {6: 32, 5: 27, 1: 7, 4: 22},
            "D": {6: 33, 5: 28, 1: 8, 4: 23},
            "E": {6: 34, 5: 29, 1: 9, 4: 24},
        }
    )
    y_train_expected = pd.Series({0: 0, 7: 1, 3: 0, 2: 2}, name=y_name)
    y_test_expected = pd.Series({6: 0, 5: 2, 1: 1, 4: 1}, name=y_name)
    return (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    )


@pytest.fixture()
def data_stratified_ks():
    X = ks.DataFrame(np.arange(40).reshape(8, 5), columns=list("ABCDE"))
    y_name = "TARGET"
    y = ks.Series([0, 1, 2, 0, 1, 2, 0, 1], name=y_name)
    test_ratio = 0.5
    obj = TrainTestSplit(test_ratio=test_ratio, strategy="stratified", random_state=0)
    X_train_expected = pd.DataFrame(
        {
            "A": {0: 0, 3: 15, 7: 35, 2: 10},
            "B": {0: 1, 3: 16, 7: 36, 2: 11},
            "C": {0: 2, 3: 17, 7: 37, 2: 12},
            "D": {0: 3, 3: 18, 7: 38, 2: 13},
            "E": {0: 4, 3: 19, 7: 39, 2: 14},
        }
    )
    X_test_expected = pd.DataFrame(
        {
            "A": {6: 30, 1: 5, 4: 20, 5: 25},
            "B": {6: 31, 1: 6, 4: 21, 5: 26},
            "C": {6: 32, 1: 7, 4: 22, 5: 27},
            "D": {6: 33, 1: 8, 4: 23, 5: 28},
            "E": {6: 34, 1: 9, 4: 24, 5: 29},
        }
    )
    y_train_expected = pd.Series({0: 0, 3: 0, 7: 1, 2: 2}, name=y_name)
    y_test_expected = pd.Series({6: 0, 1: 1, 4: 1, 5: 2}, name=y_name)
    return (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    )


def test_ordered(data_ordered):
    (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    ) = data_ordered
    X_train, X_test, y_train, y_test = obj.transform(X, y)
    assert X_train.shape == X_train_expected.shape
    assert X_test.shape == X_test_expected.shape
    assert y_train.shape == y_train_expected.shape
    assert y_test.shape == y_test_expected.shape

@pytest.mark.koalas
def test_ordered_ks(data_ordered_ks):
    (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    ) = data_ordered_ks
    X_train, X_test, y_train, y_test = obj.transform(X, y)
    assert X_train.shape == X_train_expected.shape
    assert X_test.shape == X_test_expected.shape
    assert y_train.shape == y_train_expected.shape
    assert y_test.shape == y_test_expected.shape

def test_random(data_random):
    (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    ) = data_random
    X_train, X_test, y_train, y_test = obj.transform(X, y)
    assert X_train.shape == X_train_expected.shape
    assert X_test.shape == X_test_expected.shape
    assert y_train.shape == y_train_expected.shape
    assert y_test.shape == y_test_expected.shape

@pytest.mark.koalas
def test_random_ks(data_random_ks):
    (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    ) = data_random_ks
    X_train, X_test, y_train, y_test = obj.transform(X, y)
    assert X_train.to_pandas().shape == X_train_expected.shape
    assert X_test.to_pandas().shape == X_test_expected.shape
    assert y_train.to_pandas().shape == y_train_expected.shape
    assert y_test.to_pandas().shape == y_test_expected.shape


def test_stratified(data_stratified):
    (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    ) = data_stratified
    X_train, X_test, y_train, y_test = obj.transform(X, y)
    assert X_train.shape == X_train_expected.shape
    assert X_test.shape == X_test_expected.shape
    assert y_train.shape == y_train_expected.shape
    assert y_test.shape == y_test_expected.shape


@pytest.mark.koalas
def test_stratified_ks(data_stratified_ks):
    (
        obj,
        X,
        y,
        X_train_expected,
        X_test_expected,
        y_train_expected,
        y_test_expected,
    ) = data_stratified_ks
    X_train, X_test, y_train, y_test = obj.transform(X, y)
    X_train_shape = X_train.to_pandas().shape
    X_test_shape = X_test.to_pandas().shape
    y_train_shape = y_train.to_pandas().shape
    y_test_shape = y_test.to_pandas().shape
    assert X_train_shape[0]+ X_test_shape[0]== X.shape[0]
    assert y_train_shape[0]+ y_test_shape[0]== y.shape[0]
    assert X_train_shape[1] == X.shape[1] - 1
    assert X_test_shape[1] == X.shape[1] - 1


def test_imputers_stategy():
    with pytest.raises(TypeError):
        _ = TrainTestSplit(test_ratio="q", random_state="q", strategy="q")
    with pytest.raises(TypeError):
        _ = TrainTestSplit(test_ratio="q", random_state="q", strategy="q")
    with pytest.raises(TypeError):
        _ = TrainTestSplit(test_ratio=0.1, random_state="q", strategy="q")
    with pytest.raises(TypeError):
        _ = TrainTestSplit(test_ratio=0.1, random_state=0, strategy=0)
    with pytest.raises(ValueError):
        _ = TrainTestSplit(test_ratio=0.1, random_state=0, strategy="q")
