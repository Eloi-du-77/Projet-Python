import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#pd.set_option('display.max_rows', None)
#pd.set_option('display.width', None)
#pd.set_option('display.max_colwidth', None)

#df_top_12=pd.read_pickle("../Toutes_les_df_agregees/df_top_12_sans_NaN.pkl")

def matrice_correlation (df):
    #Exclusion des années non olympiques
    df_corr = df.copy()
    df_corr = df_corr[df_corr['annee'].isin([2012,2016,2020,2024])]
    # Colonnes résultats JO
    cols_jo = [
        #'or_olympique_par_athlete', 'argent_olympique_par_athlete', 'bronze_olympique_par_athlete',
        #'total_medailles_olympiques_par_athlete', 'or_paralympique_par_athlete',
        #'argent_paralympique_par_athlete', 'bronze_paralympique_par_athlete',
        #'total_medailles_paralympiques_par_athlete',
        'score_olympique','score_paralympique',
    ]

    #Colonnes autres variables numériques
    cols_autres = ['moy_amenagement_2008','moy_education_2008','moy_loisirs_2008','moy_maladie_2008','pib_habitant','idh']

    #Colonnes pour corrélation
    cols_corr = cols_jo + cols_autres

    # Calcul de la matrice de corrélation
    matrice_corr = df_corr[cols_corr].corr().round(3)  # arrondi à 3 décimales

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

#matrice_correlation(df_top_12)
