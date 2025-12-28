import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy import stats
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def regression_simple(df,param):
    """Fais la régression simple de score_paralympique sur un paramètre
    et retourne un DataFrame avec tous les résultats
    """

    df_reg = df[['pays', 'annee', param, 'score_paralympique']].dropna()

    #Variable explicative (X) et variable à expliquer (Y)
    X = df_reg[[param]].values
    Y = df_reg['score_paralympique'].values

    # Régression linéaire
    model = LinearRegression()
    model.fit(X, Y)

    # Prédictions
    Y_pred = model.predict(X)

    # Calcul des statistiques
    n = len(Y)
    k = 1  # nombre de variables explicatives
    residuals = Y - Y_pred
    mse = np.sum(residuals**2) / (n - k - 1)
    r2 = model.score(X, Y)
    r2_adj = 1 - (1-r2)*(n-1)/(n-k-1)
    
    # Erreurs standard
    var_X = np.sum((X - X.mean())**2)
    se_slope = np.sqrt(mse / var_X)
    se_intercept = np.sqrt(mse * (1/n + X.mean()**2 / var_X))

    # Statistiques t et p-values
    t_slope = model.coef_[0] / se_slope
    t_intercept = model.intercept_ / se_intercept
    p_slope = 2 * (1 - stats.t.cdf(abs(t_slope), n - k - 1))
    p_intercept = 2 * (1 - stats.t.cdf(abs(t_intercept), n - k - 1))

    # Intervalles de confiance à 95%
    t_critical = stats.t.ppf(0.975, n - k - 1)  # valeur critique pour α=0.05 bilatéral
    
    ic_intercept_lower = model.intercept_ - t_critical * se_intercept
    ic_intercept_upper = model.intercept_ + t_critical * se_intercept
    
    ic_slope_lower = model.coef_[0] - t_critical * se_slope
    ic_slope_upper = model.coef_[0] + t_critical * se_slope

    # Création du DataFrame de résultats
    resultats = pd.DataFrame({
        'Paramètre': ['Intercept (β₀)', param + '(β₁)'],
        'Coefficient': [model.intercept_, model.coef_[0]],
        'Erreur Standard': [se_intercept, se_slope],
        'IC 95% - Borne inf': [ic_intercept_lower, ic_slope_lower],
        'IC 95% - Borne sup': [ic_intercept_upper, ic_slope_upper],
        'Statistique t': [t_intercept, t_slope],
        'P-value': [p_intercept, p_slope]
    })

    # Affichage des informations générales
    print("="*80)
    print("RÉSULTATS DE LA RÉGRESSION LINÉAIRE")
    print("="*80)
    print(f"\nModèle : score_paralympique = β₀ + β₁ × "+param+"+ ε")
    print(f"Nombre d'observations : {n}")
    print(f"R² : {r2:.4f}")
    print(f"R² ajusté : {r2_adj:.4f}")
    print(f"Erreur standard résiduelle : {np.sqrt(mse):.4f}")
    
    # Affichage du DataFrame avec un bon formatage
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.float_format', lambda x: f'{x:.4f}')
    print(resultats.to_string(index=False))
    print("="*80)
    
    return resultats

def plot_regression_simple(df, resultats_df):
    """Trace la régression linéaire de score_paralympique sur {param}
    à partir des résultats de la fonction regression_simple()
    """
    
    df_reg = df[['pays', 'annee', 'score_olympique', 'score_paralympique']].dropna()
    X = df_reg[['score_olympique']].values
    Y = df_reg['score_paralympique'].values
    n = len(Y)
    
    #Extraire les paramètres du DataFrame de résultats
    intercept = resultats_df.loc[resultats_df['Paramètre'] == 'Intercept (β₀)', 'Coefficient'].values[0]
    slope = resultats_df.loc[resultats_df['Paramètre'] == 'score_olympique (β₁)', 'Coefficient'].values[0]
    
    ic_slope_lower = resultats_df.loc[resultats_df['Paramètre'] == 'score_olympique (β₁)', 'IC 95% - Borne inf'].values[0]
    ic_slope_upper = resultats_df.loc[resultats_df['Paramètre'] == 'score_olympique (β₁)', 'IC 95% - Borne sup'].values[0]
    
    p_value = resultats_df.loc[resultats_df['Paramètre'] == 'score_olympique (β₁)', 'P-value'].values[0]
    
    #Prédictions
    Y_pred = intercept + slope * X
    
    #Création du graphique
    fig, ax = plt.subplots(figsize=(12, 8))
    
    #Points de données avec un style amélioré
    scatter = ax.scatter(X, Y, alpha=0.6, s=100, edgecolors='black', linewidths=1,
                        c=df_reg['annee'], cmap='viridis', label='Observations')
    
    #Droite de régression
    X_sorted = np.sort(X, axis=0)
    Y_pred_sorted = intercept + slope * X_sorted
    ax.plot(X_sorted, Y_pred_sorted, 'r-', linewidth=2.5, 
            label=f'Régression: Y = {intercept:.2f} + {slope:.2f}x')
    
    #Bandes de confiance pour la pente (illustratives)
    #Pente min et max de l'IC
    Y_pred_lower = intercept + ic_slope_lower * X_sorted
    Y_pred_upper = intercept + ic_slope_upper * X_sorted
    
    #Conversion explicite en array numpy float
    X_fill = X_sorted.flatten().astype(float)
    Y_lower_fill = Y_pred_lower.flatten().astype(float)
    Y_upper_fill = Y_pred_upper.flatten().astype(float)

    ax.fill_between(X_fill.flatten(), Y_lower_fill.flatten(), Y_upper_fill.flatten(), 
                     alpha=0.15, color='blue', label=f'IC 95% de β₁ [{ic_slope_lower:.2f}, {ic_slope_upper:.2f}]')
    
    #Légende des années
    annees_uniques = sorted(df_reg['annee'].unique())
    markers = ['o', 's', '^', 'D']  # cercle, carré, triangle, diamant

    for i, annee in enumerate(annees_uniques):
        mask = df_reg['annee'] == annee
        ax.scatter(X[mask], Y[mask], 
                  alpha=0.6, s=100, 
                  edgecolors='black', linewidths=1,
                  marker=markers[i],
                  label=f'{int(annee)}')
    
    #Labels et titre et légendes
    ax.set_xlabel('Score Olympique', fontsize=13, fontweight='bold')
    ax.set_ylabel('Score Paralympique', fontsize=13, fontweight='bold')
    ax.set_title('Régression linéaire : Score Paralympique vs Score Olympique', 
                 fontsize=15, fontweight='bold', pad=20)
    
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    return fig, ax