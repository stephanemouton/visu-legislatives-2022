# Carte des résultats du second tour des législatives 2022

Les résultats des législatives sont donnés par circonscription, mais quelle est la répartition des votes par commune ? C'est ce que je me propose de visualiser.

## Mode d'emploi


## Documentation

L'objectif est de générer les cartes des résultats à l'aide de folium et de scripts python.

### Documentation de référenceFolium

* [Le site de Folium](https://python-visualization.github.io/folium/quickstart.html)

### Tutoriels Folium

* https://fxjollois.github.io/cours-2016-2017/analyse-donnees-massives-tp9.html
* https://autogis-site.readthedocs.io/en/latest/notebooks/L5/02_interactive-map-folium.html
* **Attention : page sur medium.com, sujette à restriction d'accès** [A Python Tutorial on Geomapping using Folium and GeoPandas](https://medium.com/@jade.adams517/using-geopandas-and-folium-to-build-maps-on-python-c51c5aad5f44) l'article montre les grands principes mais effectue trop de simplifications dans l'usage de Pandas pour être facilement généralisable.
* [Création d'une carte interactive en utilisant le langage Python ](https://www.data.gouv.fr/fr/reuses/creation-dune-carte-interactive-en-utilisant-le-langage-python/) mais l'information est véritablement sur le github https://github.com/Guillaume-Fgt/Folium_Villes_Fleuries_Idf avec un exemple inspirant.

### Articles et inspiration

* [Comment créer une carte de données avec folium ?](https://www.lasalledutemps.fr/articles/2020-03/Generer-une-carte-avec-folium.html) : L'exemple n'est pas complet, et le code source n'est pas disponible, mais il est inspirant dans les grandes ligens et mentionne le site de Grégoire David pour les données GeoJSON
* **Attention : page sur medium.com, sujette à restriction d'accès** [How to step up your Folium Choropleth Map skills](https://towardsdatascience.com/how-to-step-up-your-folium-choropleth-map-skills-17cf6de7c6fe) Encore trop lié à Pandas mais donne de bonnes idées sur l'utilsiation des *layers* et de la légende.
* **Attention : page sur medium.com, sujette à restriction d'accès** [Folium and Choropleth Map: From Zero to Pro](https://towardsdatascience.com/folium-and-choropleth-map-from-zero-to-pro-6127f9e68564) L'article qui m'a vraiment permis de progresser.
* **Attention : page sur medium.com, sujette à restriction d'accès** [The Battle of Choropleths — Part 3 — Folium](https://towardsdatascience.com/the-battle-of-choropleths-part-3-folium-86ab1232afc) Pour aller plus loins.

### Résolutions de problèmes et détails pointus sur Folium

* *StackOverflow, évidemment* [Faire apparaître un 'tooltip' sur un choropleth](https://stackoverflow.com/questions/70471888/text-as-tooltip-popup-or-labels-in-folium-choropleth-geojson-polygons)
* *StackOverflow, évidemment* [L'usage des tooltips provoque un affichage moche bleu autour du choropleth, comment l'enlever ?](https://stackoverflow.com/questions/72376003/how-to-remove-bold-blue-outline-color-from-folium-choropleth-within-an-folium-fe)
* *StackOverflow, évidemment* [Comment faire pour que la couche (*layer*) du tooltip soit complètement transparente et n'affecte pas la couleur du chropleth ?](https://stackoverflow.com/questions/53367522/passing-transparency-style-to-geojson-in-folium) 
* *StackOverflow, évidemment* [Ajouter un titre à une carte](https://stackoverflow.com/questions/61928013/adding-a-title-or-text-to-a-folium-map)

## Sources de données

### Données électorales

* Les résultats officiels, [sur le site du Ministère de l'Intérieur](https://www.resultats-elections.interieur.gouv.fr/legislatives-2022/).
* Les résultats, commune par commune, pour la France entière : [resultats-par-niveau-subcom-t2-france-entiere.txt](https://www.data.gouv.fr/fr/datasets/r/3b43be76-1b94-4f0e-b9d6-d85981c975bd)

*Note :* je n'ai pas trouvé de fichiers avec les résultats finaux, comme sur le site officiel et j'ai donc "calculé" les résultats.

### Données géographiques

* Des fichiers CSV avec les listes des [départements](https://www.data.gouv.fr/fr/datasets/departements-de-france/) et des [régions](https://www.data.gouv.fr/fr/datasets/regions-de-france/) de France.
* GeoJSON de France, dont les communes, sur l'excellent site de Grégoire David : https://france-geojson.gregoiredavid.fr/
* Données initiales sur les communes : https://www.data.gouv.fr/fr/datasets/contours-des-communes-de-france-simplifie-avec-regions-et-departement-doutre-mer-rapproches/

