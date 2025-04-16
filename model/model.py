import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._utentiBest = -1

        self._listNerc = None
        self._listEvents = None
        self.loadNerc()

    def worstCase(self, nerc, maxY, maxH):
        parziale = []
        self.loadNerc()  #serve?
        self.loadEvents(nerc)
        rimanenti = self._listEvents  #tutti gli eventi in quell'area
        self.ricorsione(parziale, maxY, maxH, 0)
        return self._solBest, self._utentiBest

    def ricorsione(self, parziale, maxY, maxH, pos):
        #massimizzare gli utenti colpiti
        utenti = self.calcolaUtenti(parziale)
        if utenti > self._utentiBest:
            self._utentiBest = utenti
            self._solBest = copy.deepcopy(parziale)
            print(parziale)

        else:  #per ogni guasto
            for guasto in self._listEvents[pos:]:
                parziale.append(guasto)
                if self.vincoli_superati(parziale, maxY, maxH):
                    #nuovi_possibili = self.calcola_possibili(guasto, maxY, maxH, pos+1)  #vicoli (limite ore, sottrazione anni)
                    self.ricorsione(parziale, maxY, maxH, pos + 1)
            #aggiungi guasto
            #backtracking
            parziale.pop()

    def calcolaUtenti(self, parziale):
        tot_Utenti = 0
        for guasto in parziale:
            tot_Utenti += guasto.customers_affected

        return tot_Utenti

    def vincoli_superati(self, parziale, maxY, maxH):
        #vincolo orario

        totDurataTutto = 0
        annoMax = 0
        annoMin = 0

        for g in parziale:
            anno = g.date_event_began.year
            deltas = g.date_event_finished - g.date_event_began
            durata = deltas.total_seconds() / 3600

            totDurataTutto += durata
            if anno > annoMax:
                annoMax = anno
            if anno < annoMin:
                annoMin = anno

        if totDurataTutto > maxH:
            return False
        if annoMax-annoMin > maxY:
            return False
        else:
            return True

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    @property
    def listNerc(self):
        return self._listNerc
