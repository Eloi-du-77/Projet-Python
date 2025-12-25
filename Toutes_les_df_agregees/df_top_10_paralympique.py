import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

df_tous_pays=pd.read_pickle("df_tous_pays.pkl")

# FILTRAGE AVEC QUE LE TOP 10 DES JEUX PARALYMPIQUES

# Calculer le total cumulé des scores paralympiques par pays sur la période
moyennes_par_pays = df_tous_pays.groupby('pays').agg({
    'score_paralympique': 'mean',
    'athletes_paralympiques': 'mean'
}).reset_index()

moyennes_par_pays.columns = ['pays', 'score_moyen', 'athletes_moyen']

#Sélection du top 10 en excluant les pays avec en moyenne moins de cinq athlètes
pays_qualifies = moyennes_par_pays[moyennes_par_pays['athletes_moyen'] >= 5]

pays_qualifies = pays_qualifies.sort_values('score_moyen', ascending=False)

top_pays = pays_qualifies.head(10)['pays'].tolist()

# Filtrer le DataFrame original pour ne garder que les pays du top 10
# (conserve TOUTES les années pour ces pays)
df_top_10 = df_tous_pays[df_tous_pays['pays'].isin(top_pays)]

if __name__ == '__main__' :
    df_top_10.to_pickle("df_top_10.pkl")
