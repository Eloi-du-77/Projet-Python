import pandas as pd
import numpy as np


def pourcentage_valeurs_manquantes(df) :
    """Calcul du pourcentage de valeurs manquantes dans les années olympiques pour une table df
    """
    df_olymp = df[df['annee'].isin([2012,2016,2020,2024])]

    variables_a_garder = [
        'moy_maladie_2008',
        'moy_amenagement_2008',
        'moy_loisirs_2008',
        'moy_education_2008',
        'score_paralympique',
        'score_olympique',
        'pib_habitant',
        'idh'
    ]
    
    #On calcule le pourcentage de valeurs manquantes
    pourcentage_manquant = (df_olymp[variables_a_garder].isnull().sum() / len(df_olymp)) * 100
    
    #Mise sous forme de df
    resultat = pd.DataFrame({
        'Variable': pourcentage_manquant.index,
        'Pourcentage de valeurs manquantes': pourcentage_manquant.values
    })
    resultat.sort_values('Pourcentage de valeurs manquantes',ascending=False)

    return resultat
