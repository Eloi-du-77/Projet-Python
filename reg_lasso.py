import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

df_top_12 = pd.read_pickle("Toutes_les_df_agregees/df_top_12_sans_NaN.pkl")

#Préparation des régresseurs/variable à expliquer
X = df_top_12[['athletes_olympiques', 'athletes_paralympiques', 'idh', 
               'pib_habitant', 'moy_education_1995', 'moy_maladie_1995', 
               'moy_amenagement_1995', 'moy_loisirs_1995']]
Y = df_top_12['score_paralympique']

#Suppression des NaN
X = X.dropna()
Y = Y[X.index]

#Standardisation des variables
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)

#Régression Lasso (validation croisée pour choisir lambda optimal)
lasso = LassoCV(cv=5, random_state=42, max_iter=10000)
lasso.fit(X_scaled, Y)


#Affichage des coefficients
coefficients = pd.DataFrame({
    'Régresseur': X.columns,
    'Coefficient': lasso.coef_
})
coefficients['Éliminé'] = coefficients['Coefficient'] == 0
coefficients = coefficients.sort_values('Coefficient', key=abs, ascending=False)
print(coefficients)

#Affichage des paramètres intéressants
print(f"Lambda optimal : {lasso.alpha_:.4f}")
print(f"Score R² : {lasso.score(X_scaled, Y):.4f}")