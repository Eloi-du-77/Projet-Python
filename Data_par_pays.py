#!/opt/python/bin/python3.13

import pandas as pd

YEARS = [2012, 2016, 2020, 2024]

# Totaux des médailles paralympiques pour les pays sélectionnés
data = {
    "France":        [34, 28, 55, 54],
    "Germany":       [101, 88, 57, 46],
    "United Kingdom":[120, 121, 124, 103],
    "Netherlands":   [39, 62, 59, 56],
    "Norway":        [18, 8, 4, 7],
    "United States": [98, 121, 104, 138],
    "China":         [231, 239, 207, 205],
    "Ukraine":       [117, 117, 98, 82],
    "Turkey":        [9, 9, 15, 28],
    "Japan":         [10, 24, 51, 33],
}

df = pd.DataFrame(data, index=YEARS).T
df.to_csv("paralympics_medals_selected_countries.csv")
print("✅ CSV généré : paralympics_medals_selected_countries.csv")
print(df)