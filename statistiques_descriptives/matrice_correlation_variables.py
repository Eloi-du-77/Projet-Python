import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df_top_12=pd.read_pickle("../Toutes_les_df_agregees/df_top_12_sans_NaN.pkl")


def stats_descriptives_resultats (df):
    df_corr = df.copy()
    # Colonnes résultats JO
    cols_jo = [
        'or_olympique_par_athlete', 'argent_olympique_par_athlete', 'bronze_olympique_par_athlete',
        'total_medailles_olympiques_par_athlete', 'or_paralympique_par_athlete',
        'argent_paralympique_par_athlete', 'bronze_paralympique_par_athlete',
        'total_medailles_paralympiques_par_athlete','score_olympique','score_paralympique'
    ]

    #Colonnes autres variables numériques
    cols_autres = ['moy_amenagement_1995','moy_education_1995','moy_loisirs_1995','moy_maladie_1995','score_depense','pib_habitant','idh']

    #Colonnes pour corrélation
    cols_corr = cols_jo + cols_autres

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
    #for c in cols_autres:
    #    renoms[c] = c[:10] + '_moy'  # tronquer à 10 caractères max + _moy

    #matrice_corr.rename(index=renoms, columns=renoms, inplace=True)

    # Affichage explicatif
    print("==== MATRICE DE CORRÉLATION (valeurs arrondies et noms raccourcis) ====\n")
    print("Logique de calcul :")
    print("- Les colonnes de résultats olympiques/paralympiques ne sont disponibles que tous les 4 ans (années de JO).")
    print("- La corrélation est calculée entre le résultat de l'année x et la moyenne des autres variables sur toutes les années précédentes.\n")

    # Visualisation
    plt.figure(figsize=(16, 12))
    sns.heatmap(matrice_corr, 
                annot=True,           # Affiche les valeurs
                fmt='.2f',            # Format 2 décimales
                cmap='coolwarm',      # Palette de couleurs
                center=0,             # Centre sur 0
                vmin=-1, vmax=1,      # Échelle de -1 à 1
                square=True,          # Cellules carrées
                linewidths=0.5,       # Lignes entre cellules
                cbar_kws={'label': 'Corrélation'})
    
    plt.title('Matrice de corrélation : Résultats sportifs vs Statistiques nationales', 
              fontsize=14, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()
    
    return matrice_corr

stats_descriptives_resultats(df_top_12)

#%%