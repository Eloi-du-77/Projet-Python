import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def nuage_points(a, df, b="score_paralympique", nom_axe_x="Variable", nom_axe_y="Score paralympique"):
    """FONCTION DONNANT LE NUAGE ENTRE DEUX PARAMETRES ET LE NOMBRE D'OBSERVATION DES NUAGES
    a est la variable en abcisse, b en ordonnée, df la df d'ou prendre les valeurs"""
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    #On filtre la base, on enlève les valeurs manquantes
    annees = [2012, 2016, 2020, 2024]
    df_filtre = df[df['annee'].isin(annees)].copy()
    df_filtre = df_filtre.dropna(subset=[b, a])
    
    #On crée le tableau de couples (a,b)
    ax.scatter(df_filtre[a], df_filtre[b], alpha=0.6, s=50, c='purple', 
               edgecolors='black', linewidth=0.5)
    
    #On affiche
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
    
    #On affiche le nombre d'observations
    n_obs = len(df_filtre)
    ax.text(0.02, 0.98, f'N = {n_obs} observations', 
            transform=ax.transAxes, fontsize=10, 
            verticalalignment='top', bbox=dict(boxstyle='round', 
            facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()