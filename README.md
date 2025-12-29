QUELS SONT LES DETERMINANTS DE LA REUSSITE AUX JEUX PARALYMPIQUES ?

Présentation du Sujet

Dans ce projet, nous souhaitons expliquer la différence de résultat aux jeux paralympiques entre différents pays. En effet, comment se fait-il que certains pays ramènent significativement plus de médailles (ramenées au nombre d'athlètes) que d'autres ?. Dans cette étude, on cherchera alors à quels facteurs peuvent expliquer ses variation.

En particulier, les dépenses publiques de l'Etat, le PIB par habitant et l'indice de développement humain peuvent-ils expliquer les résultats paralympiques ?

Déroulé du projet :

La majeure partie du Notebook sera consacrée à narrer notre collecte et nettoyage des données ainsi que notre choix de base de donnée.

Après quelques statistiques descriptives, on regardera si la réussite aux jeux olympiques peut expliquer la réussite aux jeux paralympiques grâce à une régression linéaire simple d'un score paralymique (défini dans le Notebook) sur un score olympique (défini dans le Notebook). Ensuite, on regardera si les facteurs détaillés plus tôt expliquent ces résultats à travers une régression ridge du score paralympique sur ces paramètres. Puis en fonction des résultats de cette régression, nous feront soit une autre régression simple sur les paramètres significatifs (afin de voir plus précisément leur impact) soit une analyse en composantes principales pour voir à quelle mesure chaque paramètre joue un rôle.

Présentation des variables d'intérêt :

Total de médailles olympiques / paralympiques par athlète : Total de médailles obtenues si il y a eu des jeux cette année ramenées au nombre d'athlète du pays présents.
PIB par habitant : Total des richesses produites par le pays par année ramenées au nombre d'habitants
Dépenses publiques : Pourcentage du PIB dépensé par l'Etat en faveur d'un secteur précis. On s'intéressera aux dépenses publiques en Loisirs/Sports, Aménagement du territoire, Education et Maladie/Invalidité.
IDH : Score défini comme la moyenne géométrique entre des indices de santé, éducation et revenu de la population. Varie de 0 à 1 avec dans les faits, un minimum autour de 0.4 et un maximum autour de 1

Sources des données :

Dans le projet, nous avons utilisé : 
- Wikipédia pour les données olympiques et paralympiques
- Eurostat pour les données de dépenses publiques en Aménagement du territoire, Maladie/Invalidité et Loisirs/Sports
- World Bank Data pour les données de dépenses publiques en éducation et le PIB par habitant
- "Programme des Nations Unies pour le développement" pour l'IDH
- [Is the distribution of Olympic medals truly fair ? Martin Martinez PhD 2024](https://medium.com/@mmvillar/is-the-distribution-of-olympic-medals-truly-fair-378e509bf80e), un article de littérature expliquant le lien entre résultats olympiques et éducation.

Toutes ces données sont parfaitement publiques.

Présentation du dépôt :

Le dépôt est composé de:
- Trois dossiers (Toutes_les_df_de_depenses, Toutes_les_df_nationales, Toutes_les_df_olympiques) qui contiennent les programmes de collecte des données respectivement de dépense publique, de résultats sportifs et de caractéristiques nationales (PIB, IDH)
- Un dossier de nettoyage et de création de variables nommé Toutes_les_df_agregees
- Un dossier statistiques_descriptives contenant lui-même :
    - Un programme pour les matrices de corrélation entre les variables (matrice_correlation_variables)
    - Un programme recensant les valeurs manquantes (valeurs_manquantes)
    - Un programme donnant des statistiques sur la variation des données (défini dans le Notebook) (Stat_descr)
    - Un programme traçant des nuages de points (nuages_total_parametres)
    - Un programme traçant l'évolution temporelle des variables (evolution)
- Un dossier analyse contenant les régressions linéaires et la régression ridge
- Un dossier images contenant des images qui servent dans le programme (vous pouvez les supprimer, elles sont recrées à chaque éxecution du Notebook)
- Un notebook nommé Notebook_full contenant nos résultats.

Bonne correction !
