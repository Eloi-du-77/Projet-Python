# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)


df_tous_pays=pd.read_pickle("../Toutes_les_df_agregees/df_tous_pays.pkl")
df_top_10=pd.read_pickle("../Toutes_les_df_agregees/df_top_10.pkl")
df_top_12=pd.read_pickle("../Toutes_les_df_agregees/df_top_12_sans_NaN.pkl")
#FONCTION DONNANT LE NUAGE ENTRE DEUX PARAMETRES ET LE NOMBRE D'OBSERVATION DES NUAGES

def graphique(a, b, df):
    # Créer la figure et les axes
    annees=[2012, 2016, 2020, 2024]
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, annee in enumerate(annees):
        ax = axes[idx]
        
        # Filtrer les données pour l'année
        df_annee = df[df['annee'] == annee].copy()
        
        # Supprimer les valeurs manquantes
        df_annee = df_annee.dropna(subset=[a, b])
        
        #print(f"Année {annee}: {len(df_annee)} observations")
        
        # Créer le scatter plot
        ax.scatter(df_annee[b], df_annee[a], alpha=0.6, s=50, c='purple', 
                   edgecolors='black', linewidth=0.5)
        
        # Ajouter les labels
        ax.set_xlabel(f'{b}', fontsize=11, fontweight='bold')
        ax.set_ylabel(f'{a}', fontsize=11, fontweight='bold')
        ax.set_title(f'Année {int(annee)}', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.show()

# %%
