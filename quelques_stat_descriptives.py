# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df_tous_pays=pd.read_pickle("df_tous_pays.pkl")

# # Vérifier les colonnes disponibles
# print("Colonnes disponibles dans df_tous_pays:")
# print(df_tous_pays.columns.tolist())
# print()

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
df_tous_pays = df_tous_pays[df_tous_pays['pays'].isin(top_30_pays)].copy()

print(f"Nombre de pays conservés : {df_tous_pays['pays'].nunique()}")
print(f"Nombre total de lignes : {len(df_tous_pays)}")
print(f"Années présentes : {sorted(df_tous_pays['annee'].unique())}")
print("\nTop 30 des pays (par médailles paralympiques cumulées 2012-2024) :")
for i, pays in enumerate(top_30_pays, 1):
    total = total_medailles_par_pays[total_medailles_par_pays['pays'] == pays]['total_cumule'].values[0]
    print(f"{i}. {pays}: {int(total)} médailles")


# 1. Statistiques de base
print("\n1. STATISTIQUES DE BASE (colonnes numériques)")
print("-"*80)
print(df_tous_pays.describe())

# 2. Informations générales sur le DataFrame
print("\n\n2. INFORMATIONS GÉNÉRALES")
print("-"*80)
print(f"Nombre de lignes : {len(df_tous_pays)}")
print(f"Nombre de colonnes : {len(df_tous_pays.columns)}")

# 3. Valeurs manquantes
print("\n\n3. VALEURS MANQUANTES")
print("-"*80)
missing = df_tous_pays.isnull().sum()
missing_pct = (df_tous_pays.isnull().sum() / len(df_tous_pays)) * 100
missing_df = pd.DataFrame({
    'Valeurs manquantes': missing,
    'Pourcentage (%)': missing_pct
})
print(missing_df[missing_df['Valeurs manquantes'] > 0])

# # 4. Statistiques supplémentaires pour colonnes numériques
# print("\n\n4. STATISTIQUES DÉTAILLÉES (colonnes numériques)")
# print("-"*80)
# numeric_cols = df_tous_pays.select_dtypes(include=[np.number]).columns
# for col in numeric_cols:
#     print(f"\n{col}:")
#     print(f"  Moyenne : {df_tous_pays[col].mean():.4f}")
#     print(f"  Médiane : {df_tous_pays[col].median():.4f}")
#     print(f"  Écart-type : {df_tous_pays[col].std():.4f}")
#     print(f"  Min : {df_tous_pays[col].min():.4f}")
#     print(f"  Max : {df_tous_pays[col].max():.4f}")
#     print(f"  Q1 (25%) : {df_tous_pays[col].quantile(0.25):.4f}")
#     print(f"  Q3 (75%) : {df_tous_pays[col].quantile(0.75):.4f}")
#     print(f"  Valeurs uniques : {df_tous_pays[col].nunique()}")

