import matplotlib.pyplot as plt


def plot_evolution(df, colonne, liste_pays, nom_axe = 'Variable', moyenne=False,df_all=None,filepath=None):
    """ Permet de tracer l'évolution d'une variable pour une liste de pays, si on veut, on peut tracer la moyenne
    Si on rentre df_all, on peut aussi tracer la moyenne sur df_all
"""
    #Filtrer le DataFrame pour les pays sélectionnés
    df_filtre = df[df['pays'].isin(liste_pays)]
    
    plt.figure(figsize=(12, 6))
    
    #Tracer la moyenne globale en pointillés si df_tous_pays est fourni
    if df_all is not None:
        df_moyenne_globale = df_all.groupby('annee')[colonne].mean().reset_index()
        df_moyenne_globale = df_moyenne_globale.dropna(subset=[colonne])
        plt.plot(df_moyenne_globale['annee'], df_moyenne_globale[colonne], 
                 linestyle='--', linewidth=2, color='k', label='Moyenne globale', alpha=0.7)
    
    if moyenne:
        # Calculer la moyenne de la variable par année
        df_moyenne = df_filtre.groupby('annee')[colonne].mean().reset_index()
        df_moyenne = df_moyenne.dropna(subset=[colonne])
        plt.plot(df_moyenne['annee'], df_moyenne[colonne], linestyle = '-', linewidth=2, color = 'k', label='Moyenne sur la base restreinte')
    # Tracer une ligne par pays
    for pays in liste_pays:
        df_pays = df_filtre[df_filtre['pays'] == pays].sort_values('annee')
        df_pays = df_pays.dropna(subset=[colonne])
        plt.plot(df_pays['annee'], df_pays[colonne], linestyle = '-', linewidth=2,  label=pays)
    
    plt.title(f'Évolution de {colonne} au fil des années', fontsize=14)
    plt.xlabel('Année')
    plt.ylabel(nom_axe)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

     # Sauvegarder ou afficher
    if filepath:
        plt.savefig(filepath, bbox_inches='tight', dpi=150)
        plt.close()  # Fermer la figure pour libérer la mémoire
    else:
        plt.show()


