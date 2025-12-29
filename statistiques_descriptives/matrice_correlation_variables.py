import matplotlib.pyplot as plt
import seaborn as sns

#pd.set_option('display.max_rows', None)
#pd.set_option('display.width', None)
#pd.set_option('display.max_colwidth', None)

def matrice_correlation (df):
    """Trace la matrice de corrélation des variables intéressantes
    """
    #Exclusion des années non olympiques
    df_corr = df.copy()
    df_corr = df_corr[df_corr['annee'].isin([2012,2016,2020,2024])]
    cols = ['score_olympique','score_paralympique', 'moy_amenagement_2008','moy_education_2008',
    'moy_loisirs_2008','moy_maladie_2008','pib_habitant','idh']


    #Calcul de la matrice de corrélation
    matrice_corr = df_corr[cols].corr().round(3)  #On arrondit

    #On trace
    plt.figure(figsize=(16, 12))
    sns.heatmap(matrice_corr,   #boîte noire
                annot=True,           
                fmt='.2f',           
                cmap='coolwarm',    
                center=0,             
                vmin=-1, vmax=1,      
                square=True,          
                linewidths=0.5,       
                cbar_kws={'label': 'Corrélation'})
    
    plt.title('Matrice de corrélation : Résultats sportifs vs Statistiques nationales', 
              fontsize=14, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

