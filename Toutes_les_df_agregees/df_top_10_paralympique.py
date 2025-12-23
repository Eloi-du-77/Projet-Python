import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

df_tous_pays=pd.read_pickle("df_tous_pays.pkl")

print(df_tous_pays[(df_tous_pays['pays'] == 'Russie') & 
                   (df_tous_pays['annee'].isin([2012, 2016, 2020, 2024]))]['total_medailles_olympiques'])

# FILTRAGE AVEC QUE LE TOP 10 DES JEUX PARALYMPIQUES

# Filtrage des données entre 2012 et 2024
df_periode = df_tous_pays[(df_tous_pays['annee'] >= 2012) & (df_tous_pays['annee'] <= 2024)].copy()
print(f"Nombre de lignes dans df_periode: {len(df_periode)}")
print()

# Calculer le total cumulé de médailles paralympiques par pays sur la période
total_medailles_par_pays = df_periode.groupby('pays')['total_medailles_paralympiques'].sum().reset_index()
total_medailles_par_pays.columns = ['pays', 'total_cumule']
#Convertir la colonne en type numérique
total_medailles_par_pays['total_cumule'] = pd.to_numeric(total_medailles_par_pays['total_cumule'], errors='coerce')


#Sélection du top 10
top_10_pays = total_medailles_par_pays.nlargest(10, 'total_cumule')['pays'].tolist()

# Filtrer le DataFrame original pour ne garder que les pays du top 10
# (conserve TOUTES les années pour ces pays)
df_top_10 = df_tous_pays[df_tous_pays['pays'].isin(top_10_pays)].copy()

#Ne conserver que certaines colonnes
# Sélectionner uniquement les colonnes spécifiées
colonnes_a_garder = [
    'pays',
    'annee',
    'or_olympique',
    'argent_olympique',
    'bronze_olympique',
    'total_medailles_olympiques',
    'or_paralympique',
    'argent_paralympique',
    'bronze_paralympique',
    'total_medailles_paralympiques',
    'or_olympique_par_athlete',
    'argent_olympique_par_athlete',
    'bronze_olympique_par_athlete',
    'total_medailles_olympiques_par_athlete',
    'or_paralympique_par_athlete',
    'argent_paralympique_par_athlete',
    'bronze_paralympique_par_athlete',
    'total_medailles_paralympiques_par_athlete',
    'score_olympique',
    'score_paralympique',
    'moy_amenagement_1995',
    'moy_maladie_1995',
    'moy_loisirs_1995',
    'moy_education_1995',
    'pib_habitant',
    'idh'
]

df_top_10 = df_top_10[colonnes_a_garder]

#Ne conserver que les annees olympiques
df_top_10 = df_top_10[df_top_10['annee'].isin([2012, 2016, 2020, 2024])]

print(f"Nombre total de lignes : {len(df_tous_pays)}")
print("\nTop 10 des pays (par médailles paralympiques cumulées 2012-2024) :")
for i, pays in enumerate(top_10_pays, 1):
    total = total_medailles_par_pays[total_medailles_par_pays['pays'] == pays]['total_cumule'].values[0]
    print(f"{i}. {pays}: {int(total)} médailles")

df_top_10.to_pickle("df_top_10.pkl")
