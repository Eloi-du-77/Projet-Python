import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

df_tous_pays=pd.read_pickle("df_tous_pays.pkl")


# FILTRAGE AVEC QUE LE TOP 30 DES JEUX PARALYMPIQUES

# Filtrer les données entre 2012 et 2024
df_periode = df_tous_pays[(df_tous_pays['annee'] >= 2012) & (df_tous_pays['annee'] <= 2024)].copy()
print(f"Nombre de lignes dans df_periode: {len(df_periode)}")
print()

# Calculer le total cumulé de médailles paralympiques par pays sur la période
total_medailles_par_pays = df_periode.groupby('pays')['total_medailles_paralympiques'].sum().reset_index()
total_medailles_par_pays.columns = ['pays', 'total_cumule']

# Trier par total cumulé décroissant et garder le top 30
top_30_pays = total_medailles_par_pays.nlargest(30, 'total_cumule')['pays'].tolist()


# Filtrer le DataFrame original pour ne garder que les pays du top 30
# (conserve TOUTES les années pour ces pays)
df_top_30 = df_tous_pays[df_tous_pays['pays'].isin(top_30_pays)].copy()

print(f"Nombre total de lignes : {len(df_tous_pays)}")
print("\nTop 30 des pays (par médailles paralympiques cumulées 2012-2024) :")
for i, pays in enumerate(top_30_pays, 1):
    total = total_medailles_par_pays[total_medailles_par_pays['pays'] == pays]['total_cumule'].values[0]
    print(f"{i}. {pays}: {int(total)} médailles")

df_top_30.to_pickle("df_top_30.pkl")

#FILTRAGE AVEC QUE LE TOP 10

top_10_pays = total_medailles_par_pays.nlargest(10, 'total_cumule')['pays'].tolist()


# Filtrer le DataFrame original pour ne garder que les pays du top 10
# (conserve TOUTES les années pour ces pays)
df_top_10 = df_tous_pays[df_tous_pays['pays'].isin(top_10_pays)].copy()

print(f"Nombre total de lignes : {len(df_tous_pays)}")
print("\nTop 10 des pays (par médailles paralympiques cumulées 2012-2024) :")
for i, pays in enumerate(top_10_pays, 1):
    total = total_medailles_par_pays[total_medailles_par_pays['pays'] == pays]['total_cumule'].values[0]
    print(f"{i}. {pays}: {int(total)} médailles")

df_top_10.to_pickle("df_top_10.pkl")



# # 1. Statistiques de base
# print("\n1. STATISTIQUES DE BASE (colonnes numériques)")
# print("-"*80)
# print(df_tous_pays.describe())

# # 2. Informations générales sur le DataFrame
# print("\n\n2. INFORMATIONS GÉNÉRALES")
# print("-"*80)
# print(f"Nombre de lignes : {len(df_tous_pays)}")
# print(f"Nombre de colonnes : {len(df_tous_pays.columns)}")
