# visu-legislatives-2022 : expérimentation de Folium pour représenter la répartition géographique des législatives françaises de 2022
# Regroupe les fonctions utilitaires de traitement de chaînes

from unidecode import unidecode

# Les noms de communes sont utilisés comme clefs entre les informations geoJSON et les données électorales
# En conséquence, ils sont simplifiés (pas d'accents, pas de pronoms) pour éviter les erreurs d'association
def nom_simplifie(nom_original):
    pronoms = ["le ", "la ", "les ", "l'"]
    nom = unidecode(nom_original.lower())
    for pronom in pronoms:
        if nom.startswith(pronom):
            nom = nom[len(pronom):]
    nom = nom.replace("'", "-")
    nom = nom.replace(' ', '-')
    return nom
