import pandas as pd
import numpy as np

#Import des df

df_medailles_olympiques=pd.read_pickle("df_medailles_olympiques.pkl")
df_medailles_paralympiques=pd.read_pickle("df_medailles_paralympiques.pkl")
df_athletes_olympiques=pd.read_pickle("df_athletes_olympiques.pkl")
df_athletes_paralympiques=pd.read_pickle("df_athletes_paralympiques.pkl")
df_depenses_publiques=pd.read_pickle("df_depenses_publiques.pkl")
df_idh=pd.read_pickle("df_idh.pkl")
df_pib_par_habitant=pd.read_pickle("df_pib_par_habitant.pkl")
df_education=pd.read_pickle("df_education.pkl")

#tout réunir

df_merge = df_medailles_olympiques.merge(
    df_medailles_paralympiques, 
    on=['pays', 'annee'], 
    how='outer'
)

df_merge = df_merge.merge(
    df_athletes_olympiques, 
    on=['pays', 'annee'], 
    how='outer'
)

df_merge = df_merge.merge(
    df_athletes_paralympiques, 
    on=['pays', 'annee'], 
    how='outer'
)

df_merge = df_merge.merge(
    df_depenses_publiques, 
    on=['pays', 'annee'], 
    how='outer'
)

df_merge = df_merge.merge(
    df_education, 
    on=['pays', 'annee'], 
    how='outer'
)

df_merge = df_merge.merge(
    df_idh, 
    on=['pays', 'annee'], 
    how='outer'
)

df_merge = df_merge.merge(
    df_pib_par_habitant, 
    on=['pays', 'annee'], 
    how='outer'
)
#Mettre le nombre d'athlètes en format float
df_merge['athletes_olympiques'] = pd.to_numeric(df_merge['athletes_olympiques'], errors='coerce')
df_merge['athletes_paralympiques'] = pd.to_numeric(df_merge['athletes_paralympiques'], errors='coerce')

#Ajout de la variable médaille par athlète

# Médailles olympiques par athlète
df_merge['or_olympique_par_athlete'] = df_merge['or_olympique'] / df_merge['athletes_olympiques']
df_merge['argent_olympique_par_athlete'] = df_merge['argent_olympique'] / df_merge['athletes_olympiques']
df_merge['bronze_olympique_par_athlete'] = df_merge['bronze_olympique'] / df_merge['athletes_olympiques']
df_merge['total_medailles_olympique_par_athlete'] = df_merge['total_medailles_olympiques'] / df_merge['athletes_olympiques']

# Médailles paralympiques par athlète
df_merge['or_paralympique_par_athlete'] = df_merge['or_paralympique'] / df_merge['athletes_paralympiques']
df_merge['argent_paralympique_par_athlete'] = df_merge['argent_paralympique'] / df_merge['athletes_paralympiques']
df_merge['bronze_paralympique_par_athlete'] = df_merge['bronze_paralympique'] / df_merge['athletes_paralympiques']
df_merge['total_medailles_paralympiques_par_athlete'] = df_merge['total_medailles_paralympiques'] / df_merge['athletes_paralympiques']

#Ajout de la variable dépense par habitant
df_merge['amenagement_territoire_par_habitant'] = df_merge['amenagement_territoire'] * df_merge['pib_habitant']
df_merge['loisirs_sports_par_habitant'] = df_merge['loisirs_sports'] * df_merge['pib_habitant']
df_merge['maladie_invalidite_par_habitant'] = df_merge['maladie_invalidite'] * df_merge['pib_habitant']
df_merge['education_par_habitant'] = df_merge['education'] * df_merge['pib_habitant']

#Ajout d'une variable de performance (3 points pour une medaille d'or, 2 pour une en argent, 1 pour une en bronze)
df_merge['score_paralympique'] = (3 * df_merge['or_paralympique_par_athlete'] + 
                                 2 * df_merge['argent_paralympique_par_athlete'] + 
                                 df_merge['bronze_paralympique_par_athlete'])

df_merge['score_olympique'] = (3 * df_merge['or_olympique_par_athlete'] + 
                                 2 * df_merge['argent_olympique_par_athlete'] + 
                                 df_merge['bronze_olympique_par_athlete'])

#Ajout de variables donnant la moyenne des dépenses sur les 4 dernières années
# Initialiser les nouvelles colonnes avec NaN
df_merge['moy_education_pre_jo'] = np.nan
df_merge['moy_loisirs_pre_jo'] = np.nan
df_merge['moy_amenagement_pre_jo'] = np.nan
df_merge['moy_maladie_pre_jo'] = np.nan

# Pour chaque année olympique
annees_olympiques = [2012,2016,2020,2024]
for annee_jo in annees_olympiques:
    # Définir les 4 années précédentes
    annees_precedentes = [annee_jo - 4, annee_jo - 3, annee_jo - 2, annee_jo - 1]
    
    # Pour chaque pays
    for pays in df_merge['pays'].unique():
        # Filtrer les données du pays pour les 4 années précédentes
        mask_pays_annees = (df_merge['pays'] == pays) & (df_merge['annee'].isin(annees_precedentes))
        donnees_precedentes = df_merge[mask_pays_annees]
        
        # Calculer les moyennes si on a des données
        if len(donnees_precedentes) > 0:
            moy_education = donnees_precedentes['education_par_habitant'].mean()
            moy_loisirs = donnees_precedentes['loisirs_sports_par_habitant'].mean()
            moy_amenagement = donnees_precedentes['amenagement_territoire_par_habitant'].mean()
            moy_maladie = donnees_precedentes['maladie_invalidite_par_habitant'].mean()
            
            # Assigner ces moyennes à la ligne de l'année olympique
            mask_jo = (df_merge['pays'] == pays) & (df_merge['annee'] == annee_jo)
            df_merge.loc[mask_jo, 'moy_education_pre_jo'] = moy_education
            df_merge.loc[mask_jo, 'moy_loisirs_pre_jo'] = moy_loisirs
            df_merge.loc[mask_jo, 'moy_amenagement_pre_jo'] = moy_amenagement
            df_merge.loc[mask_jo, 'moy_maladie_pre_jo'] = moy_maladie

#Création d'une variable de moyenne de dépenses depuis 1995

df_merge['moy_education_1995'] = np.nan
df_merge['moy_loisirs_1995'] = np.nan
df_merge['moy_amenagement_1995'] = np.nan
df_merge['moy_maladie_1995'] = np.nan

# Pour chaque année olympique
for annee_jo in annees_olympiques:
    # Pour chaque pays
    for pays in df_merge['pays'].unique():
        # Filtrer les données du pays depuis 1995 jusqu'à l'année olympique (exclue)
        mask_pays_annees = (df_merge['pays'] == pays) & (df_merge['annee'] >= 1995) & (df_merge['annee'] < annee_jo)
        donnees_depuis_1995 = df_merge[mask_pays_annees]
        
        # Calculer les moyennes si on a des données
        if len(donnees_depuis_1995) > 0:
            moy_education = donnees_depuis_1995['education_par_habitant'].mean()
            moy_loisirs = donnees_depuis_1995['loisirs_sports_par_habitant'].mean()
            moy_amenagement = donnees_depuis_1995['amenagement_territoire_par_habitant'].mean()
            moy_maladie = donnees_depuis_1995['maladie_invalidite_par_habitant'].mean()
            
            # Assigner ces moyennes à la ligne de l'année olympique
            mask_jo = (df_merge['pays'] == pays) & (df_merge['annee'] == annee_jo)

            df_merge.loc[mask_jo, 'moy_education_1995'] = moy_education
            df_merge.loc[mask_jo, 'moy_loisirs_1995'] = moy_loisirs
            df_merge.loc[mask_jo, 'moy_amenagement_1995'] = moy_amenagement
            df_merge.loc[mask_jo, 'moy_maladie_1995'] = moy_maladie

#Suppression des colonnes des pays n'ayant jamais amené d'athlètes aux jeux olympiques (permet surtout d'enlever les groupes de pays présents dans certaines bases : Afrique du Nord, etc...)

df_merge = df_merge[df_merge.groupby('pays')['athletes_olympiques'].transform('sum') > 0]

#Suppression des années sans JO

df_merge.to_pickle("df_tous_pays.pkl")



# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)





# # Afficher les résultats
# print(f"Nombre total de lignes: {len(df_merge)}")
# print(f"Nombre de colonnes: {len(df_merge.columns)}")
# print(f"\nAperçu du DataFrame fusionné:")
print(df_merge.query('pays == "France"'))
# print(f"\nNombre de valeurs manquantes par colonne:")
# print(df_merge.isnull().sum())



















