import pandas as pd
import numpy as np

#Le df qui sera créé sera gigantesque, il recueille presque tous les pays, les années non olympiques et des variables peu utiles par la suite
#Il sera épuré dans df_top12

# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

#Import des df
df_medailles_olympiques=pd.read_pickle("../Toutes_les_df_olympiques/df_medailles_olympiques.pkl")
df_medailles_paralympiques=pd.read_pickle("../Toutes_les_df_olympiques/df_medailles_paralympiques.pkl")
df_athletes_olympiques=pd.read_pickle("../Toutes_les_df_olympiques/df_athletes_olympiques.pkl")
df_athletes_paralympiques=pd.read_pickle("../Toutes_les_df_olympiques/df_athletes_paralympiques.pkl")
df_depenses_publiques=pd.read_pickle("../Toutes_les_df_de_depenses/df_depenses_publiques.pkl")
df_idh=pd.read_pickle("../Toutes_les_df_nationales/df_idh.pkl")
df_pib_par_habitant=pd.read_pickle("../Toutes_les_df_nationales/df_pib_par_habitant.pkl")
df_education=pd.read_pickle("../Toutes_les_df_de_depenses/df_education.pkl")

#Réunir toutes les tables

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

#Mettre le nombre d'athlètes et les annees en format numérique
df_merge['athletes_olympiques'] = pd.to_numeric(df_merge['athletes_olympiques'], errors='coerce')
df_merge['athletes_paralympiques'] = pd.to_numeric(df_merge['athletes_paralympiques'], errors='coerce')
df_merge["annee"] = pd.to_numeric(df_merge["annee"], errors='coerce')
#AJOUTS DE VARIABLES

# Médailles olympiques par athlète
df_merge['or_olympique_par_athlete'] = df_merge['or_olympique'] / df_merge['athletes_olympiques']
df_merge['argent_olympique_par_athlete'] = df_merge['argent_olympique'] / df_merge['athletes_olympiques']
df_merge['bronze_olympique_par_athlete'] = df_merge['bronze_olympique'] / df_merge['athletes_olympiques']
df_merge['total_medailles_olympiques_par_athlete'] = df_merge['total_medailles_olympiques'] / df_merge['athletes_olympiques']

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

#Création d'une variable de moyenne de dépenses depuis 1995

annees_olympiques = [2012,2016,2020,2024]
df_merge['moy_education_1995'] = np.nan
df_merge['moy_loisirs_1995'] = np.nan
df_merge['moy_amenagement_1995'] = np.nan
df_merge['moy_maladie_1995'] = np.nan

for annee_jo in annees_olympiques:
    for pays in df_merge['pays'].unique():
        #Filtration des données du pays entre 1995 et l'année olympique (exclue)
        df_avant_annee = (df_merge['pays'] == pays) & (df_merge['annee'] >= 1995) & (df_merge['annee'] < annee_jo)
        donnees_depuis_1995 = df_merge[df_avant_annee]
        
        #Calcul des moyennes si on a des données
        if len(donnees_depuis_1995) > 0:
            moy_education = donnees_depuis_1995['education_par_habitant'].mean()
            moy_loisirs = donnees_depuis_1995['loisirs_sports_par_habitant'].mean()
            moy_amenagement = donnees_depuis_1995['amenagement_territoire_par_habitant'].mean()
            moy_maladie = donnees_depuis_1995['maladie_invalidite_par_habitant'].mean()
            
            #Ajout du résultat dans les variables
            pays_annee_jo = (df_merge['pays'] == pays) & (df_merge['annee'] == annee_jo)

            df_merge.loc[pays_annee_jo, 'moy_education_1995'] = moy_education
            df_merge.loc[pays_annee_jo, 'moy_loisirs_1995'] = moy_loisirs
            df_merge.loc[pays_annee_jo, 'moy_amenagement_1995'] = moy_amenagement
            df_merge.loc[pays_annee_jo, 'moy_maladie_1995'] = moy_maladie

#Suppression des colonnes des pays n'ayant jamais amené d'athlètes aux jeux olympiques (permet surtout d'enlever les groupes de pays présents dans certaines bases : Afrique du Nord, etc...)
df_merge = df_merge[df_merge.groupby('pays')['athletes_olympiques'].transform('sum') > 0]

#Gestion d'un bug, la Russie a deux colonne en 2024 (une avec tous ses résultats sportifs, une avec le reste) on les fusionne
#Sélection des lignes à fusionner
mask = (df_merge['pays'] == 'Russie') & (df_merge['annee'] == 2024)
df_Russie_2024 = df_merge[mask]
#Remplacement des NaN de l'une par les valeurs de l'autre
ligne_fusion = df_Russie_2024.iloc[0].combine_first(df_Russie_2024.iloc[1])
#Ajouter la ligne et supprimer les deux anciennes
df_merge = df_merge[~mask]
df_merge = pd.concat([df_merge, ligne_fusion.to_frame().T], ignore_index=True)

df_merge.to_pickle("df_tous_pays.pkl")






