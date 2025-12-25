import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%
df_top_12=pd.read_pickle("../Toutes_les_df_agregees/df_top_12_sans_NaN.pkl")

def boxplot(df, y_var='score_paralympique', titre='Distribution par année', ylabel='Valeur'):
    #Définir les années possibles
    annees_possibles = [2012, 2016, 2020, 2024]
    
    #Vérifier quelles années sont présentes dans le DataFrame (faire que ce soit plus beau si il manque les valeurs d'une année)
    annees_presentes = [annee for annee in annees_possibles 
                        if annee in df['annee'].values and 
                        df[df['annee'] == annee][y_var].notna().any()]
    #Filtrer le df avec les années présentes
    df_jo = df[df['annee'].isin(annees_presentes)]
    
    #Créer le boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_jo, x='annee', y=y_var, palette='Set2')
    plt.title(titre, fontsize=14)
    plt.xlabel('Année des jeux paralympiques')
    plt.ylabel(ylabel)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
#%%