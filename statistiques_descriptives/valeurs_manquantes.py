import pandas as pd
import numpy as np


pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

#Ce programme a pour objectif d'afficher le pourcentage de valeurs manquantes pour chaque variable
df_tous_pays=pd.read_pickle("../Toutes_les_df_agregees/df_tous_pays.pkl")
df_top_10=pd.read_pickle("../Toutes_les_df_agregees/df_top_10.pkl")

#Calculer le pourcentage de valeurs manquantes dans les années olympiques pour la table totale et la table que avec le top 10
df_olymp = df_tous_pays[df_tous_pays['annee'].isin([2012,2016,2020,2024])]
pourcentage_manquant = (df_olymp.isnull().sum() / len(df_olymp)) * 100

pourcentage_manquant_10 = (df_top_10.isnull().sum() / len(df_top_10)) * 100

print("Pourcentage de valeurs manquantes par colonne de df_tous_pays :\n")
print(pourcentage_manquant.sort_values(ascending=False))

print("Pourcentage de valeurs manquantes par colonne de df_top_10 :\n")
print(pourcentage_manquant_10.sort_values(ascending=False))