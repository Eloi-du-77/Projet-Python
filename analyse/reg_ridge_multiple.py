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
    avec validation croisée pour choisir le meilleur paramètre de pénalisation
    """
    #On prépare les données
    variables_X = ['pib_habitant', 'idh', 'moy_amenagement_2008', 
                   'moy_maladie_2008', 'moy_education_2008', 'moy_loisirs_2008']
    
    colonnes_necessaires = ['pays', 'annee', 'score_paralympique'] + variables_X
    df_reg = df[colonnes_necessaires].dropna()

    #On standardise car c'est obligatoire en ridge
    scaler = StandardScaler()
    
    X_original = df_reg[variables_X].values.astype(np.float64)
    X = scaler.fit_transform(X_original)
    Y = df_reg['score_paralympique'].values.astype(np.float64)

    #Régression Ridge avec validation croisée pour le meilleur alpha
    alphas = np.logspace(-3, 3, 100)  #On teste 100 valeurs d'alpha entre 0.001 et 1000 réparties par échelle log
    model = RidgeCV(alphas=alphas, cv=5, scoring='r2')  #Validation croisée à 5 sous ensembles
    model.fit(X, Y)

    #Régression
    Y_pred = model.predict(X)

    #Calcul du nombre de variables, du R², R² ajusté
    n = len(Y)
    k = len(variables_X)
    residuals = Y - Y_pred
    mse = np.sum(residuals**2) / (n - k - 1)
    r2 = model.score(X, Y)
    r2_adj = 1 - (1-r2)*(n-1)/(n-k-1)
    

    #Calcul approché de la matrice de variance-covariance
    X_with_intercept = np.column_stack([np.ones(n), X]).astype(np.float64)
    alpha = model.alpha_
    XtX = X_with_intercept.T @ X_with_intercept

    #Ajouter la pénalité Ridge (sauf sur l'intercept)
    ridge_penalty = np.diag([0] + [alpha] * k)
    
    try:
        var_covar_matrix = mse * np.linalg.inv(XtX + ridge_penalty) @ XtX @ np.linalg.inv(XtX + ridge_penalty)
        
        #Erreurs standard
        se_intercept = np.sqrt(var_covar_matrix[0, 0])
        se_coefficients = np.sqrt(np.diag(var_covar_matrix[1:, 1:]))
        
        #Statistiques de student et p valeurs
        t_intercept = model.intercept_ / se_intercept
        t_coefficients = model.coef_ / se_coefficients
        
        p_intercept = 2 * (1 - stats.t.cdf(abs(t_intercept), n - k - 1))
        p_coefficients = 2 * (1 - stats.t.cdf(np.abs(t_coefficients), n - k - 1))
        
        #Intervalles de confiance à 95%
        t_critical = stats.t.ppf(0.975, n - k - 1)
        
        ic_intercept_lower = model.intercept_ - t_critical * se_intercept
        ic_intercept_upper = model.intercept_ + t_critical * se_intercept
        
        ic_coefficients_lower = model.coef_ - t_critical * se_coefficients
        ic_coefficients_upper = model.coef_ + t_critical * se_coefficients
        
        has_inference = True
        
    except:
        #Si jamais on a mal codé quelque chose ou que l'argument est mauvais, on renvoit des nan
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

    #Création d'un df de résultats
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

    #Affichage
    print(" "*80)
    print("RÉSULTATS DE LA RÉGRESSION RIDGE (VARIABLES STANDARDISÉES)")
    print(" "*80)
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
    
    print("\n" + " "*80)
    print("COEFFICIENTS STANDARDISÉS ET INTERVALLES DE CONFIANCE") #Il n'y a rien sous-ça, c'est fait pour que le df s'affiche grâce au format notebook
    print(" "*80)
    
    return resultats, scaler, model
