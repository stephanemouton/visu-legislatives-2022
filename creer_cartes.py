import actions_carte

departement = '59'
circonscription = '12'
fichier_geojson = 'geojsons/communes-59-nord.geojson'
resultat = "resultats/circo_059_012.html"
actions_carte.cree_carte_circonscription(departement, circonscription, fichier_geojson, resultat)
