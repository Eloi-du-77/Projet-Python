import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan

# 1) Chargement des données
df = pd.read_pickle("Toutes_les_df_agregees/df_tous_pays.pkl")

# 2) Filtrage des années olympiques
annees_jo = [2012, 2016, 2020, 2024]
df = df[df["annee"].isin(annees_jo)]

# 3) Colonnes utilisées
cols = [
    "score_olympique",
    "moy_education_1995",
    "moy_loisirs_1995",
    "moy_amenagement_1995",
    "moy_maladie_1995",
    "pib_habitant",
    "idh",
    "athletes_olympiques"
]

# 4) Sélection + nettoyage (clé pour éviter tous les bugs)
df = (
    df[cols]
    .apply(pd.to_numeric, errors="coerce")
    .dropna()
    .reset_index(drop=True)
)

# 5) Définition de y et X
y = df["score_olympique"]
X = df.drop(columns="score_olympique")

# 6) Constante
X = sm.add_constant(X)

# 7) Régression OLS
model = sm.OLS(y, X).fit()

# 8) Résultats
print(model.summary())

print("Nombre d'observations :", df.shape[0])
print("Nombre de variables explicatives :", X.shape[1] - 1)  # sans la constante

residus = model.resid
stats.jarque_bera(residus)


het_breuschpagan(residus, model.model.exog)


plt.scatter(model.fittedvalues, residus)
plt.axhline(0)
plt.xlabel("Valeurs ajustées")
plt.ylabel("Résidus")
plt.title("Résidus vs valeurs ajustées")
plt.show()

# En dépit de ses limites, la régression linéaire constitue un cadre pertinent pour une première analyse
# des déterminants macroéconomiques de la performance olympique. Les résultats doivent être interprétés
# avec prudence mais offrent des pistes solides pour des modèles plus avancés, notamment des approches
# en données de panel avec effets fixes.




