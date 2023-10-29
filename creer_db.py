# visu-legislatives-2022 : expérimentation de Folium pour représenter la répartition géographique des législatives françaises de 2022
# Lit le fichier des résultats et crée une base de données pour utiliser plus facilement les données

import sqlite3
from sqlite3 import Error

def creer_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def inserer_en_table(conn, sql, ligne_db):
    cur = conn.cursor()
    cur.execute(sql, ligne_db)
    conn.commit()
    return cur.lastrowid


def importe_donnes_en_base(file_name, db_file_name):
    # Lit le fichier des résultats, ligne par ligne et les insère dans une BD créée à cet effet
    conn = None
    try:
        # On commence par créer la BD
        conn = sqlite3.connect(db_file_name)
        print(sqlite3.version)

        # entête du CSV, découpé par zones (fixe = 1 seule zone, multiple = 1 par candidat)
        # Fixe : Zone département /circonscription / commune
        #  Code du département;Libellé du département;Code de la circonscription;Libellé de la circonscription;Code de la commune;Libellé de la commune;
        # Fixe : Informations générales sur le vote
        # Etat saisie;Inscrits;Abstentions;% Abs/Ins;Votants;% Vot/Ins;Blancs;% Blancs/Ins;% Blancs/Vot;Nuls;% Nuls/Ins;% Nuls/Vot;Exprim�s;% Exp/Ins;% Exp/Vot;
        sql_creer_table_communes = """ CREATE TABLE IF NOT EXISTS communes (
                                            ID text PRIMARY KEY,
                                            code_departement text,
                                            nom_departement text,
                                            code_circonscription text,
                                            nom_circonscription text,
                                            code_commune text,
                                            nom_commune text,
                                            etat_saisie text,
                                            inscrits integer,
                                            abstentions integer,
                                            pourcent_abs_sur_ins real,
                                            votants integer,
                                            pourcent_vot_sur_ins real,
                                            blancs integer,
                                            pourcent_bla_sur_ins real,
                                            pourcent_bla_sur_vot real,
                                            nuls integer,
                                            pourcent_nul_sur_ins real,
                                            pourcent_nul_sur_vot real,
                                            exprimes integer,
                                            pourcent_exp_sur_ins real,
                                            pourcent_exp_sur_vot real
                                        ); """
        # Multiple : information candidat
        # N�Panneau;Sexe;Nom;Pr�nom;Nuance;Voix;% Voix/Ins;% Voix/Exp
        sql_creer_table_candidats = """ CREATE TABLE IF NOT EXISTS candidats (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            id_commune text,
                                            numero_panneau integer,
                                            sexe text,
                                            nom text NOT NULL,
                                            prenom text,
                                            nuance text,
                                            voix integer,
                                            pourcent_voi_sur_ins real,
                                            pourcent_voi_sur_exp real
                                        ); """
        creer_table(conn, sql_creer_table_communes)
        creer_table(conn, sql_creer_table_candidats)

        sql_inserer_commune = ''' INSERT INTO communes(ID,code_departement,nom_departement,code_circonscription,nom_circonscription,code_commune,nom_commune,etat_saisie,inscrits,abstentions,pourcent_abs_sur_ins,votants,pourcent_vot_sur_ins,blancs,pourcent_bla_sur_ins,pourcent_bla_sur_vot,nuls,pourcent_nul_sur_ins,pourcent_nul_sur_vot,exprimes,pourcent_exp_sur_ins,pourcent_exp_sur_vot)
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        sql_inserer_candidat = ''' INSERT INTO candidats(id_commune,numero_panneau,sexe,nom,prenom,nuance,voix,pourcent_voi_sur_ins,pourcent_voi_sur_exp)
                                    VALUES(?,?,?,?,?,?,?,?,?) '''

        with open(file_name, newline='') as fp:
            print('== Header ===========================================')
            ligne = fp.readline()
            print(ligne)
            print('=====================================================')
            ligne = fp.readline()
            while ligne:
                # entête du CSV, découpé par zones (fixe = 1 seule zone, multiple = 1 par candidat)
                # Fixe : Zone département /circonscription / commune
                #  Code du d�partement;Libell� du d�partement;Code de la circonscription;Libell� de la circonscription;Code de la commune;Libell� de la commune;
                # Fixe : Informations générales sur le vote
                # Etat saisie;Inscrits;Abstentions;% Abs/Ins;Votants;% Vot/Ins;Blancs;% Blancs/Ins;% Blancs/Vot;Nuls;% Nuls/Ins;% Nuls/Vot;Exprim�s;% Exp/Ins;% Exp/Vot;
                # Multiple : information candidat
                # N�Panneau;Sexe;Nom;Pr�nom;Nuance;Voix;% Voix/Ins;% Voix/Exp
                champs = ligne.split(';')
                # Préparation des champs de la ligne à insérer dans la table commune
                code_departement = champs[0]  # text
                nom_departement = champs[1]  # text
                code_circonscription = champs[2]  # text
                nom_circonscription = champs[3]  # text
                code_commune = champs[4]  # text
                nom_commune = champs[5]  # text
                id_commune = code_departement + '_' + code_circonscription + '_' + code_commune
                etat_saisie = champs[6]  # text
                inscrits = int(champs[7])  # integer
                abstentions = int(champs[8])  # integer
                pourcent_abs_sur_ins = float(champs[9].replace(',', '.'))  # real
                votants = int(champs[10])  # integer
                pourcent_vot_sur_ins = float(champs[11].replace(',', '.'))  # real
                blancs = int(champs[12])  # integer
                pourcent_bla_sur_ins = float(champs[13].replace(',', '.'))  # real
                pourcent_bla_sur_vot = float(champs[14].replace(',', '.'))  # real
                nuls = int(champs[15])  # integer
                pourcent_nul_sur_ins = float(champs[16].replace(',', '.'))  # real
                pourcent_nul_sur_vot = float(champs[17].replace(',', '.'))  # real
                exprimes = int(champs[18])  # integer
                pourcent_exp_sur_ins = float(champs[19].replace(',', '.'))  # real
                pourcent_exp_sur_vot = float(champs[20].replace(',', '.'))  # real

                ligne_db_commune = (
                id_commune, code_departement, nom_departement, code_circonscription, nom_circonscription, code_commune,
                nom_commune, etat_saisie, inscrits, abstentions, pourcent_abs_sur_ins, votants, pourcent_vot_sur_ins,
                blancs, pourcent_bla_sur_ins, pourcent_bla_sur_vot, nuls, pourcent_nul_sur_ins, pourcent_nul_sur_vot,
                exprimes, pourcent_exp_sur_ins, pourcent_exp_sur_vot)
                print(id_commune)
                inserer_en_table(conn, sql_inserer_commune, ligne_db_commune)
                champs_candidats = champs[21:]
                print(champs_candidats)
                nb_candidats = int(len(champs_candidats) / 8)
                for j in range(nb_candidats):
                    id_commune_candidat = id_commune
                    numero_panneau = int(champs_candidats[j * 8 + 0])
                    sexe = champs_candidats[j * 8 + 1]
                    nom = champs_candidats[j * 8 + 2]
                    prenom = champs_candidats[j * 8 + 3]
                    nuance = champs_candidats[j * 8 + 4]
                    voix = int(champs_candidats[j * 8 + 5])
                    pourcent_voi_sur_ins = float(champs_candidats[j * 8 + 6].replace(',', '.'))
                    pourcent_voi_sur_exp = float(champs_candidats[j * 8 + 7].replace(',', '.'))

                    print(id_commune + ' ' + prenom + ' ' + nom)
                    ligne_db_candidat = (
                    id_commune_candidat, numero_panneau, sexe, nom, prenom, nuance, voix, pourcent_voi_sur_ins,
                    pourcent_voi_sur_exp)
                    inserer_en_table(conn, sql_inserer_candidat, ligne_db_candidat)
                ligne = fp.readline()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def determine_candidats_elus(db_file_name):
    conn = None
    try:
        # On commence par créer la BD
        conn = sqlite3.connect(db_file_name)

        sql_creer_table_elus = """ CREATE TABLE IF NOT EXISTS elus (
                                            ID integer PRIMARY KEY,
                                            code_departement text,
                                            nom_departement text,
                                            code_circonscription text,
                                            nom_circonscription text,
                                            numero_panneau integer,
                                            sexe text,
                                            elu integer,
                                            nom text NOT NULL,
                                            prenom text,
                                            nuance text,
                                            exprimes integer,
                                            voix integer
                                        ); """
        creer_table(conn, sql_creer_table_elus)

        # Balayer par département et par circonscription
        sql_departement = "SELECT DISTINCT code_departement, nom_departement FROM communes"
        curseur = conn.cursor()
        curseur.execute(sql_departement)
        db_departements = curseur.fetchall()

        for db_departement in db_departements:
            sql_circonscription = "SELECT DISTINCT code_circonscription, nom_circonscription FROM communes " \
                                  "WHERE code_departement='{}'".format(db_departement[0])
            curseur = conn.cursor()
            curseur.execute(sql_circonscription)
            db_circonscriptions = curseur.fetchall()
            for db_circonscription in db_circonscriptions:
                # On commence par récupérer le nombre de suffrages exprimés par circonscription
                sql_exprimes = "SELECT SUM(exprimes) FROM communes " \
                               "WHERE code_departement = '{}' and code_circonscription = '{}'".format(db_departement[0], db_circonscription[0])
                curseur = conn.cursor()
                curseur.execute(sql_exprimes)
                db_exprime = curseur.fetchone()
                # Enfin on récupère les résultats des candidats en triant selon leur nombre de voix : le premier est élu
                sql_elus = "SELECT sum(voix) total_voix, numero_panneau, sexe, nom, prenom, nuance from candidats c " \
                           "WHERE c.id_commune IN " \
                           "(SELECT id FROM communes WHERE code_departement = '{}' and code_circonscription = '{}') " \
                           "GROUP BY nom ORDER BY total_voix DESC".format(db_departement[0], db_circonscription[0])
                curseur = conn.cursor()
                curseur.execute(sql_elus)
                db_elus = curseur.fetchall()
                elu_en_db = False
                nb_candidats = 0
                for db_elu in db_elus:
                    # Il reste à sauver les résultats, en utilisant le fait que le premier candidat est élu
                    elu = 0
                    nb_candidats += 1
                    if not elu_en_db:
                        elu_en_db = True
                        elu = 1
                    sql_inserer_elu = "INSERT INTO elus(" \
                                      "code_departement,nom_departement, code_circonscription,nom_circonscription," \
                                      "numero_panneau,sexe,elu,nom,prenom,nuance,exprimes,voix) " \
                                      "VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"
                    ligne_db_elu = (
                        db_departement[0], db_departement[1], db_circonscription[0], db_circonscription[1],
                        db_elu[1], db_elu[2], elu, db_elu[3], db_elu[4], db_elu[5], db_exprime[0], db_elu[0])
                    if nb_candidats > 2:
                        print("> 2 candidats dans circo {} du {}".format(db_circonscription[0], db_departement[0]))
                    inserer_en_table(conn, sql_inserer_elu, ligne_db_elu)

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    file_name = 'resultats-par-niveau-subcom-t2-france-entiere.csv'
    db_file_name = 'legislatives_2022_tour2.sqlite'
    #importe_donnes_en_base(file_name, db_file_name)
    #determine_candidats_elus(db_file_name)
