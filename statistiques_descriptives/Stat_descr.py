import pandas as pd
import numpy as np
from scipy.optimize import minimize


#Nombre de valeurs dans chaque base
def nombre_pays_annee (df):
    n_pays = df['pays'].nunique()
    n_annees = df['annee'].nunique()
    couples = df.groupby(['pays', 'annee']).ngroups
    return n_pays, couples

def quotient(df,df_tous_pays):
    """Fonction pour observer les quotients (écart_type sur la "sous-base")/moyenne sur df_tous_pays des variables
    """
    variables = [
        'moy_amenagement_2008',
        'moy_maladie_2008',
        'moy_loisirs_2008',
        'moy_education_2008',
        'pib_habitant',
        'idh'
    ]
    resultats = pd.DataFrame(columns=['Variable', 'Moyenne', 'Quotient (%)','Observations'])

    for v in variables:
        #Calcul pour chaque variable de la moyenne, de l'écart type, de la moyenne de tous les pays et du quotient
        data = df[v].dropna()
        data_tous_pays=df_tous_pays[v].dropna() 
        if len(data) > 0:
            moyenne = data.mean()
            moyenne_tous_pays=data_tous_pays.mean()
            ecart_type = data.std()
            variance = data.var()
            quotient = (ecart_type / moyenne_tous_pays * 100) if moyenne_tous_pays != 0 else np.nan
            obs = len(data)

            resultats.loc[len(resultats)] = [v, moyenne, quotient, obs]
    return (resultats)
    

def affichage_quotient(df, titre="Analyse de variabilité"):
    """Affichage propre du quotient et de la moyenne
    """
    resultats = quotient(df)
    print(type(resultats))

    #Tri par quotient décroissant et arrondi des valeurs
    resultats = resultats.sort_values('Quotient (%)', ascending=False)
    resultats['Moyenne'] = resultats['Moyenne'].round(4)
    resultats['Quotient (%)'] = resultats['Quotient (%)'].round(4)
    
    print(f"\n{titre}")
    print(" " * 80)
    print(resultats.to_string(index=False))

