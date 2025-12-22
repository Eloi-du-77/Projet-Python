import numpy as np
import pandas as pd

df_tous_pays=pd.read_pickle("df_tous_pays.pkl")

#On veut faire une sélection de pays avec très peu de NaN et quand même performants aux jeux paralympiques
# Donc on va faire le top 12 des pays avec moins de 5 NaN

# Définition des années olympiques (il y a beaucoup de NaN en 2024 donc on ne le prend pas en compte pour le top 12)
annees_olympiques = [2012, 2016, 2020]
annees_olympiques_avec_2024 = [2012,2016,2020,2024]

# Filtration des années olympiques (avec et sans 2024)
df_olympiques = df_tous_pays[df_tous_pays['annee'].isin(annees_olympiques)]
df_olympiques_avec_2024 = df_tous_pays[df_tous_pays['annee'].isin(annees_olympiques_avec_2024)]


# Le pays est considéré comme complet si il a une observation pour 2012, 2016 et 2020 et aucun NaN
pays_complets = df_olympiques.groupby('pays').filter(
    lambda x: len(x) == len(annees_olympiques) and x.isna().sum().sum() <=5
)['pays'].unique()

#On crée une df df_filtre avec toutes les années mais que les pays complets
#df_olympiques_avec_2024 est utile ici
df_filtre = df_olympiques_avec_2024[df_olympiques_avec_2024['pays'].isin(pays_complets)]

# Calculer le score olympique moyen par pays
scores_moyens = df_filtre.groupby('pays')['score_paralympique'].mean().sort_values(ascending=False)

# Garder les 12 meilleurs pays
top_12_pays = scores_moyens.head(12).index
df_top12 = df_filtre[df_filtre['pays'].isin(top_12_pays)]

print(f"Top 12 pays : {list(top_12_pays)}")
print(f"Nombre de lignes : {len(df_top12)}")
print(df_top12)
df_top12.to_pickle("df_top_12_sans_NaN.pkl")