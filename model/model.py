import copy

from database.meteo_dao import MeteoDao



class Model:
    def __init__(self):
        self._dao = MeteoDao()
        self._lista_itinerario = []
        self._costo_minore = 10000000

    def get_umidita_mese_torino(self, mese):
        lista_situazioni = self._dao.get_all_situazioni()
        lista_filtrata_torino = []
        for row in lista_situazioni:
            mese_situazione = row.data.month
            if mese_situazione == int(mese):
                if row.localita == "Torino":
                    lista_filtrata_torino.append(row)

        value_umidita = 0
        cnt = 0
        for row in lista_filtrata_torino:
            value_umidita += row.umidita
            cnt += 1
        if cnt != 0:
            umidita_media = value_umidita / cnt
        else:
            return None
        return umidita_media

    def get_umidita_mese_milano(self, mese):
        lista_situazioni = self._dao.get_all_situazioni()
        lista_filtrata_milano = []
        for row in lista_situazioni:
            mese_situazione = row.data.month
            if mese_situazione == int(mese):
                if row.localita == "Milano":
                    lista_filtrata_milano.append(row)
        value_umidita = 0
        cnt = 0
        for row in lista_filtrata_milano:
            value_umidita += row.umidita
            cnt += 1
        if cnt != 0:
            umidita_media = value_umidita / cnt
        else:
            return None
        return umidita_media

    def get_umidita_mese_genova(self, mese):
        lista_situazioni = self._dao.get_all_situazioni()
        lista_filtrata_genova = []
        for row in lista_situazioni:
            mese_situazione = row.data.month
            if mese_situazione == int(mese):
                if row.localita == "Genova":
                    lista_filtrata_genova.append(row)
        value_umidita = 0
        cnt = 0
        for row in lista_filtrata_genova:
            value_umidita += row.umidita
            cnt += 1
        if cnt != 0:
            umidita_media = value_umidita / cnt
        else:
            return None
        return umidita_media

    def get_umidita_media_giorni(self, inizio, fine, citta, mese):
        lista_situazioni = self._dao.get_all_situazioni()
        lista_filtrata = []
        for row in lista_situazioni:
            mese_situazione = row.data.month
            if mese_situazione == int(mese):
                if row.localita == citta:
                    lista_filtrata.append(row)
        value_umidita = 0
        if inizio >= 1:
            cnt = inizio - 1
        else:
            return ValueError("Il primo giorno non puo' essere negativo")
        while cnt <= (fine - inizio):
            value_umidita += lista_filtrata[cnt].umidita
            cnt += 1
        umidita_media = value_umidita / cnt
        return umidita_media

    def trova_percorso(self, mese):
        # scelgo il punto di partenza
        # prendo l umidita media dei primi 3,4,5 e giorni nelle 3 citta

        i = 1  # inizializzazione per i giorni in input
        lista_citta = ["Torino", "Milano", "Genova"]
        lista_umidita_minori = []

        for citta in lista_citta:
            umidita_3 = self.get_umidita_media_giorni(i, i + 2, citta, int(mese))
            umidita_4 = self.get_umidita_media_giorni(i, i + 3, citta, int(mese))
            umidita_5 = self.get_umidita_media_giorni(i, i + 4, citta, int(mese))
            umidita_6 = self.get_umidita_media_giorni(i, i + 5, citta, int(mese))
            umidita_minore = 0
            # qua prendo i primi tre giorni
            if umidita_4 <= umidita_3:
                umidita_minore = umidita_4
            else:
                umidita_minore = umidita_3
            if umidita_5 <= umidita_minore:
                umidita_minore = umidita_5
            if umidita_6 <= umidita_minore:
                umidita_minore = umidita_6
            lista_umidita_minori.append(umidita_minore)  # so che la 1 e torino la 2 milano e la 3 genova
        # adesso controllo quale citta ha la minore umidita
        partenza = []  # lista con il primo risultato
        if lista_umidita_minori[0] <= lista_umidita_minori[1] and lista_umidita_minori[0] <= lista_umidita_minori[2]:  # Torino
            obj = self._dao.get_oggetto_giorno(mese, 1, "Torino")  # LISTA DI UN OGGETTO SITUAZIONE
            partenza.append(obj)
        elif lista_umidita_minori[1] <= lista_umidita_minori[2] and lista_umidita_minori[1] <= lista_umidita_minori[0]:  # Milano
            obj = self._dao.get_oggetto_giorno(mese, 1, "Milano")
            partenza.append(obj)
        elif lista_umidita_minori[2] <= lista_umidita_minori[0] and lista_umidita_minori[2] <= lista_umidita_minori[1]:  # Genova
            obj = self._dao.get_oggetto_giorno(mese, 1, "Genova")
            partenza.append(obj)

        self._recursion(partenza, 1, mese)
        return (self._lista_itinerario, self._costo_minore)

    def _recursion(self, parziale, giorno, mese):  # il giorno non e da sommare +1
        # terminal condition
        if len(parziale) == 15:
            ### start test
            # for row in parziale:
            #     print(row.localita)
            ### end test
            # calcolo del costo
            ### start test costo
            print(self.get_costo(parziale, mese))
            ### end test costo
            costo = self.get_costo(parziale, mese)
            if costo < self._costo_minore:
                self._costo_minore = costo
                self._lista_itinerario = copy.deepcopy(parziale)
        else:
            # creo un array next day con le tre possibilita
            next_day = []
            next_day.append(self._dao.get_oggetto_giorno(mese, giorno + 1, "Torino"))
            next_day.append(self._dao.get_oggetto_giorno(mese, giorno + 1, "Milano"))
            next_day.append(self._dao.get_oggetto_giorno(mese, giorno + 1, "Genova"))
            # enumerare il prossimo nodo
            for s in next_day:
                parziale.append(s)
                # check dei constraints
                if self._percorso_ammissibile(parziale):
                    self._recursion(parziale, giorno + 1, mese)
                # traceback
                parziale.pop()

    def get_costo(self, percorso, mese):  # CNOTROLLA SE PASSI UNA CITTA O SOLO LA LISTA
        costo_totale = self.get_umidita_media_giorni(1, 1, percorso[0].localita, mese)
        giorni_ancora_maggiorati = 0

        # calcola il costo del percorso
        # calcolo dal primo giorno in poi
        for i in range(1, len(percorso)):  # CONTROLLA LA LUNGHEZZA DELL ARRAY / o nel caso metti 15
            if giorni_ancora_maggiorati >= 1:
                costo_totale += 100 + (self.get_umidita_giorno(mese, i + 1, percorso[i].localita))
                giorni_ancora_maggiorati -= 1
                if percorso[i].localita != percorso[i - 1].localita:  # se intanto csmbio anche localita dop aver raggigunto l utlimo giorno di maggiorazione
                    giorni_ancora_maggiorati = 2
            elif percorso[i].localita == percorso[i - 1].localita and giorni_ancora_maggiorati == 0:
                costo_totale += self.get_umidita_giorno(mese, i + 1, percorso[i].localita)  # forse i+1 nella citta
            elif percorso[i].localita != percorso[i - 1].localita:
                costo_totale += 100 + (self.get_umidita_giorno(mese, i + 1, percorso[i].localita))
                giorni_ancora_maggiorati = 1
        return costo_totale

    def get_umidita_giorno(self, mese, giorno, citta):
        return self._dao.get_umidita_giorno(mese, giorno, citta)

    def _percorso_ammissibile(self, parziale):
        giorni_stesso_posto = 1
        giorni_totali_torino = 0
        giorni_totali_milano = 0
        giorni_totali_genova = 0
        # inizializzazione
        citta_oggi = parziale[0].localita
        if parziale[0].localita == "Torino":
            giorni_totali_torino += 1
        elif parziale[0].localita == "Milano":
            giorni_totali_milano += 1
        elif parziale[0].localita == "Genova":
            giorni_totali_genova += 1
        #per tutti i giorni
        for i in range(1, len(parziale)):
            # check se stiamo piu di 3 giorni nella stessa citta
            if giorni_stesso_posto > 3:
                return False
            # aumento/reset counter
            if parziale[i].localita == citta_oggi:
                giorni_stesso_posto += 1
                citta_oggi = parziale[i].localita
            else:
                giorni_stesso_posto = 1
                citta_oggi = parziale[i].localita
            # aumento counter totale
            if parziale[i].localita == "Torino":
                giorni_totali_torino += 1
            elif parziale[i].localita == "Milano":
                giorni_totali_milano += 1
            elif parziale[i].localita == "Genova":
                giorni_totali_genova += 1
        if giorni_stesso_posto > 3:
            return False
        # check se stiamo piu di 6 giorni totali in un stessa citta
        if giorni_totali_torino > 6 or giorni_totali_milano > 6 or giorni_totali_genova > 6:
            return False

        return True

