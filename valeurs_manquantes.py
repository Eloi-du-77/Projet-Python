import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df_tous_pays=pd.read_pickle("df_tous_pays.pkl")

# # 3. Valeurs manquantes
# print("\n\n3. VALEURS MANQUANTES")
# print("-"*80)
# missing = df_tous_pays.isnull().sum()
# missing_pct = (df_tous_pays.isnull().sum() / len(df_tous_pays)) * 100
# missing_df = pd.DataFrame({
#     'Valeurs manquantes': missing,
#     'Pourcentage (%)': missing_pct
# })
# print(missing_df[missing_df['Valeurs manquantes'] > 0])

# Calculer le pourcentage de valeurs manquantes par colonne
df_olymp = df_tous_pays[df_tous_pays['annee'].isin([2012,2016,2020,2024])]
pourcentage_manquant = (df_olymp.isnull().sum() / len(df_olymp)) * 100

# Afficher les résultats
print("Pourcentage de valeurs manquantes par colonne :\n")
print(pourcentage_manquant)

# Optionnel : trier par ordre décroissant pour voir les colonnes les plus problématiques
print("\n--- Trié par ordre décroissant ---\n")
print(pourcentage_manquant.sort_values(ascending=False))

pays_sans_bronze = df_olymp[df_tous_pays['total_medailles_olympiques'].isnull()]

# Afficher les pays concernés
print(f"Nombre de pays sans donnée bronze_olympique : {len(pays_sans_bronze)}")
print("\nListe des pays :")
print(pays_sans_bronze["pays"], pays_sans_bronze["annee"])