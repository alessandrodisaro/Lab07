from unittest import result

from flet_core import row

from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao:

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_umidita_giorno(mese, giorno, citta):
        cnx = DBConnect.get_connection()
        if cnx is None:
            return f"Errore di connessione"
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT Umidita 
                    FROM situazione 
                    WHERE month(Data) = %s and day(Data) = %s and Localita = %s"""
            cursor.execute(query, (mese, giorno, citta))
            result_temp = cursor.fetchone()   #####
            result = result_temp.get("Umidita")
            cursor.close()
            cnx.close()
            return result
    @staticmethod
    def get_situazione_giorno(mese, giorno, citta):
        cnx = DBConnect.get_connection()
        if cnx is None:
            return f"Errore di connessione"
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT Umidita 
                    FROM situazione 
                    WHERE month(Data) = %s and day(Data) = %s and Localita = %s"""
            cursor.execute(query, (mese, giorno, citta))
            result = []
            for row in cursor:
                result.append(Situazione(row["Localita"], row["Data"], row["Umidita"]))
            cursor.close()
            cnx.close()
            return result

    def get_oggetto_giorno(self, mese, giorno, citta):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT Localita, Data, Umidita
                    FROM situazione
                    WHERE month(Data) = %s and day(Data) = %s and Localita = %s"""
        cursor.execute(query, (mese, giorno, citta))
        result = []
        for row in cursor:
            result.append(Situazione(row["Localita"], row["Data"], row["Umidita"]))
        object_result = result[0]
        cursor.close()
        cnx.close()
        return object_result


