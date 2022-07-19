# Regroupe les manipulations de données geoJSON, à savoir :
# - Lit un fichier geojson et en extraie les communes d'une circonscription
# - Associe au GeoJSON d'une circonscription les données électorales
import copy
import json
from unidecode import unidecode
from statistics import mean


def extraire_circonscription(communes, geojson_file_name):
    communes_pas_trouvees = communes
    geo = json.load(open(geojson_file_name))
    geo_circonscription = {}
    geo_circonscription['type'] = geo['type']
    geo_circonscription['features'] = []
    # Les données de chaque commune se trouvent dans la liste 'features'
    # Chaque enregistrement de la liste, de type 'Feature', est un dictionnaire sous le format suivant :
    # 'type' = 'Feature',
    # 'geometry' = dictionnaire avec liste de coordonnées {'type': 'Polygon', 'coordinates': [[[3.3486821875225, 50.440823851679], ..., [3.3486821875225, 50.440823851679]]]}
    # 'properties' = dictionnaire avec code et nom de commune {'code': '59109', 'nom': 'Brillon'}}
    liste_longitude = []
    liste_latitude = []
    for donnes_commune in geo['features']:
        nom = unidecode(donnes_commune['properties']['nom'].lower())
        if nom in communes:
            communes_pas_trouvees.remove(nom)
            geo_commune = {}
            geo_commune['type'] = donnes_commune['type']
            geo_commune['geometry'] = donnes_commune['geometry']
            # on ajoute une clef, le nom expurgé des accents et en minuscule, pour associer les données aux zones
            geo_commune['id'] = nom
            geo_commune['properties'] = donnes_commune['properties']
            # Récupération de la première coordonnée du polygone d'une commune pour
            # approximation de la position centrale de la circonscription et centrage de la carte
            if geo_commune['geometry']['type'].lower() == 'polygon':
                liste_longitude.append(geo_commune['geometry']['coordinates'][0][0][0])
                liste_latitude.append(geo_commune['geometry']['coordinates'][0][0][1])
            else:
                liste_longitude.append(geo_commune['geometry']['coordinates'][0][0][0][0])
                liste_latitude.append(geo_commune['geometry']['coordinates'][0][0][0][1])
            geo_circonscription['features'].append(geo_commune)
    if len(communes_pas_trouvees) > 0:
        print('Communes pas trouvées : ', end='')
        print(communes_pas_trouvees)
    longitude = mean(liste_longitude)
    latitude = mean(liste_latitude)
    centre_carte = [latitude, longitude]
    return centre_carte, geo_circonscription


def ajouter_resultats(geo, resultat_candidat):
    geo_circonscription = {}
    geo_circonscription['type'] = copy.copy(geo['type'])
    geo_circonscription['features'] = []
    for donnes_commune in geo['features']:
        geo_commune = {}
        geo_commune['type'] = copy.copy(donnes_commune['type'])
        geo_commune['geometry'] = copy.deepcopy(donnes_commune['geometry'])
        geo_commune['id'] = copy.copy(donnes_commune['id'])
        geo_commune['properties'] = copy.deepcopy(donnes_commune['properties'])
        geo_commune['properties']['pourcentage'] = resultat_candidat[geo_commune['id']][0]
        geo_commune['properties']['voix'] = resultat_candidat[geo_commune['id']][1]
        geo_circonscription['features'].append(geo_commune)
    return geo_circonscription

if __name__ == '__main__':
    communes = ['aulnoye-aymeries', 'dunkerque', 'berlaimont']
    geojson_file_name = 'communes-59-nord.geojson'
    centre_carte, geo_circonscription = extraire_circonscription(communes, geojson_file_name)
    print(geo_circonscription)
    print(centre_carte)
