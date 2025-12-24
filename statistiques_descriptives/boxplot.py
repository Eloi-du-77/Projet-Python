import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%
df_top_12=pd.read_pickle("../Toutes_les_df_agregees/df_top_12_sans_NaN.pkl")
df_jo_recents = df_top_12[df_top_12['annee'].isin([2012, 2016, 2020, 2024])]

plt.figure(figsize=(12, 6))
sns.boxplot(data=df_jo_recents, x='annee', y='score_paralympique', palette='Set2')
plt.title('Distribution du Score Paralympique par année (JO récents)', fontsize=14)
plt.xlabel('Année des Jeux Olympiques')
plt.ylabel('Score Paralympique')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
#%%