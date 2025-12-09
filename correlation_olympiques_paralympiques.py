from Création_df_propre_et_complète import *
import seaborn as sns
import matplotlib.pyplot as plt


# Calcul de la corrélation entre les médailles par athlète aux JO et aux Paralympiques

# Sélectionner les colonnes des médailles par athlète
cols_jo = ['or_olympique_par_athlete', 'argent_olympique_par_athlete', 'bronze_olympique_par_athlete', 'total_medailles_olympique_par_athlete']
cols_jp = ['or_paralympique_par_athlete', 'argent_paralympique_par_athlete', 'bronze_paralympique_par_athlete', 'total_medailles_paralympiques_par_athlete']

# Créer un DataFrame avec les colonnes des médailles par athlète JO et JP
df_correlation = df_merge[cols_jo + cols_jp]

# Calculer la matrice de corrélation entre les médailles obtenues par athlète aux JO et aux JP
correlation_matrix = df_correlation.corr()

# Arrondir les valeurs de la matrice de corrélation à 2 décimales pour plus de lisibilité
correlation_matrix = df_correlation.corr().round(2)

import seaborn as sns
import matplotlib.pyplot as plt

# Raccourci des noms des colonnes liées aux JO et aux Paralympiques
rename_jo = {
    'or_olympique_par_athlete': 'Or Olympiques',
    'argent_olympique_par_athlete': 'Argent Olympiques',
    'bronze_olympique_par_athlete': 'Bronze Olympiques',
    'total_medailles_olympique_par_athlete': 'Total Olympiques'
}

rename_jp = {
    'or_paralympique_par_athlete': 'Or Paralympiques',
    'argent_paralympique_par_athlete': 'Argent Paralympiques',
    'bronze_paralympique_par_athlete': 'Bronze Paralympiques',
    'total_medailles_paralympiques_par_athlete': 'Total Paralympiques'
}

# Renommer les colonnes dans le DataFrame fusionné
df_merge.rename(columns={**rename_jo, **rename_jp}, inplace=True)

# Sélectionner uniquement les colonnes concernées par les JO et les Paralympiques
cols_jo = list(rename_jo.values())  # Colonnes liées aux JO
cols_jp = list(rename_jp.values())  # Colonnes liées aux Paralympiques

# Créer un DataFrame avec les colonnes JO et JP
df_correlation_jo_jp = df_merge[cols_jo + cols_jp]

# Calculer la matrice de corrélation
correlation_matrix = df_correlation_jo_jp.corr()

# Afficher la heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt=".2f", linewidths=0.5, cbar_kws={'label': 'Corrélation'})
plt.title("Matrice de Corrélation : JO vs Paralympiques (par Athlète)", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=45, va='top')
plt.tight_layout()
plt.show()

# Afficher la matrice de corrélation proprement formatée dans la console
print("Matrice de corrélation entre les médailles par athlète aux JO et aux Paralympiques (raccourcie) :")
print(correlation_matrix)



