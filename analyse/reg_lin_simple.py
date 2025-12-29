import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy import stats
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def regression_simple(df, param):
    """Fais la régression simple de score_paralympique sur un paramètre
    et retourne un DataFrame avec tous les résultats
    
    Si param commence par 'moy_', la variable est standardisée
    """

    df_reg = df[['pays', 'annee', param, 'score_paralympique']].dropna()

    #On vérifie si il faut standardiser, comme on utilise cette fonction que pour param = score_paralympique ou param = moy_education_2008, on dit que
    #si param commence par moy, on standardise
    standardiser = param.startswith('moy_')
    
    if standardiser:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X = scaler.fit_transform(df_reg[[param]].values.astype(np.float64))
        note_standardisation = " (standardisé)"
    else:
        X = df_reg[[param]].values
        scaler = None
        note_standardisation = ""
    
    Y = df_reg['score_paralympique'].values

    #On régresse
    model = LinearRegression()
    model.fit(X, Y)

    #Prédictions
    Y_pred = model.predict(X)

    #Calcul du R², R² ajusté, nombre d'observations
    n = len(Y)
    k = 1 
    residuals = Y - Y_pred
    mse = np.sum(residuals**2) / (n - k - 1)
    r2 = model.score(X, Y)
    r2_adj = 1 - (1-r2)*(n-1)/(n-k-1)
    
    #Erreurs standard
    var_X = np.sum((X - X.mean())**2)
    se_slope = np.sqrt(mse / var_X)
    se_intercept = np.sqrt(mse * (1/n + X.mean()**2 / var_X))

    #Statistiques t et p valeurs
    t_slope = model.coef_[0] / se_slope
    t_intercept = model.intercept_ / se_intercept
    p_slope = 2 * (1 - stats.t.cdf(abs(t_slope), n - k - 1))
    p_intercept = 2 * (1 - stats.t.cdf(abs(t_intercept), n - k - 1))

    #Intervalles de confiance à 95%
    t_critical = stats.t.ppf(0.975, n - k - 1)  #valeur critique pour alpha=0.05 en test bilatéral
    
    ic_intercept_lower = model.intercept_ - t_critical * se_intercept
    ic_intercept_upper = model.intercept_ + t_critical * se_intercept
    
    ic_slope_lower = model.coef_[0] - t_critical * se_slope
    ic_slope_upper = model.coef_[0] + t_critical * se_slope

    #Création du df de résultats
    resultats = pd.DataFrame({
        'Paramètre': ['Intercept (β₀)', param + note_standardisation + ' (β₁)'],
        'Coefficient': [model.intercept_, model.coef_[0]],
        'Erreur Standard': [se_intercept, se_slope],
        'IC 95% - Borne inf': [ic_intercept_lower, ic_slope_lower],
        'IC 95% - Borne sup': [ic_intercept_upper, ic_slope_upper],
        'Statistique t': [t_intercept, t_slope],
        'P-value': [p_intercept, p_slope]
    })

    #Affichage
    print(" "*80)
    print("RÉSULTATS")
    print(" "*80)
    print(f"\nModèle : score_paralympique = β₀ + β₁ × {param}{note_standardisation} + ε")
    if standardiser:
        print(f"On a standardisé {param} (moyenne=0, écart-type=1)")
        print(f"Ecart-type avant standardisation : {df_reg[param].std()}")
    print(f"\nNombre d'observations : {n}")
    print(f"R² : {r2:.4f}")
    print(f"R² ajusté : {r2_adj:.4f}")
    print(f"Erreur standard résiduelle : {np.sqrt(mse):.4f}")

    #On retourne aussi le scaler si standardisation
    if standardiser:
        return resultats, scaler
    else:
        return resultats


def plot_regression_simple(df, resultats_df, param):
    """Trace la régression linéaire de score_paralympique sur param
    à partir des résultats de la fonction regression_simple()
    
    Si param commence par 'moy_', la variable est standardisée
    """
    
    df_reg = df[['pays', 'annee', param, 'score_paralympique']].dropna()
    
    #Vérifie si on doit standardiser
    standardiser = param.startswith('moy_')
    
    if standardiser:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X = scaler.fit_transform(df_reg[[param]].values.astype(np.float64))
        note_standardisation = " (standardisé)"
        x_label = param + " (standardisé)"
    else:
        X = df_reg[[param]].values
        note_standardisation = ""
        x_label = param
    
    Y = df_reg['score_paralympique'].values
    n = len(Y)
    
    #Extraire les paramètres du df de résultat
    if standardiser :
        resultats_df = resultats_df[0]  
        intercept = resultats_df.loc[resultats_df['Paramètre'] == 'Intercept (β₀)', 'Coefficient'].iloc[0]
    else :
        intercept = resultats_df.loc[resultats_df['Paramètre'] == 'Intercept (β₀)', 'Coefficient'].values[0]
    
    #Le nom du paramètre dans resultats_df inclut la note de standardisation
    param_name = param + note_standardisation + ' (β₁)'
    slope = resultats_df.loc[resultats_df['Paramètre'] == param_name, 'Coefficient'].values[0]
    ic_slope_lower = resultats_df.loc[resultats_df['Paramètre'] == param_name, 'IC 95% - Borne inf'].values[0]
    ic_slope_upper = resultats_df.loc[resultats_df['Paramètre'] == param_name, 'IC 95% - Borne sup'].values[0]
    p_value = resultats_df.loc[resultats_df['Paramètre'] == param_name, 'P-value'].values[0]
    
    #On note la prédiction
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
    
    # Bandes de confiance pour la pente (on a moins de 5% de chances d'être dans ces bandes)
    #On trace donc la pente min et max de l'IC
    Y_pred_lower = intercept + ic_slope_lower * X_sorted
    Y_pred_upper = intercept + ic_slope_upper * X_sorted
    
    #Conversion
    X_fill = X_sorted.flatten().astype(float)
    Y_lower_fill = Y_pred_lower.flatten().astype(float)
    Y_upper_fill = Y_pred_upper.flatten().astype(float)

    ax.fill_between(X_fill.flatten(), Y_lower_fill.flatten(), Y_upper_fill.flatten(), 
                     alpha=0.15, color='blue', label=f'IC 95% de β₁ [{ic_slope_lower:.2f}, {ic_slope_upper:.2f}]')
    
    annees_uniques = sorted(df_reg['annee'].unique())
    markers = ['o', 's', '^', 'x']  #fans de Playstation, nous marquons les points par cercle, carré, triangle, croix

    for i, annee in enumerate(annees_uniques):
        mask = df_reg['annee'] == annee
        ax.scatter(X[mask], Y[mask], 
                  alpha=0.6, s=100, 
                  edgecolors='black', linewidths=1,
                  marker=markers[i],
                  label=f'{int(annee)}')
    
    #Labels et titre et légendes
    ax.set_xlabel(x_label, fontsize=13, fontweight='bold')
    ax.set_ylabel('Score Paralympique', fontsize=13, fontweight='bold')
    ax.set_title('Régression linéaire : Score Paralympique vs ' + param, 
                 fontsize=15, fontweight='bold', pad=20)
    
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    return fig, ax