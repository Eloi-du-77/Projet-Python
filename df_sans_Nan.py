import pandas as pd

pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

df_tous_pays=pd.read_pickle("df_tous_pays.pkl")


annees_olympiques = [2012, 2016, 2020]

# Filtrer pour ne garder que les années olympiques
df_olympiques = df_tous_pays[df_tous_pays['annee'].isin(annees_olympiques)]

# Identifier les pays qui ont des données complètes pour toutes les années olympiques
# Un pays est valide s'il a 4 observations (une par année) et aucun NaN
pays_complets = df_olympiques.groupby('pays').filter(
    lambda x: x.isna().sum().sum() <= 5
)['pays'].unique()

# Filtrer le dataframe ORIGINAL pour ne garder que ces pays
# Cela conserve toutes les années (olympiques et non-olympiques) pour ces pays
df_filtre = df_tous_pays[df_tous_pays['pays'].isin(pays_complets)]

print(f"Nombre de pays conservés : {(pays_complets)}")
print(f"Nombre de lignes avant : {len(df_tous_pays)}")
print(f"Nombre de lignes après : {len(df_filtre)}")
#print(df_filtre[df_filtre["annee"].isin(annees_olympiques)].head())

# Calculer le score olympique moyen par pays
scores_moyens = df_filtre.groupby('pays')['score_paralympique'].mean().sort_values(ascending=False)

# Garder les 12 meilleurs pays
top_12_pays = scores_moyens.head(12).index

# Filtrer le dataframe
df_top12 = df_filtre[df_filtre['pays'].isin(top_12_pays)]

print(f"Top 12 pays : {list(top_12_pays)}")
print(f"Nombre de lignes : {len(df_top12)}")


df_top12.to_pickle("df_top12_sans_NaN.pkl")