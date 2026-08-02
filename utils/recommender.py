import pandas as pd

airfoils = pd.read_csv("data/airfoils.csv")


def recommend_airfoil(aircraft, mission):
    """
    Returns the best matching airfoil.
    """

    # Aircraft + Mission matching

    if aircraft == "Drone":

        if mission == "Surveillance":
            return airfoils.iloc[0]

        elif mission == "Delivery":
            return airfoils.iloc[5]

    if aircraft == "Cargo Aircraft":
        return airfoils.iloc[2]

    if aircraft == "Glider":
        return airfoils.iloc[3]

    if aircraft == "Fighter Jet":
        return airfoils.iloc[4]

    return airfoils.iloc[1]