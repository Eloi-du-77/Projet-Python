import pandas as pd

# Charger le fichier Excel (skip les 3 premières lignes qui sont généralement des métadonnées)
df = pd.read_excel('Projet-Python/PIB_par_habitant_par_pays_par_annee.xls', skiprows=3)

# Afficher les premières colonnes pour voir la structure
# Les colonnes non-annees sont généralement: 
# 'Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'
# Les annees sont les colonnes restantes

# Identifier les colonnes d'identifiants (non-annees)
id_cols = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']

# Transformer en format long
df_long = pd.melt(
    df,
    id_vars=id_cols,
    var_name='annee',
    value_name='pib_habitant'
)

# Convertir annee en numérique (enlève 'Unnamed' et autres)
df_long['annee'] = pd.to_numeric(df_long['annee'], errors='coerce')

# Supprimer les lignes où annee est NaN
df_long = df_long.dropna(subset=['annee'])

# Convertir annee en entier
df_long['annee'] = df_long['annee'].astype(int)

# Filtrer pour annee >= 2008
df_long = df_long[df_long['annee'] >= 2008].reset_index(drop=True)

# Supprimer les lignes avec PIB manquant si nécessaire
df_long = df_long.dropna(subset=['pib_habitant'])


df_long = df_long.drop(['Indicator Name', 'Indicator Code'], axis=1)

#Changer les noms de certains pays
country_mapping = {
    "Brunéi Darussalam": "Brunei",
    "Congo, Rép. dém. du": "République démocratique du Congo",
    "Congo, Rép. du": "Congo",
    "Cabo Verde": "Cap Vert",
    "Égypte, République arabe d'": "Égypte",
    "Micronésie, États fédérés de": "Micronésie",
    "Hong Kong, Chine": "Hong Kong",
    "Iran, Rép. islamique d'": "Iran",
    "Iraq": "Irak",
    "République kirghize": "Kirghizistan",
    "Saint-Kitts-et-Nevis": "Saint-Christophe-et-Niévès",
    "Corée, Rép. de": "Corée du sud",
    "Rép. dém. pop. lao": "Laos",
    "Macao, Chine": "Macao",
    "Puerto Rico (US)": "Porto Rico", 
    "Corée, Rép. dém. de": "Corée du Nord",
    "Cisjordanie et Gaza": "Palestine",
    "Fédération de Russie": "Russie",
    "République dédérale de Somalie": "Somalie",
    "République slovaque": "Slovaquie",
    "République arabe syrienne": "Syrie",
    "Timor-Leste": "Timor oriental",
    "Îles Vierges (EU)": "Iles vierges américaines",
    "Viet Nam": "Viêt Nam",
    "Yémen, Rép. du": "Yémen",
    "Saint-Vincent-et-les Grenadines" :"Saint-Vincent-et-les-Grenadines",
}

df_long['Country Name'] = df_long['Country Name'].replace(country_mapping)


df_long.columns = ["pays", "code_du_pays", "annee", "pib_habitant"]

df_long.to_pickle("df_pib_par_habitant.pkl")