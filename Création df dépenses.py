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

print(df_longue.head(30))
tableau_3d = df_longue.pivot_table(
    index='pays',
    columns=['annee', 'cofog99'],
    values='depense',
    aggfunc='sum'  
)
cofog_labels = {'GF0602': 'Aménagement du territoire', "GF0801": "Loisirs et sports", "GF1001" : "Maladie / Invalidité"}

tableau_3d.rename(columns=cofog_labels, level=1, inplace=True)

print(tableau_3d.head())