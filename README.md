Présentation du Sujet

Dans ce projet, nous souhaitons expliquer la différence de résultat aux jeux paralympiques entre différents pays. En effet, comment se fait-il que certains pays ramènent significativement plus de médailles (ramenées au nombre d'athlètes que d'autres ?). Dans cette étude, on cherchera alors à quels facteurs peuvent expliquer ses variation. En particulier, les dépenses publiques de l'Etat, le PIB par habitant et l'indice de développement humain peuvent-ils expliquer les résultats paralympiques.

Déroulé du projet :

Dans un premier temps, on regardera si la réussite aux jeux olympiques peut expliquer la réussite aux jeux paralympiques grâce à une régression linéaire simple d'un score paralymique (à définir) sur un score olympique (à définir). Ensuite, on regardera si les facteurs détaillés plus tôt expliquent ces résultats à travers notamment une analyse en composantes principales et une régression linéaire multiple du score paralympique sur ces paramètres.

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
Toutes ces données sont parfaitement publiques.

Présentation du dépot :

Le dépot est composé de:
- Trois dossiers (Toutes_les_df_de_depenses, Toutes_les_df_olympiques, Toutes_les_df_nationales) qui contiennent les programmes de collecte des données respectivement de dépense publique, de résultats sportifs et de caractéristiques nationales (PIB, IDH)
- Un dossier de nettoyage et de création de variables nommé Toutes_les_df_agregees
- Un dossier statistiques_descriptives contenant des matrices de corrélation entre les variables, un programme recensant les valeurs manquantes, un programme donnant les coefficients de variations des variables et un faisant des boîtes à moustaches de variables.
- Un dossier analyse contenant une ACP et une régression linéaire
- Un notebook noté ...
