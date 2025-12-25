import numpy as np

#Crée une moyenne des dépenses entre 2008 et l'année olympique exclue
def creation_moyenne(df_merge):
    annees_olympiques = [2012,2016,2020,2024]
    df_merge['moy_education_2008'] = np.nan
    df_merge['moy_loisirs_2008'] = np.nan
    df_merge['moy_amenagement_2008'] = np.nan
    df_merge['moy_maladie_2008'] = np.nan

    for annee_jo in annees_olympiques:
        for pays in df_merge['pays'].unique():
            #Filtration des données du pays entre 2008 et l'année olympique (exclue)
            df_avant_annee = (df_merge['pays'] == pays) & (df_merge['annee'] >= 2008) & (df_merge['annee'] < annee_jo)
            donnees_depuis_2008 = df_merge[df_avant_annee]
        
            #Calcul des moyennes si on a des données
            if len(donnees_depuis_2008) > 0:
                moy_education = donnees_depuis_2008['education_par_habitant'].mean()
                moy_loisirs = donnees_depuis_2008['loisirs_sports_par_habitant'].mean()
                moy_amenagement = donnees_depuis_2008['amenagement_territoire_par_habitant'].mean()
                moy_maladie = donnees_depuis_2008['maladie_invalidite_par_habitant'].mean()
            
                #Ajout du résultat dans les variables
                pays_annee_jo = (df_merge['pays'] == pays) & (df_merge['annee'] == annee_jo)

                df_merge.loc[pays_annee_jo, 'moy_education_2008'] = moy_education
                df_merge.loc[pays_annee_jo, 'moy_loisirs_2008'] = moy_loisirs
                df_merge.loc[pays_annee_jo, 'moy_amenagement_2008'] = moy_amenagement
                df_merge.loc[pays_annee_jo, 'moy_maladie_2008'] = moy_maladie
    return df_merge