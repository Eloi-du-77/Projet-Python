from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt

df_top_12=pd.read_pickle("Toutes_les_df_agregees/df_top_12_sans_NaN.pkl")

#Sélection des variables explicatives
variables_a_exclure = [
    'pays', 'annee', 'code_du_pays',  # Identifiants
    'or_olympique', 'argent_olympique', 'bronze_olympique', 'total_medailles_olympiques',  # Variables olympiques
    'or_paralympique', 'argent_paralympique', 'bronze_paralympique', 'total_medailles_paralympiques',  # Variables paralympiques
    'score_olympique', 'score_paralympique',  # Scores à expliquer
    'or_olympique_par_athlete', 'argent_olympique_par_athlete', 
    'bronze_olympique_par_athlete', 'total_medailles_olympique_par_athlete',  # Ratios olympiques
    'or_paralympique_par_athlete', 'argent_paralympique_par_athlete',
    'bronze_paralympique_par_athlete', 'total_medailles_paralympiques_par_athlete',  # Ratios paralympiques    ''
    'maladie_invalidite_par_habitant', 'loisirs_sports_par_habitant', 'education_par_habitant',
    'amenagement_territoire_par_habitant', 'moy_amenagement_pre_jo',
    'moy_loisirs_pre_jo', 'moy_education_pre_jo', 'moy_maladie_pre_jo',
    'education', 'maladie_invalidite', 'loisirs_sports', 'amenagement_territoire',# variables non retenues
    'athletes_olympiques', "athletes_paralympiques",
    'score_olympique_moyen', 'score_paralympique_moyen', #variables sportives
    "moy_amenagement_1995"
]

#On ne conserve que les dépenses publiques moyennées depuis 1995, l'idh et le PIB par habitant
X = df_top_12.drop(columns=variables_a_exclure, errors='ignore')
X = X.select_dtypes(include=['float64', 'int64'])

#Suppression des NaN 
X_clean = X.dropna()

#Standardisation des variables explicatives
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_clean)

#ACP complète pour voir la variance
ACP_complete = PCA()
ACP_complete.fit(X_scaled)

#Graphique de la variance expliquée
plt.figure(figsize=(14, 5))

plt.subplot(1, 3, 1)
plt.bar(range(1, min(11, len(ACP_complete.explained_variance_ratio_) + 1)), 
        ACP_complete.explained_variance_ratio_[:10])
plt.xlabel('Composante')
plt.ylabel('Variance expliquée')
plt.title('Variance expliquée par composante')
plt.xticks(range(1, min(11, len(ACP_complete.explained_variance_ratio_) + 1)))

plt.subplot(1, 3, 2)
plt.plot(range(1, len(ACP_complete.explained_variance_ratio_) + 1), 
         ACP_complete.explained_variance_ratio_.cumsum(), marker='o')
plt.xlabel('Nombre de composantes')
plt.ylabel('Variance expliquée cumulée')
plt.title('Variance cumulée')
plt.axhline(y=0.8, color='r', linestyle='--', label='80%')
plt.legend()
plt.grid(True, alpha=0.3)

#ACP avec 2 composantes
ACP = PCA(n_components=2)
X_ACP = ACP.fit_transform(X_scaled)

#Construction d'une table avec les deux composantes principales
df_ACP = pd.DataFrame(
    X_ACP, 
    columns=['PC1', 'PC2'],
    index=X_clean.index
)

#Création de colonnes pays et score paralympique (un mask est nécessaire pour gérer les valeurs manquantes)
mask = df_top_12.notna().all(axis=1)

df_ACP['pays'] = df_top_12.loc[mask, 'pays']
df_ACP['score_paralympique'] = df_top_12.loc[mask, 'score_paralympique']

print(f"\n{'='*60}")
print(f"Variance expliquée par PC1 : {ACP.explained_variance_ratio_[0]:.2%}")
print(f"Variance expliquée par PC2 : {ACP.explained_variance_ratio_[1]:.2%}")
print(f"Variance totale (PC1+PC2) : {ACP.explained_variance_ratio_.sum():.2%}")
print(f"{'='*60}\n")

#Contributions des variables
loadings = pd.DataFrame(
    ACP.components_.T,
    columns=['PC1', 'PC2'],
    index=X_clean.columns
)

print("\n" + "="*60)
print("INTERPRÉTATION DES COMPOSANTES PRINCIPALES")
print("="*60)
print("\nVariables contribuant à PC1 :")
top_pc1 = loadings['PC1'].abs().sort_values(ascending=False).head()
for var, val in top_pc1.items():
    signe = "+" if loadings.loc[var, 'PC1'] > 0 else "-"
    print(f"  {signe} {var}: {abs(loadings.loc[var, 'PC1']):.3f}")

print("\nVariables contribuant à PC2 :")
top_pc2 = loadings['PC2'].abs().sort_values(ascending=False).head()
for var, val in top_pc2.items():
    signe = "+" if loadings.loc[var, 'PC2'] > 0 else "-"
    print(f"  {signe} {var}: {abs(loadings.loc[var, 'PC2']):.3f}")

#Visualisation avec coloration par score paralympique
plt.subplot(1, 3, 3)
scatter = plt.scatter(df_ACP['PC1'], df_ACP['PC2'], 
                     c=df_ACP['score_paralympique'], 
                     s=100, alpha=0.7, cmap='viridis')
plt.colorbar(scatter, label='Score Paralympique')

for idx, row in df_ACP.iterrows():
    plt.annotate(row['pays'], (row['PC1'], row['PC2']), 
                 fontsize=8, alpha=0.8)

plt.xlabel(f'PC1 ({ACP.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({ACP.explained_variance_ratio_[1]:.1%})')
plt.title('Pays selon leurs caractéristiques explicatives')
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)

plt.tight_layout()
plt.show()



#Corrélation entre les composantes principales et le score paralympique
from scipy.stats import pearsonr

#Enlever les NaN éventuels
df_ACP_clean = df_ACP.dropna(subset=['score_paralympique'])

corr_pc1, pval_pc1 = pearsonr(df_ACP_clean['PC1'], df_ACP_clean['score_paralympique'])
corr_pc2, pval_pc2 = pearsonr(df_ACP_clean['PC2'], df_ACP_clean['score_paralympique'])

print("\n" + "="*60)
print("CORRÉLATION AVEC LE SCORE OLYMPIQUE")
print("="*60)
print(f"Corrélation PC1 - Score Paralympique : {corr_pc1:.3f} (p-value: {pval_pc1:.4f})")
print(f"Corrélation PC2 - Score Paralympique : {corr_pc2:.3f} (p-value: {pval_pc2:.4f})")

#Affichage du cercle des corrélations
top_vars = loadings['PC1'].abs().add(loadings['PC2'].abs()).sort_values(ascending=False).head(12).index

plt.figure(figsize=(10, 10))
circle = plt.Circle((0, 0), 1, fill=False, color='gray', linestyle='--')
plt.gca().add_patch(circle)

for var in top_vars:
    plt.arrow(0, 0, loadings.loc[var, 'PC1'], loadings.loc[var, 'PC2'],
              head_width=0.04, head_length=0.04, fc='blue', ec='blue', alpha=0.6)
    plt.text(loadings.loc[var, 'PC1']*1.15, loadings.loc[var, 'PC2']*1.15, 
             var, fontsize=9, ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

plt.xlabel(f'PC1 ({ACP.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({ACP.explained_variance_ratio_[1]:.1%})')
plt.title('Cercle des corrélations - Variables explicatives du score Paralympique')
plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
plt.xlim(-1.2, 1.2)
plt.ylim(-1.2, 1.2)
plt.grid(True, alpha=0.3)
plt.axis('equal')
plt.tight_layout()
plt.show()

#Tracé des axes en repère orthonormé
plt.figure(figsize=(14, 10))

#Pays représentés par des points
scatter = plt.scatter(df_ACP['PC1'], df_ACP['PC2'], 
                     c=df_ACP['score_paralympique'], 
                     s=150, alpha=0.6, cmap='RdYlGn', edgecolors='black')
plt.colorbar(scatter, label='Score Paralympique')

for idx, row in df_ACP.iterrows():
    plt.annotate(row['pays'], (row['PC1'], row['PC2']), 
                 fontsize=10, weight='bold')

#Flèches représentant les variables
scale_factor = 3
for var in top_vars:
    plt.arrow(0, 0, 
              loadings.loc[var, 'PC1']*scale_factor, 
              loadings.loc[var, 'PC2']*scale_factor,
              head_width=0.2, head_length=0.2, 
              fc='red', ec='red', alpha=0.5, linewidth=2)
    plt.text(loadings.loc[var, 'PC1']*scale_factor*1.1, 
             loadings.loc[var, 'PC2']*scale_factor*1.1, 
             var, fontsize=9, color='red', weight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

plt.xlabel(f'PC1 ({ACP.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({ACP.explained_variance_ratio_[1]:.1%})')
plt.title('Biplot - Pays et variables explicatives du score olympique', fontsize=14)
plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

#%%