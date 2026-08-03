import pandas as pd

airfoils = pd.read_csv("data/airfoils.csv")

# Normalize column names
airfoils.columns = [
    "name",
    "category",
    "mission",
    "cl",
    "cd",
    "ld",
    "stall",
    "description",
]


def recommend_airfoil(aircraft, mission):

    aircraft_map = {
        "Cargo Aircraft": "Cargo",
        "Fighter Jet": "Fighter",
        "Drone": "Drone",
        "Glider": "Glider",
    }

    aircraft = aircraft_map.get(aircraft, aircraft)

    match = airfoils[
        (airfoils["category"] == aircraft) &
        (airfoils["mission"] == mission)
    ]

    if not match.empty:
        return match.iloc[0]

    match = airfoils[
        airfoils["category"] == aircraft
    ]

    if not match.empty:
        return match.iloc[0]

    return airfoils.iloc[1]