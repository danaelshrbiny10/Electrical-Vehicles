"""
Train small synthetic models and save them to src/models/saved/*.pkl

Run:
    python src/pipelines/train_all.py
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import joblib
from infer.helpers import model_path, save_model

def gen_consumption(n=20000, seed=0):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "distance": rng.uniform(1, 400, n),
            "speed": rng.uniform(30, 130, n),
            "temp": rng.uniform(-10, 40, n),
            "ac": rng.integers(0, 2, n),
            "heater": rng.integers(0, 2, n),
            "payload": rng.uniform(50, 300, n),
            "battery_kwh": rng.uniform(40, 120, n),
            "eff": rng.normal(0.17, 0.03, n),
        }
    )
    # physics + heuristics
    df["energy"] = (
        df["distance"]
        * df["eff"]
        * (1 + (df["speed"] - 80) / 500)
        * (1 + df["ac"] * 0.05 + df["heater"] * 0.04)
        * (1 + (df["payload"] - 100) / 2000)
    )
    return df


def gen_charging(n=15000, seed=1):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "soc_from": rng.uniform(5, 50, n),
            "soc_to": rng.uniform(60, 100, n),
            "battery_kwh": rng.uniform(40, 120, n),
            "power_kw": rng.uniform(20, 250, n),
        }
    )
    soc_diff = (df["soc_to"] - df["soc_from"]) / 100
    # minutes with taper near high soc
    df["minutes"] = (
        (df["battery_kwh"] * soc_diff / df["power_kw"])
        * 60
        * (1 + (df["soc_to"] - 70) / 200)
    )
    return df


def gen_health(n=8000, seed=2):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "cycles": rng.uniform(50, 3000, n),
            "avg_temp": rng.uniform(5, 45, n),
            "fast_charge_ratio": rng.uniform(0, 1, n),
        }
    )
    df["degradation"] = (
        (df["cycles"] / 100)
        + (df["avg_temp"] - 25) * 0.3
        + df["fast_charge_ratio"] * 7
        + rng.normal(0, 2, n)
    )
    return df


def train_and_save():
    # consumption model
    dfc = gen_consumption()
    Xc = dfc[
        ["distance", "speed", "temp", "ac", "heater", "payload", "battery_kwh", "eff"]
    ]
    yc = dfc["energy"]
    lr = LinearRegression().fit(Xc, yc)
    save_model(lr, "consumption.pkl")
    print("saved consumption.pkl")

    # charging model
    dfch = gen_charging()
    Xch = dfch[["soc_from", "soc_to", "battery_kwh", "power_kw"]]
    ych = dfch["minutes"]
    Xtr, Xte, ytr, yte = train_test_split(Xch, ych, test_size=0.2, random_state=0)
    mlp = MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=300, random_state=0)
    mlp.fit(Xtr, ytr)
    save_model(mlp, "charging.pkl")
    print("saved charging.pkl")

    # health model
    dfh = gen_health()
    Xh = dfh[["cycles", "avg_temp", "fast_charge_ratio"]]
    yh = dfh["degradation"]
    lrh = LinearRegression().fit(Xh, yh)
    save_model(lrh, "health.pkl")
    print("saved health.pkl")


if __name__ == "__main__":
    train_and_save()
