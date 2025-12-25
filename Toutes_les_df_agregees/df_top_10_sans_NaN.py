import numpy as np
import pandas as pd

df_tous_pays=pd.read_pickle("df_tous_pays.pkl")

#On veut faire une sélection de pays avec très peu de NaN et quand même performants aux jeux paralympiques
# Donc on va faire le top 10 des pays avec moins de 5  lors des années olympiques

# Définition des années olympiques (il y a beaucoup de NaN en 2024 donc on ne le prend pas en compte pour le top 10)
annees_olympiques = [2012, 2016, 2020]

# Filtration des années olympiques (avec et sans 2024)
df_olympiques = df_tous_pays[df_tous_pays['annee'].isin(annees_olympiques)]

# Le pays est considéré comme complet si il a une observation pour 2010, 2016 et 2020 et moins de 5 NaN
pays_complets = df_olympiques.groupby('pays').filter(
    lambda x: len(x) == len(annees_olympiques) and x.isna().sum().sum() <=5
)['pays'].unique()
#On crée une df df_filtre avec toutes les années mais que les pays complets
df_filtre = df_tous_pays[df_tous_pays['pays'].isin(pays_complets)]

#Calcul des pib moyens et du nombre d'athlète moyen
moyennes_par_pays = df_filtre.groupby('pays').agg({
    'pib_habitant': 'mean',
    'athletes_paralympiques': 'mean'
}).reset_index()

moyennes_par_pays.columns = ['pays', 'pib_habitant', 'athletes_moyen']

#Filtrer avec au moins 5 athlètes en moyenne
pays_qualifies = moyennes_par_pays[moyennes_par_pays['athletes_moyen'] >= 5]

#Trouver les 10 meilleurs pays
pays_qualifies = pays_qualifies.sort_values('pib_habitant', ascending=False)
liste_top_10 = pays_qualifies.head(10)['pays'].tolist()

#Filtrer df_tous_pays pour ne garder que ces pays (toutes années confondues)
df_top_10 = df_tous_pays[df_tous_pays['pays'].isin(liste_top_10)]

if __name__ == '__main__':
    df_top_10.to_pickle("df_top_10_sans_NaN.pkl")