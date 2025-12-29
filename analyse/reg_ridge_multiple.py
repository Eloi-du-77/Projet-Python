import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy import stats
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import RidgeCV

def regression_ridge(df):
    """Fais la régression Ridge de score_paralympique sur plusieurs variables
    avec validation croisée pour choisir le paramètre de régularisation optimal
    """
    
    # Variables explicatives
    variables_X = ['pib_habitant', 'idh', 'moy_amenagement_2008', 
                   'moy_maladie_2008', 'moy_education_2008', 'moy_loisirs_2008']
    
    # Préparer les données pour la régression
    colonnes_necessaires = ['pays', 'annee', 'score_paralympique'] + variables_X
    df_reg = df[colonnes_necessaires].dropna()

    # Standardisation des variables explicatives (OBLIGATOIRE pour Ridge)
    scaler = StandardScaler()
    
    X_original = df_reg[variables_X].values.astype(np.float64)
    X = scaler.fit_transform(X_original)
    Y = df_reg['score_paralympique'].values.astype(np.float64)

    # Régression Ridge avec validation croisée pour alpha optimal
    alphas = np.logspace(-3, 3, 100)  # Teste 100 valeurs d'alpha entre 0.001 et 1000
    model = RidgeCV(alphas=alphas, cv=5, scoring='r2')  # 5-fold cross-validation
    model.fit(X, Y)

    # Prédictions
    Y_pred = model.predict(X)

    # Calcul des statistiques
    n = len(Y)
    k = len(variables_X)
    residuals = Y - Y_pred
    mse = np.sum(residuals**2) / (n - k - 1)
    r2 = model.score(X, Y)
    r2_adj = 1 - (1-r2)*(n-1)/(n-k-1)
    
    # Pour Ridge, on peut approximer les erreurs standard
    # (pas de formule exacte car les coefficients sont biaisés)
    # On utilise une approximation bootstrap ou on les calcule de manière approchée
    
    # Calcul approché de la matrice de variance-covariance
    X_with_intercept = np.column_stack([np.ones(n), X]).astype(np.float64)
    
    # Matrice Ridge : (X'X + αI)^(-1)
    alpha = model.alpha_
    XtX = X_with_intercept.T @ X_with_intercept
    # Ajouter la pénalité Ridge (pas sur l'intercept)
    ridge_penalty = np.diag([0] + [alpha] * k)
    
    try:
        var_covar_matrix = mse * np.linalg.inv(XtX + ridge_penalty) @ XtX @ np.linalg.inv(XtX + ridge_penalty)
        
        # Erreurs standard
        se_intercept = np.sqrt(var_covar_matrix[0, 0])
        se_coefficients = np.sqrt(np.diag(var_covar_matrix[1:, 1:]))
        
        # Statistiques t et p-values (approximatives pour Ridge)
        t_intercept = model.intercept_ / se_intercept
        t_coefficients = model.coef_ / se_coefficients
        
        p_intercept = 2 * (1 - stats.t.cdf(abs(t_intercept), n - k - 1))
        p_coefficients = 2 * (1 - stats.t.cdf(np.abs(t_coefficients), n - k - 1))
        
        # Intervalles de confiance à 95%
        t_critical = stats.t.ppf(0.975, n - k - 1)
        
        ic_intercept_lower = model.intercept_ - t_critical * se_intercept
        ic_intercept_upper = model.intercept_ + t_critical * se_intercept
        
        ic_coefficients_lower = model.coef_ - t_critical * se_coefficients
        ic_coefficients_upper = model.coef_ + t_critical * se_coefficients
        
        has_inference = True
        
    except:
        # Si le calcul échoue, on met des NaN
        se_intercept = np.nan
        se_coefficients = np.full(k, np.nan)
        t_intercept = np.nan
        t_coefficients = np.full(k, np.nan)
        p_intercept = np.nan
        p_coefficients = np.full(k, np.nan)
        ic_intercept_lower = np.nan
        ic_intercept_upper = np.nan
        ic_coefficients_lower = np.full(k, np.nan)
        ic_coefficients_upper = np.full(k, np.nan)
        has_inference = False

    # Création du DataFrame de résultats
    parametres = ['Intercept (β₀)'] + [f'{var} (β{i+1})' for i, var in enumerate(variables_X)]
    coefficients = [model.intercept_] + list(model.coef_)
    
    if has_inference:
        erreurs_standard = [se_intercept] + list(se_coefficients)
        ic_inf = [ic_intercept_lower] + list(ic_coefficients_lower)
        ic_sup = [ic_intercept_upper] + list(ic_coefficients_upper)
        statistiques_t = [t_intercept] + list(t_coefficients)
        p_values = [p_intercept] + list(p_coefficients)
    else:
        erreurs_standard = [np.nan] * (k + 1)
        ic_inf = [np.nan] * (k + 1)
        ic_sup = [np.nan] * (k + 1)
        statistiques_t = [np.nan] * (k + 1)
        p_values = [np.nan] * (k + 1)
    
    resultats = pd.DataFrame({
        'Paramètre': parametres,
        'Coefficient (std)': coefficients,
        'Erreur Standard': erreurs_standard,
        'IC 95% - Borne inf': ic_inf,
        'IC 95% - Borne sup': ic_sup,
        'Statistique t': statistiques_t,
        'P-value': p_values
    })

    # Affichage des informations générales
    print("="*80)
    print("RÉSULTATS DE LA RÉGRESSION RIDGE (VARIABLES STANDARDISÉES)")
    print("="*80)
    print(f"\nModèle : score_paralympique = β₀ + β₁×pib_habitant + β₂×idh + β₃×moy_amenagement_2008")
    print(f"         + β₄×moy_maladie_2008 + β₅×moy_education_2008 + β₆×moy_loisirs_2008 + ε")
    print(f"\nNombre d'observations : {n}")
    print(f"Alpha optimal : {alpha:.6f}")
    print(f"R² : {r2:.4f}")
    print(f"R² ajusté : {r2_adj:.4f}")
    print(f"Erreur standard résiduelle : {np.sqrt(mse):.4f}")
    
    if not has_inference:
        print("\nLes erreurs standard et p-values ne sont pas disponibles")
        print("Seuls les coefficients sont fiables.")
    
    print("\n" + "="*80)
    print("COEFFICIENTS STANDARDISÉS ET INTERVALLES DE CONFIANCE")
    print("="*80)
    
    return resultats, scaler, model


def plot_regression_ridge(df, resultats_df, model):
    """Trace les graphiques de diagnostic pour la régression Ridge
    """
    
    # Variables explicatives
    variables_X = ['pib_habitant', 'idh', 'moy_amenagement_2008', 
                   'moy_maladie_2008', 'moy_education_2008', 'moy_loisirs_2008']
    
    # Préparer les données
    colonnes_necessaires = ['pays', 'annee', 'score_paralympique'] + variables_X
    df_reg = df[colonnes_necessaires].dropna()
    
    # Standardisation
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    
    X_original = df_reg[variables_X].values.astype(np.float64)
    X = scaler.fit_transform(X_original)
    Y = df_reg['score_paralympique'].values.astype(np.float64)
    
    # Prédictions et résidus
    Y_pred = model.predict(X)
    residuals = Y - Y_pred
    
    # Créer une figure avec 3 sous-graphiques
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Résidus vs valeurs prédites
    ax1 = axes[0, 0]
    ax1.scatter(Y_pred, residuals, alpha=0.6, s=80, edgecolors='black', linewidths=1)
    ax1.axhline(y=0, color='r', linestyle='--', linewidth=2)
    ax1.set_xlabel('Valeurs prédites', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Résidus', fontsize=11, fontweight='bold')
    ax1.set_title('Résidus vs Valeurs Prédites', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # 2. Q-Q plot
    ax2 = axes[0, 1]
    stats.probplot(residuals, dist="norm", plot=ax2)
    ax2.set_title('Q-Q Plot des Résidus', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # 3. Importance des coefficients standardisés
    ax3 = axes[1, 0]
    
    coefficients_std = model.coef_
    colors = ['green' if c > 0 else 'red' for c in coefficients_std]
    bars = ax3.barh(range(len(variables_X)), coefficients_std, color=colors, alpha=0.7, edgecolor='black')
    ax3.set_yticks(range(len(variables_X)))
    ax3.set_yticklabels([v.replace('_', ' ').replace('moy ', '') for v in variables_X], fontsize=9)
    ax3.set_xlabel('Coefficients standardisés (Ridge)', fontsize=11, fontweight='bold')
    ax3.set_title(f'Importance Relative des Variables (α={model.alpha_:.4f})', fontsize=12, fontweight='bold')
    ax3.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax3.grid(True, alpha=0.3, linestyle='--', axis='x')
    
    # 4. Valeurs observées vs prédites
    ax4 = axes[1, 1]
    
    # Créer des couleurs discrètes pour les années
    annees_uniques = sorted(df_reg['annee'].unique())
    colors_map = plt.cm.viridis(np.linspace(0, 1, len(annees_uniques)))
    annee_to_color = {annee: colors_map[i] for i, annee in enumerate(annees_uniques)}
    point_colors = [annee_to_color[annee] for annee in df_reg['annee']]
    
    ax4.scatter(Y, Y_pred, alpha=0.6, s=80, edgecolors='black', linewidths=1, c=point_colors)
    
    # Ligne de référence y=x
    min_val = min(Y.min(), Y_pred.min())
    max_val = max(Y.max(), Y_pred.max())
    ax4.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Prédiction parfaite')
    
    ax4.set_xlabel('Valeurs observées', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Valeurs prédites', fontsize=11, fontweight='bold')
    ax4.set_title('Valeurs Observées vs Prédites', fontsize=12, fontweight='bold')
    ax4.legend(loc='lower right', fontsize=9)
    ax4.grid(True, alpha=0.3, linestyle='--')
    
    # Légende pour les années
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors_map[i], edgecolor='black', 
                             label=f'{int(annee)}') 
                       for i, annee in enumerate(annees_uniques)]
    ax4.legend(handles=legend_elements, title='Année', 
              loc='upper left', fontsize=9, framealpha=0.9)
    
    plt.tight_layout()
    
    return fig, axes