import pandas as pd
import numpy as np
from scipy.optimize import minimize

df_tous_pays=pd.read_pickle("../Toutes_les_df_agregees/df_tous_pays.pkl")
df_top_10=pd.read_pickle("../Toutes_les_df_agregees/df_top_10.pkl")
df_top_12=pd.read_pickle("../Toutes_les_df_agregees/df_top_12_sans_NaN.pkl")

#Troncage de df_tous_pays avec que les années olympiques
df_olymp = df_tous_pays[df_tous_pays['annee'].isin([2012,2016,2020,2024])]

#Nombre de valeurs dans chaque base
def nombre_pays_annee (df):
    n_pays = df['pays'].nunique()
    n_annees = df['annee'].nunique()
    couples = df.groupby(['pays', 'annee']).ngroups
    return n_pays, couples

#Affichage
print("==== Nombre d'observations par db ====\n")
print("Nombre de pays dans df_tous_pays")
print(nombre_pays_annee(df_tous_pays)[0])
print("Nombre de couples annees, pays dans df_tous_pays")
print(nombre_pays_annee(df_tous_pays)[1])
print("Nombre de pays dans df_top_10")
print(nombre_pays_annee(df_top_10)[0])
print("Nombre de couples annees, pays dans df_top_10")
print(nombre_pays_annee(df_top_10)[1])
print("Nombre de pays dans df_top_12")
print(nombre_pays_annee(df_top_12)[0])
print("Nombre de couples annees, pays dans df_top_12")
print(nombre_pays_annee(df_top_12)[1])

#Il semble alors judicieux de considérer une observation comme un couple (pays*annee) pour quadrupler le nombre d'observations

#Fonction pour comparer les coefficients de variation entre df
def coef_variation(df):
    variables = [
        'total_medailles_olympiques_par_athlete',
        'total_medailles_paralympiques_par_athlete',
        'amenagement_territoire_par_habitant',
        'maladie_invalidite_par_habitant',
        'loisirs_sports_par_habitant',
        'education_par_habitant',
        'pib_habitant',
        'idh'
    ]
    resultats = pd.DataFrame(columns=['Variable', 'Moyenne', 'CV (%)','Observations'])

    for v in variables:
        #Enlever les valeurs manquantes
        data = df[v].dropna() 
        if len(data) > 0:
            moyenne = data.mean()
            ecart_type = data.std()
            variance = data.var()
            cv = (ecart_type / moyenne * 100) if moyenne != 0 else np.nan
            obs = len(data)

            resultats.loc[len(resultats)] = [v, moyenne, cv, obs]
    return (resultats)
    
#Affichage propre du cv et de la moyenne
def affichage_cv(df, titre="Analyse de variabilité"):
    resultats = coef_variation(df)
    print(type(resultats))
    #Tri par CV décroissant
    resultats = resultats.sort_values('CV (%)', ascending=False)
    
    #Arrondir les valeurs
    resultats['Moyenne'] = resultats['Moyenne'].round(4)
    resultats['CV (%)'] = resultats['CV (%)'].round(4)
    
    print(f"\n{titre}")
    print("=" * 80)
    print(resultats.to_string(index=False))

affichage_cv(df_tous_pays, titre="Analyse de variabilité pour df_tous_pays")
affichage_cv(df_top_10, titre="Analyse de variabilité pour df_top_10")
affichage_cv(df_top_12, titre="Analyse de variabilité pour df_top_12")

#df_top_12 semble alors le meilleur compromis entre un nombre correct d'observations et une variance plus faible que dans df_tous_pays

#Coefficient de variation du le score olympique / paralympique et du le total de medailles par athlete
def cv_score_total(df) :
    resultats = pd.DataFrame(columns=['score_olympique', 'score_paralympique',
    'total_medailles_olympiques_par_athlete', 'total_medailles_paralympiques_par_athlete'])
    
    #CV du score olympique
    data = df['score_olympique'].dropna()
    cv_so=np.nan
    if len(data) > 0 and data.mean() != 0:
        cv_so = (data.std() / data.mean()) * 100

    #CV du score paralympique
    data = df['score_paralympique'].dropna()
    cv_sp=np.nan
    if len(data) > 0 and data.mean() != 0:
        cv_sp = (data.std() / data.mean()) * 100

    #CV du total de medailles olympiques
    data = df['total_medailles_olympiques_par_athlete'].dropna()
    cv_to=np.nan
    if len(data) > 0 and data.mean() != 0:
        cv_to = (data.std() / data.mean()) * 100

    #CV du total de medailles paralympiques
    data = df['total_medailles_paralympiques_par_athlete'].dropna()
    cv_tp = np.nan
    if len(data) > 0 and data.mean() != 0:
        cv_tp = (data.std() / data.mean()) * 100

    resultats.loc[len(resultats)] = [cv_so, cv_sp, cv_to, cv_tp]
    return(resultats)

cv_score_total(df_top_12)
#Affichage du CV des scores et des totaux

def affichage_score_totaux(df, titre="Affichage du coefficient de variation des scores et des totaux sportifs par athlète"):
    resultats=cv_score_total(df)

    #Arrondir les valeurs
    resultats['score_olympique'] = resultats['score_olympique'].round(4)
    resultats['score_paralympique'] = resultats['score_paralympique'].round(4)
    resultats['total_medailles_olympiques_par_athlete'] = pd.to_numeric(resultats['total_medailles_olympiques_par_athlete'], errors='coerce').round(4)
    resultats['total_medailles_paralympiques_par_athlete'] = pd.to_numeric(resultats['total_medailles_paralympiques_par_athlete'], errors='coerce').round(4)
    
    print(f"\n{titre}")
    print("=" * 80)
    print(resultats.to_string(index=False))

affichage_score_totaux(df_top_12)

#fonction qui trouve le score olympique qui minimise le coefficient de variation
def score_min(df):

    #fonction à minimiser
    def cv(x):
        c_or,c_argent,c_bronze=x
        col = c_or*df['or_olympique_par_athlete']+c_argent*df['argent_olympique_par_athlete']+c_bronze*df['bronze_olympique_par_athlete']
        data = col.dropna()
        cv = np.nan
        if len(data) > 0 and data.mean() != 0:
            cv = (data.std() / data.mean()) * 100
        return cv

    #fonction de contrainte    
    contrainte =[
    {'type': 'ineq', 'fun': lambda x: x[0]},
    {'type': 'ineq', 'fun': lambda x: x[1]},
    {'type': 'ineq', 'fun': lambda x: x[2]},
]


    x0 = [1,1,1]
    coefficients = minimize(cv, x0, constraints=contrainte)
    return coefficients

print(score_min(df_top_12))

























def stats_descriptives_resultats (df):
    df_corr = df.copy()
    # Colonnes résultats JO
    cols_jo = [
        'or_olympique_par_athlete', 'argent_olympique_par_athlete', 'bronze_olympique_par_athlete',
        'total_medailles_olympique_par_athlete', 'or_paralympique_par_athlete',
        'argent_paralympique_par_athlete', 'bronze_paralympique_par_athlete',
        'total_medailles_paralympiques_par_athlete',
    ]

    # Colonnes autres variables numériques
    cols_autres = [c for c in df_corr.columns if df_corr[c].dtype in [np.float64, np.int64] and c not in cols_jo]

    # Années des JO
    annees_jo = sorted(df_corr['annee'].unique())

    # Calcul des moyennes cumulées avant chaque année pour chaque pays et chaque variable
    df_moyennes = df_corr.groupby('pays').apply(
        lambda g: g.sort_values('annee').assign(
            **{f'{col}_moy_avant': g[col].expanding().mean().shift(1) for col in cols_autres}
        )
    ).reset_index(drop=True)

    # Garde uniquement les années de JO
    df_corr = df_moyennes[df_moyennes['annee'].isin(annees_jo)].copy()

    # Colonnes pour corrélation
    cols_corr = cols_jo + [c+'_moy_avant' for c in cols_autres]

    # Calcul de la matrice de corrélation
    matrice_corr = df_corr[cols_corr].corr().round(3)  # arrondi à 3 décimales

    # Raccourcir les noms de colonnes pour affichage
    renoms = {
        'or_olympique':'Or_O',
        'argent_olympique':'Arg_O',
        'bronze_olympique':'Bro_O',
        'total_medailles_olympiques':'Tot_O',
        'or_paralympique':'Or_P',
        'argent_paralympique':'Arg_P',
        'bronze_paralympique':'Bro_P',
        'total_medailles_paralympiques':'Tot_P'
    }

    # Ajouter les autres variables moyennes
    for c in cols_autres:
        renoms[c+'_moy_avant'] = c[:10] + '_moy'  # tronquer à 10 caractères max + _moy

    matrice_corr.rename(index=renoms, columns=renoms, inplace=True)

    # Affichage explicatif
    print("==== MATRICE DE CORRÉLATION (valeurs arrondies et noms raccourcis) ====\n")
    print("Logique de calcul :")
    print("- Les colonnes de résultats olympiques/paralympiques ne sont disponibles que tous les 4 ans (années de JO).")
    print("- La corrélation est calculée entre le résultat de l'année x et la moyenne des autres variables sur toutes les années précédentes.\n")

    print(matrice_corr)

#stats_descriptives_resultats(df_top_12)