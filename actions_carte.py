# visu-legislatives-2022 : expérimentation de Folium pour représenter la répartition géographique des législatives françaises de 2022
# Création des cartes par circonscription

import folium
import actions_db
import actions_geojson
import pandas as pd


def liste_simplifiee_de_noms(communes):
    noms_communes = []
    for commune in communes:
        nom = commune[22]
        noms_communes.append(nom)
    return noms_communes


def cree_carte_circonscription(departement, circonscription, fichier_geojson, resultat):
    # Valeurs possibles de la palette (qui doit avoir au moins 3 entrées pour 3 candidats)
    # * sequential
    #   * multihue: YlGn,YlGnBu,GnBu,BuGn,PuBuGn,PuBu,BuPu,RdPu,PuRd,OrRd,YlOrRd,YlOrBr
    #   * singlehue: Purples,Blues,,Oranges,Reds,Greys
    # * diverging: PuOr,BrBG,PRGn,PiYG,RdBu,RdGy,RdYlBu,Spectral,RdYlGn
    palette_couleur = ["PuBu", "PuRd", "YlGn"]

    # On commence par récupérer les informations électorales de la circonscription.
    communes = actions_db.extraire_circonscription(departement, circonscription)

    # Les noms de communes servent de clefs
    noms_communes = liste_simplifiee_de_noms(communes)

    # Création du tableau de valeurs pour le choropleth avec les colonnes suivantes :
    # - 'id' : nom simplifié de communes
    # - 'candidat1' (prénom + nom + nuance candidat 1) : % voix candidat 1
    # - 'candidat2' (prénom + nom + nuance candidat 2) : % voix candidat 2
    # (éventuellement on recommence si candidat 3)

    # Tout d'abord on détermine le nombre de candidats et leur ordre
    ordre_candidat = {}
    colonnes = []
    colonnes.append('id')
    for candidat in communes[0][24]:
        nom_complet = candidat[5] + ' ' + candidat[4] + ' (' + candidat[6] + ')'
        nb_panneau = candidat[2]
        ordre_candidat[nb_panneau] = nom_complet
        colonnes.append(nom_complet)
        # colonnes.append('pourcent '+nom_complet)
    # Ensuite on remplit le tableau
    nb_lignes = 0
    donnees = []
    for commune in communes:
        ligne = []
        valeurs = {}
        valeurs['id'] = commune[22]
        for candidat in commune[24]:
            valeurs[ordre_candidat[candidat[2]]] = candidat[9]
        for colonne in colonnes:
            ligne.append(valeurs[colonne])
        donnees.append(ligne)
        nb_lignes += 1
    # Enfin on remplit le DataFrame qui va être utilisé dans le choropleth
    df = pd.DataFrame(donnees, columns=colonnes)

    # On passe maintenant à la préparation des données, ajoutées au GeoJSON pour afficher les résultats électoraux
    resultat_candidat = {}
    # for candidat in ordre_candidat:
    #     resultats_candidat[ordre_candidat[candidat]] = []

    for id_panneau, nom in ordre_candidat.items():
        resultat_candidat[nom] = {}

    for commune in communes:
        id_commune = commune[22]
        for candidat in commune[24]:
            id_candidat = candidat[2]
            pourcentage = candidat[9]
            voix = candidat[7]
            resultat_commune_candidat = [pourcentage, voix]
            resultat_candidat[ordre_candidat[id_candidat]][id_commune] = resultat_commune_candidat

    # On prépare l'affichage en commençant par extraire les informations geoJSON de la "circo"
    centre_carte, geo = actions_geojson.extraire_circonscription(noms_communes, fichier_geojson)
    # On exploite les données des résultats par candidat
    geojson_candidat = {}

    for id_panneau, nom in ordre_candidat.items():
        geojson_candidat[nom] = actions_geojson.ajouter_resultats(geo, resultat_candidat[nom])

    # création de map centrée sur la moyenne de la première valeur de polygone de chaque commune
    # (c'est une approximation simple qui semble donner de bons résultats)
    m = folium.Map(
        location=centre_carte,
        zoom_start=10,
        tiles=None,
    )
    folium.TileLayer("CartoDB positron", name="Light Map", control=False).add_to(m)

    choropleth = {}
    index_palette = 0
    for id_panneau, nom in ordre_candidat.items():
        choropleth[nom] = folium.Choropleth(
            geo_data=geojson_candidat[nom],
            data=df,
            bins=6,
            columns=['id', nom],
            key_on="feature.id",
            fill_color=palette_couleur[index_palette],
            fill_opacity=1,
            line_opacity=0.7,
            name=nom,
            overlay=False,
            legend_name='Pourcentage de vote pour ' + nom).add_to(m)
        index_palette += 1

        folium.features.GeoJson(
            data=geojson_candidat[nom],
            style_function=lambda feature: {
                "fillColor": '#00000000',
                "color": '#00000000',
                "weight": 1,
            },
            tooltip=folium.features.GeoJsonTooltip(
                fields=["nom", "pourcentage", "voix"],
                aliases=["Commune : ", "Résultat (%) : ", "Nombre de voix : "],
                sticky=False,
                localize=True,
                labels=True,
            ),
            overlay=False,
            name="Résultats communes",
        ).add_to(choropleth[nom].geojson)

    # Ne pas oublier de faire apparaître le titre et la légende
    nom_departement, nom_circonscription, prenom_nom_elu, nuance_elu, sexe_elu = actions_db.elu_circonscription(departement, circonscription)
    suffixe = '.'
    if sexe_elu == 'F':
        suffixe = 'e.'
    titre = '{}, {} : {} ({}) élu{}'.format(nom_departement, nom_circonscription, prenom_nom_elu, nuance_elu, suffixe)
    titre_html = '''
                 <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                 '''.format(titre)
    m.get_root().html.add_child(folium.Element(titre_html))
    folium.LayerControl(collapsed=False).add_to(m)

    # sauver la carte
    m.save(resultat)


if __name__ == '__main__':
    departement = '59'
    circonscription = '12'
    fichier_geojson = 'geojsons/communes-59-nord.geojson'
    resultat = "resultats/circo_059_012.html"
    cree_carte_circonscription(departement, circonscription, fichier_geojson, resultat)
