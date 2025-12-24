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
        'moy_amenagement_1995',
        'moy_maladie_1995',
        'moy_loisirs_1995',
        'moy_education_1995',
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

#fonction qui trouve le score de dépense qui minimise le coefficient de variation
def score_min_var(df):

    #fonction à minimiser
    def cv(x):
        c_amenagement,c_education, c_maladie, c_loisirs=x
        col = c_amenagement*df['moy_amenagement_1995']+c_education*df['moy_education_1995']
        +c_maladie*df['moy_maladie_1995']+c_loisirs*df['moy_loisirs_1995']
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
    {'type': 'ineq', 'fun': lambda x: x[3]},
    ]


    x0 = [1,1,1,1]
    coefficients = minimize(cv, x0, constraints=contrainte)
    return coefficients

#fonction qui donne la combinaison linéaire optimale de dépenses pour maximiser le R² d'une régression de score_paralympique sur la combinaison
def score_max_R(df):

    #fonction à minimiser
    def R_2(x):
        c_amenagement,c_education, c_maladie, c_loisirs=x
        col = c_amenagement*df['moy_amenagement_1995']+c_education*df['moy_education_1995']
        +c_maladie*df['moy_maladie_1995']+c_loisirs*df['moy_loisirs_1995']
        data = col.dropna()
        para = df['score_paralympique']
        R_2 = np.nan
        if len(data) > 0 and data.mean() != 0:
            R_2 = (para.cov(data) / data.var())
        return -abs(R_2)

    #fonction de contrainte    
    contrainte =[
    {'type': 'ineq', 'fun': lambda x: x[0]},
    {'type': 'ineq', 'fun': lambda x: x[1]},
    {'type': 'ineq', 'fun': lambda x: x[2]},
    {'type': 'ineq', 'fun': lambda x: x[3]},
    ]


    x0 = [1,1,1,1]
    coefficients = minimize(R_2, x0, constraints=contrainte)
    return coefficients

print(score_min_var(df_top_12))
print(score_max_R(df_top_12))






















