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






df_merge.to_pickle("df_tous_pays.pkl")



pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)





# Afficher les résultats
print(f"Nombre total de lignes: {len(df_merge)}")
print(f"Nombre de colonnes: {len(df_merge.columns)}")
print(f"\nAperçu du DataFrame fusionné:")
print(df_merge.query('pays == "France" & annee == 2012'))
print(f"\nNombre de valeurs manquantes par colonne:")
print(df_merge.isnull().sum())


# 1. Statistiques de base
print("\n1. STATISTIQUES DE BASE (colonnes numériques)")
print("-"*80)
print(df_merge.describe())

# 2. Informations générales sur le DataFrame
print("\n\n2. INFORMATIONS GÉNÉRALES")
print("-"*80)
print(f"Nombre de lignes : {len(df_merge)}")
print(f"Nombre de colonnes : {len(df_merge.columns)}")
print(f"\nTypes de données :")
print(df_merge.dtypes)

# 3. Valeurs manquantes
print("\n\n3. VALEURS MANQUANTES")
print("-"*80)
missing = df_merge.isnull().sum()
missing_pct = (df_merge.isnull().sum() / len(df_merge)) * 100
missing_df = pd.DataFrame({
    'Valeurs manquantes': missing,
    'Pourcentage (%)': missing_pct
})
print(missing_df[missing_df['Valeurs manquantes'] > 0])

# 4. Statistiques supplémentaires pour colonnes numériques
print("\n\n4. STATISTIQUES DÉTAILLÉES (colonnes numériques)")
print("-"*80)
numeric_cols = df_merge.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    print(f"\n{col}:")
    print(f"  Moyenne : {df_merge[col].mean():.4f}")
    print(f"  Médiane : {df_merge[col].median():.4f}")
    print(f"  Écart-type : {df_merge[col].std():.4f}")
    print(f"  Min : {df_merge[col].min():.4f}")
    print(f"  Max : {df_merge[col].max():.4f}")
    print(f"  Q1 (25%) : {df_merge[col].quantile(0.25):.4f}")
    print(f"  Q3 (75%) : {df_merge[col].quantile(0.75):.4f}")
    print(f"  Valeurs uniques : {df_merge[col].nunique()}")



















#Creation d'une variable sur les dépenses moyennes en sport les 4 années avant les JO précédents

annees_jo = [2012, 2016, 2020, 2024] #nous n'avons pas le nombre d'athlètes avant 2012 donc on ne travaillera pas dessus

# def depense_jo(g):
    
#     liste_secteurs = ["Maladie / Invalidité", "Aménagement du territoire", "Loisirs et sports"]
#     g['depense_jo'] = np.nan #pas de valeur si il n'y a pas de JO cette année
#     for elt in liste_secteurs :
#         for pays in g['pays']:
#             for a in annees_jo:
#                 annees_avant = []
#                 for i in range(1,5):
#                     val = g.loc[(g["pays"]==pays) & (g["type_depense"]==elt) & (g["annee"] == a-i), "depense"]
#                     if not val.empty:
#                         print(annees_avant,pays,elt,a)
#                         annees_avant.append(val.values[0])
#                 if annees_avant:
#                     g.loc[(g["pays"]==pays) & (g["type_depense"]==elt) & (g["annee"] == a), 'depense_jo'] = sum(annees_avant)/len(annees_avant)
#     return g


#Creation d'une variable sur les dépenses moyenne en sport entre 1995 et l'année en question

# print(df_depenses_publiques.dtypes)

# def depense_jo_tous_temps(g):
    
#     liste_secteurs = ["Maladie / Invalidité", "Aménagement du territoire", "Loisirs et sports"]
#     g['depense_jo'] = np.nan #pas de valeur si il n'y a pas de JO cette année
#     for elt in liste_secteurs :
#         for pays in g['pays']:
#             for a in annees_jo:
#                 annees_avant = [g.loc[(g["pays"]==pays) & (g["cofog99"]==elt) & (g["annee"] == i), "depense"] for i in range (1995,a)]
#                 print(annees_avant)
#                 if not annees_avant==[]:
#                     g.loc[(g["pays"]==pays) & (g["cofog99"]==elt) & (g["annee"] == a), 'depense_jo'] = sum(annees_avant)/len(annees_avant)
#     return g


