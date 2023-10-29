# visu-legislatives-2022 : expérimentation de Folium pour représenter la répartition géographique des législatives françaises de 2022
# Lit la base de données des résultats et extrait les résultats d'une circonscription

import actions_chaine
import sqlite3
from sqlite3 import Error


def extraire_circonscription(departement, circonscription, db_file_name='legislatives_2022_tour2.sqlite'):
    conn = None
    communes = []
    try:
        # On commence par se connecter à la BD pour récupérer les données de la circonscription
        conn = sqlite3.connect(db_file_name)
        sql_commune = "SELECT * FROM communes where code_departement='{}' and code_circonscription='{}'".format(
            departement, circonscription)
        curseur = conn.cursor()
        curseur.execute(sql_commune)
        db_communes = curseur.fetchall()

        for db_commune in db_communes:
            commune = list(db_commune)
            # On ajoute le nom simplifié
            commune.append(actions_chaine.nom_simplifie(commune[6]))
            # On recherche maintenant les candidats du second tour et on les ajoutes aux données de la commune ...
            sql_candidat = "SELECT * FROM candidats where id_commune='{}'".format(db_commune[0])
            curseur = conn.cursor()
            curseur.execute(sql_candidat)
            candidats = curseur.fetchall()
            liste_candidats = []
            nb_candidats = len(candidats)
            for candidat in candidats:
                liste_candidats.append(candidat)
            # ... le nombre de candidats
            commune.append(nb_candidats)
            # ... et les informations de candidats
            commune.append(liste_candidats)
            communes.append(commune)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return communes


def obtenir_circonscriptions(departement, db_file_name='legislatives_2022_tour2.sqlite'):
    conn = None
    circonscriptions = []
    try:
        # On commence par se connecter à la BD pour récupérer les données de la circonscription
        conn = sqlite3.connect(db_file_name)
        sql_circonscription = "SELECT DISTINCT code_circonscription FROM communes where code_departement='{}' order by code_circonscription".format(departement)
        curseur = conn.cursor()
        curseur.execute(sql_circonscription)
        db_circonscriptions = curseur.fetchall()
        for db_circonscription in db_circonscriptions:
            circonscriptions.append(db_circonscription[0])
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return circonscriptions


def elu_circonscription(departement, circonscription, db_file_name='legislatives_2022_tour2.sqlite'):
    conn = None
    nom_departement = ''
    nom_circonscription = ''
    prenom_nom_elu = ''
    sexe_elu = ''
    nuance_elu = ''
    try:
        # On commence par se connecter à la BD pour récupérer les données de la circonscription
        conn = sqlite3.connect(db_file_name)
        sql_elu = "SELECT nom_departement, nom_circonscription, prenom, nom, nuance, sexe FROM elus " \
                      "where code_departement='{}' and code_circonscription='{}' and elu=1".format(
                        departement, circonscription)
        curseur = conn.cursor()
        curseur.execute(sql_elu)
        db_elu = curseur.fetchone()
        nom_departement = db_elu[0]
        nom_circonscription = db_elu[1]
        prenom_nom_elu = db_elu[2] + ' ' + db_elu[3]
        nuance_elu = db_elu[4]
        sexe_elu = db_elu[5]
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return nom_departement, nom_circonscription, prenom_nom_elu, nuance_elu, sexe_elu


if __name__ == '__main__':
    departement = '59'
    circonscription = '03'
    db_file_name = 'legislatives_2022_tour2.sqlite'
    communes_circo = extraire_circonscription(departement, circonscription, db_file_name)
    print('======== Commune de la circonscription ' + circonscription + ' du département ' + departement)
    for commune in communes_circo:
        print(commune)
