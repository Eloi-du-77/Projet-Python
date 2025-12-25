import matplotlib.pyplot as plt

#Permet de tracer l'évolution d'une variable pour une liste de pays, si on veut, on peut tracer la moyenne

def plot_evolution(df, colonne, liste_pays, nom_axe = 'Variable', moyenne=False):
    # Filtrer le DataFrame pour les pays sélectionnés
    df_filtre = df[df['pays'].isin(liste_pays)]
    
    plt.figure(figsize=(12, 6))
    
    if moyenne:
        # Calculer la moyenne de la variable par année
        df_moyenne = df_filtre.groupby('annee')[colonne].mean().reset_index()
        df_moyenne = df_moyenne.dropna(subset=[colonne])
        plt.plot(df_moyenne['annee'], df_moyenne[colonne], marker='o', linestyle = '-', linewidth=2, label='Moyenne')
    # Tracer une ligne par pays
    for pays in liste_pays:
        df_pays = df_filtre[df_filtre['pays'] == pays].sort_values('annee')
        df_pays = df_pays.dropna(subset=[colonne])
        plt.plot(df_pays['annee'], df_pays[colonne], marker='o', linestyle = '-', linewidth=2,  label=pays)
    
    plt.title(f'Évolution de {colonne} au fil des années', fontsize=14)
    plt.xlabel('Année')
    plt.ylabel(nom_axe)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()