from création_df_que_certains_pays import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Charger les données
df_tous_pays = pd.read_pickle("df_tous_pays.pkl")

# Filtrer les données entre 2012 et 2024 pour les pays du top 30
df_periode = df_tous_pays[(df_tous_pays['annee'] >= 2012) & (df_tous_pays['annee'] <= 2024)]

# Calculer le total cumulé des médailles paralympiques pour chaque pays
total_medailles_par_pays = df_periode.groupby('pays')['total_medailles_paralympiques'].sum().reset_index()

# Top 30 des pays ayant le plus de médailles paralympiques
top_30_pays = total_medailles_par_pays.nlargest(30, 'total_medailles_paralympiques')['pays'].tolist()

# Filtrer le DataFrame pour ne garder que ces pays
df_tous_pays = df_tous_pays[df_tous_pays['pays'].isin(top_30_pays)].copy()

# Vérification des données
print(f"Nombre de pays conservés : {df_tous_pays['pays'].nunique()}")
print(f"Nombre total de lignes : {len(df_tous_pays)}")

# Afficher les premières lignes pour vérifier la structure
print(df_tous_pays.head())

# Suppression des lignes avec des valeurs manquantes dans les colonnes critiques
df_tous_pays = df_tous_pays.dropna(subset=['idh', 'total_medailles_paralympiques', 'amenagement_territoire', 'loisirs_sports', 'maladie_invalidite', 'pib_habitant'])

# Filtrer les années olympiques (2012, 2016, 2020, 2024)
annees = [2012, 2016, 2020, 2024]
df_filtree = df_tous_pays[df_tous_pays['annee'].isin(annees)]

# Définir les variables explicatives (X) et la variable cible (y)
X = df_filtree[['idh', 'amenagement_territoire', 'loisirs_sports', 'maladie_invalidite', 'pib_habitant']]
y = df_filtree['total_medailles_paralympiques']

# Diviser les données en jeu d'entraînement et jeu de test (70% entraînement, 30% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Appliquer la régression linéaire
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Prédire les résultats sur les données de test
y_pred = regressor.predict(X_test)

# Calculer l'erreur quadratique moyenne (RMSE)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Afficher les résultats de la régression
print(f"\nRMSE (Root Mean Squared Error) : {rmse:.2f}\n")

# Coefficients de la régression
coefficients = pd.DataFrame(regressor.coef_, X.columns, columns=['Coefficient'])
print("Coefficients de la régression :")
print(coefficients)

# Graphique : Réel vs Prédit
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)  # Ligne diagonale (réel == prédit)
plt.xlabel('Valeurs réelles')
plt.ylabel('Valeurs prédites')
plt.title('Régression Linéaire : Valeurs réelles vs Prédites')
plt.grid(True)
plt.show()

# Graphique des résidus (différence entre réels et prédits)
residus = y_test - y_pred
plt.figure(figsize=(8, 6))
sns.histplot(residus, kde=True, color='red', bins=20)
plt.title('Distribution des Résidus (Erreurs de Prédiction)')
plt.xlabel('Résidus')
plt.ylabel('Fréquence')
plt.grid(True)
plt.show()



