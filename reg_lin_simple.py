import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy import stats
import numpy as np

# Charger les données
df_top_12 = pd.read_pickle("Toutes_les_df_agregees/df_top_12_sans_NaN.pkl")

# Préparer les données pour la régression
# Supprimer les lignes avec des NaN dans score_olympique ou score_paralympique
df_reg = df_top_12[['pays', 'annee', 'score_olympique', 'score_paralympique']].dropna()

print(f"Nombre d'observations : {len(df_reg)}")
print(f"Pays présents : {df_reg['pays'].nunique()}")
print(f"Années présentes : {sorted(df_reg['annee'].unique())}")

# Variable explicative (X) et variable à expliquer (y)
X = df_reg[['score_olympique']].values
y = df_reg['score_paralympique'].values

# Régression linéaire
model = LinearRegression()
model.fit(X, y)

# Prédictions
y_pred = model.predict(X)

# Calcul du R²
r2 = model.score(X, y)

# Calcul des statistiques pour les p-values
n = len(y)
k = 1  # nombre de variables explicatives
residuals = y - y_pred
mse = np.sum(residuals**2) / (n - k - 1)
var_X = np.sum((X - X.mean())**2)
se_slope = np.sqrt(mse / var_X)
se_intercept = np.sqrt(mse * (1/n + X.mean()**2 / var_X))

# Statistiques t
t_slope = model.coef_[0] / se_slope
t_intercept = model.intercept_ / se_intercept

# P-values (test bilatéral)
p_slope = 2 * (1 - stats.t.cdf(abs(t_slope), n - k - 1))
p_intercept = 2 * (1 - stats.t.cdf(abs(t_intercept), n - k - 1))

# Affichage des résultats
print("\n" + "="*70)
print("RÉSULTATS DE LA RÉGRESSION LINÉAIRE")
print("="*70)
print(f"\nModèle : score_paralympique = β₀ + β₁ × score_olympique + ε")
print(f"\n{'Paramètre':<25} {'Coefficient':<15} {'P-value':<15}")
print("-"*70)
print(f"{'Intercept (β₀)':<25} {model.intercept_:>14.4f} {p_intercept:>14.6f}")
print(f"{'score_olympique (β₁)':<25} {model.coef_[0]:>14.4f} {p_slope:>14.6f}")
print("-"*70)
print(f"\n{'R² (coefficient de détermination)':<40} {r2:.4f}")
print(f"{'R² ajusté':<40} {1 - (1-r2)*(n-1)/(n-k-1):.4f}")
print(f"{'Erreur standard résiduelle':<40} {np.sqrt(mse):.4f}")
print("="*70)