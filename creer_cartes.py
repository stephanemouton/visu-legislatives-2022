# visu-legislatives-2022 : expérimentation de Folium pour représenter la répartition géographique des législatives françaises de 2022
# Création des cartes de résultat à l'aide de la liste des départements
import csv
from unidecode import unidecode
import actions_carte
import actions_db

def filtre_nom(nom_brut):
    nom = unidecode(nom_brut.lower())
    nom = nom.replace(' ', '-')
    nom = nom.replace("'", '-')
    return nom

def genere_liste_departements():
    departements = {}
    with open('departements-france.csv', newline='') as csvfile:
        lecteur = csv.reader(csvfile, delimiter=',')
        next(lecteur)
        for ligne in lecteur:
            departements[ligne[0]] = filtre_nom(ligne[1])
    return departements

if __name__ == '__main__':
    departements = genere_liste_departements()

    for code_dpt, nom_dpt in departements.items():
        code_db_dpt = code_dpt
        # Traitement "manuel" d'une poignée d'exceptions
        if code_dpt == '971':
                code_db_dpt = 'ZA' # Guadeloupe
        if code_dpt == '972':
                code_db_dpt = 'ZB' # Martinique
        if code_dpt == '973':
                code_db_dpt = 'ZC' # Guyane
        if code_dpt == '974':
                code_db_dpt = 'ZD' # La Réunion
        if code_dpt == '976':
                code_db_dpt = 'ZM' # Mayotte
        # On génère par circonscriptions
        circonscriptions = actions_db.obtenir_circonscriptions(code_db_dpt)
        for circonscription in circonscriptions:
            print('================================')
            print('Département = ' + code_db_dpt + ', circonscription = ' + circonscription)
            fichier_geojson = 'geojsons/communes-{}-{}.geojson'.format(code_dpt, nom_dpt)
            # print('Fichier geoJSON = ' + fichier_geojson)
            code_dpt_fichier = code_dpt
            if len(code_dpt_fichier) == 2:
                code_dpt_fichier = '0' + code_dpt_fichier
            fichier_resultat = 'resultats/circo_{}_{}.html'.format(code_dpt_fichier, circonscription)
            # print('Fichier résultat = ' + fichier_resultat)
            actions_carte.cree_carte_circonscription(code_db_dpt, circonscription, fichier_geojson, fichier_resultat)

    # departement = '59'
    # circonscription = '12'
    # fichier_geojson = 'geojsons/communes-59-nord.geojson'
    # resultat = "resultats/circo_059_012.html"
    # actions_carte.cree_carte_circonscription(departement, circonscription, fichier_geojson, resultat)
