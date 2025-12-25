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


# Le pays est considéré comme complet si il a une observation pour 2012, 2016 et 2020 et moins de 5 NaN
pays_complets = df_olympiques.groupby('pays').filter(
    lambda x: len(x) == len(annees_olympiques) and x.isna().sum().sum() <=5
)['pays'].unique()

#On crée une df df_filtre avec toutes les années mais que les pays complets
#df_olympiques_avec_2024 est utile ici
df_filtre = df_tous_pays[df_tous_pays['pays'].isin(pays_complets)]

#Calcul des scores moyens
moyennes_par_pays = df_filtre.groupby('pays').agg({
    'score_paralympique': 'mean',
    'athletes_paralympiques': 'mean'
}).reset_index()

moyennes_par_pays.columns = ['pays', 'score_moyen', 'athletes_moyen']

#Filtrer avec au moins 5 athlètes en moyenne
pays_qualifies = moyennes_par_pays[moyennes_par_pays['athletes_moyen'] >= 5]

#Trouver les 12 meilleurs pays
pays_qualifies = pays_qualifies.sort_values('score_moyen', ascending=False)
liste_top_12 = pays_qualifies.head(12)['pays'].tolist()

#Filtrer df_tous_pays pour ne garder que ces pays (toutes années confondues)
df_top_12 = df_tous_pays[df_tous_pays['pays'].isin(liste_top_12)]

if __name__ == '__main__':
    df_top_12.to_pickle("df_top_12_sans_NaN.pkl")