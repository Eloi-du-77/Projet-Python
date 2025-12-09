from eurostat import get_data_df
import pandas as pd

df = get_data_df("gov_10a_exp")


df_filtree=df[df['cofog99'].isin(['GF0602','GF0801','GF1001'])]

df_longue = df_filtree.melt(
    id_vars=['geo\\TIME_PERIOD', 'cofog99'],  # colonnes fixes
    value_vars=[str(y) for y in range(1995, 2025)],  # colonnes années
    var_name='annee',
    value_name='depense'
)

df_longue.rename(columns={'geo\\TIME_PERIOD':'pays'}, inplace=True)


pays_dict = {
    'AT': 'Autriche',
    'BE': 'Belgique',
    'BG': 'Bulgarie',
    'HR': 'Croatie',
    'CY': 'Chypre',
    'CZ': 'République tchèque',
    'DK': 'Danemark',
    'EE': 'Estonie',
    'FI': 'Finlande',
    'FR': 'France',
    'DE': 'Allemagne',
    'GR': 'Grèce',
    'HU': 'Hongrie',
    'IE': 'Irlande',
    'IT': 'Italie',
    'LV': 'Lettonie',
    'LT': 'Lituanie',
    'LU': 'Luxembourg',
    'MT': 'Malte',
    'NL': 'Pays-Bas',
    'PL': 'Pologne',
    'PT': 'Portugal',
    'RO': 'Roumanie',
    'SK': 'Slovaquie',
    'SI': 'Slovénie',
    'ES': 'Espagne',
    'SE': 'Suède'
}

df_longue['pays'] = df_longue['pays'].map(pays_dict)

cofog_labels = {'GF0602': 'amenagement_territoire', "GF0801": "loisirs_sports", "GF1001" : "maladie_invalidite"}

df_longue['annee'] = df_longue['annee'].astype('float64')
df_longue['cofog99'] = df_longue['cofog99'].map(cofog_labels)
df_longue.rename(columns={'cofog99': 'type_depense'}, inplace=True)

df_longue = df_longue.pivot_table(
    index=['pays', 'annee'],
    columns='type_depense',
    values='depense', 
    aggfunc='first'
).reset_index()

df_longue.to_pickle("df_depenses_publiques.pkl")