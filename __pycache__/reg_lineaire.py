import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import scipy.stats as stats

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df_top_12 = pd.read_pickle("Toutes_les_df_agregees/df_top_12_sans_NaN.pkl")

#Préparation des régresseurs/variable à expliquer
X = df_top_12[['idh', 
               'pib_habitant', 'moy_education_1995', 'moy_maladie_1995', 
               'moy_amenagement_1995', 'moy_loisirs_1995']]
Y = df_top_12['score_paralympique']

#Suppression des NaN
X = X.dropna()
Y = Y[X.index]

#Standardiser (au cas ou on veut comparer avec Lasso)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)

#Régression linéaire
ols = LinearRegression()
ols.fit(X_scaled_df, Y)

#Affichage des résultats
Y_pred = ols.predict(X_scaled_df)
r2 = r2_score(Y, Y_pred)
rmse = np.sqrt(mean_squared_error(Y, Y_pred))
n = len(Y)
p = X.shape[1]
r2_adjusted = 1 - (1 - r2) * (n - 1) / (n - p - 1)

print(f"R² : {r2:.4f}")
print(f"R² ajusté : {r2_adjusted:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"Intercept : {ols.intercept_:.4f}")

#Calcul des p-valeurs
residuels = Y - Y_pred
mse = np.sum(residuels**2) / (n - p - 1)
var_coef = mse * np.linalg.inv(X_scaled_df.T @ X_scaled_df).diagonal()
std_errors = np.sqrt(var_coef)
t_stats = ols.coef_ / std_errors
p_values = [2 * (1 - stats.t.cdf(np.abs(t), n - p - 1)) for t in t_stats]

# Tableau récapitulatif avec significativité
tableau = pd.DataFrame({
    'Régresseur': X.columns,
    'Coefficient': ols.coef_,
    'Std Error': std_errors,
    't-statistic': t_stats,
    'p-value': p_values,
    'Significatif (α=0.05)': ['***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.1 else '' for p in p_values]
})
tableau = tableau.sort_values('p-value')

print(tableau)