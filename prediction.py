import joblib
import numpy as np


def predict(data):
    clf = joblib.load("best_reg.sav.gz")

    return clf.predict(data)