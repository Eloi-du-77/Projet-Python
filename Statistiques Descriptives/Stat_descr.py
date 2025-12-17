from Création_df_propre_et_complète import *
import pandas as pd
import numpy as np

# Copier le DataFrame pour travailler dessus
df = df_merge.copy()

# Nombre total de valeurs attendues
# Si chaque pays avait une valeur pour chaque année
n_pays = df['pays'].nunique()
n_annees = df['annee'].nunique()
total_attendu = n_pays * n_annees

# Construire un DataFrame de comptage
compte_valeurs = pd.DataFrame({
    'valeurs_presentes': df.count(),
    'valeurs_totales_attendues': total_attendu
})

# Ajouter une colonne avec le pourcentage de remplissage
compte_valeurs['pourcentage_rempli'] = compte_valeurs['valeurs_presentes'] / compte_valeurs['valeurs_totales_attendues'] * 100

# Affichage
print(compte_valeurs)

df_corr = df.copy()

# Colonnes résultats JO
cols_jo = [
    'or_olympique', 'argent_olympique', 'bronze_olympique', 'total_medailles_olympiques',
    'or_paralympique', 'argent_paralympique', 'bronze_paralympique', 'total_medailles_paralympiques'
]

# Colonnes autres variables numériques
cols_autres = [c for c in df_corr.columns if df_corr[c].dtype in [np.float64, np.int64] and c not in cols_jo]

# Années des JO
annees_jo = sorted(df_corr['annee'].unique())

# Calcul des moyennes cumulées avant chaque année pour chaque pays et chaque variable
df_moyennes = df_corr.groupby('pays').apply(
    lambda g: g.sort_values('annee').assign(
        **{f'{col}_moy_avant': g[col].expanding().mean().shift(1) for col in cols_autres}
    )
).reset_index(drop=True)

# Garde uniquement les années de JO
df_corr = df_moyennes[df_moyennes['annee'].isin(annees_jo)].copy()

# Colonnes pour corrélation
cols_corr = cols_jo + [c+'_moy_avant' for c in cols_autres]

# Calcul de la matrice de corrélation
matrice_corr = df_corr[cols_corr].corr().round(3)  # arrondi à 3 décimales

# Raccourcir les noms de colonnes pour affichage
renoms = {
    'or_olympique':'Or_O',
    'argent_olympique':'Arg_O',
    'bronze_olympique':'Bro_O',
    'total_medailles_olympiques':'Tot_O',
    'or_paralympique':'Or_P',
    'argent_paralympique':'Arg_P',
    'bronze_paralympique':'Bro_P',
    'total_medailles_paralympiques':'Tot_P'
}
# Ajouter les autres variables moyennes
for c in cols_autres:
    renoms[c+'_moy_avant'] = c[:10] + '_moy'  # tronquer à 10 caractères max + _moy

matrice_corr.rename(index=renoms, columns=renoms, inplace=True)

# Affichage explicatif
print("==== MATRICE DE CORRÉLATION (valeurs arrondies et noms raccourcis) ====\n")
print("Logique de calcul :")
print("- Les colonnes de résultats olympiques/paralympiques ne sont disponibles que tous les 4 ans (années de JO).")
print("- La corrélation est calculée entre le résultat de l'année x et la moyenne des autres variables sur toutes les années précédentes.\n")

print(matrice_corr)