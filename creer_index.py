# visu-legislatives-2022 : expérimentation de Folium pour représenter la répartition géographique des législatives françaises de 2022
# Création des index de consultation
#   Par Région
#       Par Département
#            Par circonscription
# pour

import csv
from unidecode import unidecode
import actions_db


def filtre_nom(nom_brut):
    # nom = unidecode(nom_brut)
    return nom_brut


def filtre_reference(nom_brut):
    return nom_brut.lower().replace(" ", "-").replace("'", "")


def dictionnaire_departements_par_regions():
    regions = {}
    with open("departements-france.csv", newline="") as csvfile:
        lecteur = csv.reader(csvfile, delimiter=",")
        next(lecteur)
        for ligne in lecteur:
            nom_departement = filtre_nom(ligne[1])
            code_departement = ligne[0]
            nom_region = filtre_nom(ligne[3])
            if nom_region in regions:
                regions[nom_region][nom_departement] = code_departement
                # print(regions[nom_region])
            else:
                departements = {}
                departements[nom_departement] = code_departement
                regions[nom_region] = departements
                # print(regions[nom_region])
    return dict(sorted(regions.items(), key=lambda x: x[0]))


if __name__ == "__main__":

    conf_fr = {"fichier": "legislatives_2022_fr.md", "resultats": "Résultats", "circonscriptions": "Circonscriptions "}
    conf_en = {"fichier": "legislatives_2022_en.md", "resultats": "Results", "circonscriptions": "Constituencies"}
    configurations = [conf_fr, conf_en]

    for configuration in configurations:
        with open(configuration["fichier"], "w") as f:
            regions = {}
            regions = dictionnaire_departements_par_regions()

            f.write("# " + configuration["resultats"] + "\n\n")
            for region in regions:
                f.write(
                    "* **["
                    + region
                    + ']({{<ref "#'
                    + filtre_reference(region)
                    + '" >}})**\n'
                )
                departements_non_tries = regions[region]
                departements = dict(
                    sorted(departements_non_tries.items(), key=lambda x: x[0])
                )
                f.write("   * ")
                premier = True
                for departement in departements:
                    if premier:
                        premier = False
                    else:
                        f.write(", ")
                    f.write(
                        "["
                        + departement
                        + ']({{<ref "#'
                        + filtre_reference(departement)
                        + '" >}})'
                    )
                f.write("\n\n")

            for region in regions:
                f.write("## {}\n\n".format(region))
                departements_non_tries = regions[region]
                departements = dict(
                    sorted(departements_non_tries.items(), key=lambda x: x[0])
                )
                for departement in departements:
                    f.write("### {}\n\n".format(departement))
                    # On génère par circonscriptions
                    code_dpt = departements[departement]
                    code_db_dpt = code_dpt
                    # Traitement "manuel" d'une poignée d'exceptions
                    if code_dpt == "971":
                        code_db_dpt = "ZA"  # Guadeloupe
                    if code_dpt == "972":
                        code_db_dpt = "ZB"  # Martinique
                    if code_dpt == "973":
                        code_db_dpt = "ZC"  # Guyane
                    if code_dpt == "974":
                        code_db_dpt = "ZD"  # La Réunion
                    if code_dpt == "976":
                        code_db_dpt = "ZM"  # Mayotte
                    circonscriptions = actions_db.obtenir_circonscriptions(code_db_dpt)
                    f.write("* " + configuration["circonscriptions"] + ": ")
                    premier = True
                    for circonscription in circonscriptions:
                        if premier:
                            premier = False
                        else:
                            f.write(", ")
                        f.write(
                            "["
                            + circonscription
                            + "](/fr_legislatives_2022/circo_"
                            + code_dpt.rjust(3, "0")
                            + "_"
                            + circonscription
                            + ".html)"
                        )
                    f.write("\n\n")


# departement = '59'
# circonscription = '12'
# fichier_geojson = 'geojsons/communes-59-nord.geojson'
# resultat = "fr_legislatives_2022/circo_059_012.html"
# actions_carte.cree_carte_circonscription(departement, circonscription, fichier_geojson, resultat)
