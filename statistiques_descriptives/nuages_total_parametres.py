import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#pd.set_option('display.max_rows', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)


#df_tous_pays=pd.read_pickle("../Toutes_les_df_agregees/df_tous_pays.pkl")
#df_top_10=pd.read_pickle("../Toutes_les_df_agregees/df_top_10.pkl")
#df_top_12=pd.read_pickle("../Toutes_les_df_agregees/df_top_12_sans_NaN.pkl")


def nuage_points(a, df, b="score_paralympique", nom_axe_x="Variable", nom_axe_y="Score paralympique"):
    """FONCTION DONNANT LE NUAGE ENTRE DEUX PARAMETRES ET LE NOMBRE D'OBSERVATION DES NUAGES """
    
    #Créer la figure
    fig, ax = plt.subplots(figsize=(10, 7))
    
    #Filtrer les données pour ne garder que les années souhaitées
    annees = [2012, 2016, 2020, 2024]
    df_filtre = df[df['annee'].isin(annees)].copy()
    
    #Supprimer les valeurs manquantes
    df_filtre = df_filtre.dropna(subset=[b, a])
    
    #Créer le scatter plot avec toutes les observations
    ax.scatter(df_filtre[a], df_filtre[b], alpha=0.6, s=50, c='purple', 
               edgecolors='black', linewidth=0.5)
    
    #Ajouter les labels
    ax.set_xlabel(nom_axe_x, fontsize=11, fontweight='bold')
    ax.set_ylabel(nom_axe_y, fontsize=11, fontweight='bold')
    ax.set_title(
    f"Nuage de points des pays de df_top_10_sans_NaN\n"
    f"Score paralympique en fonction de {a}\n"
    f"Toutes années confondues (2012-2024)",
    fontsize=13,
    fontweight='bold'
)


    ax.grid(True, alpha=0.3, linestyle='--')
    
    #Afficher le nombre d'observations
    n_obs = len(df_filtre)
    ax.text(0.02, 0.98, f'N = {n_obs} observations', 
            transform=ax.transAxes, fontsize=10, 
            verticalalignment='top', bbox=dict(boxstyle='round', 
            facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()