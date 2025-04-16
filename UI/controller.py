import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        if self._view._ddNerc.value is None:
            self._view.create_alert("Selezionare un Nerc!")
            return
        if self._view._txtYears.value is None:
            self._view.create_alert("Selezionare gli anni!")
            return
        if self._view._txtHours.value is None:
            self._view.create_alert("Selezionare le ore!")
            return

        nerc_string=self._view._ddNerc.value
        nerc = self._idMap[nerc_string]

        maxY= int(self._view._txtYears.value)
        maxH= int(self._view._txtHours.value)

        listaSol, utentiSol = self._model.worstCase(nerc, maxY, maxH)
       # self._solBest, self._solBest

        self._view.txtOut.controls.append(ft.Text(f"hai schiacciato. Il numero di utenti è {utentiSol}"))
        for e in listaSol:
            self._view.txtOut.controls.append(ft.Text(f"evento:{e}"))
        self._view.update_page()


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(text=n.value, data=n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
