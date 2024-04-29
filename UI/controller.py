import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.clean()
        umidita_torino = self._model.get_umidita_mese_torino(self._view.dd_mese.value)
        umidita_milano = self._model.get_umidita_mese_milano(self._view.dd_mese.value)
        umidita_genova = self._model.get_umidita_mese_genova(self._view.dd_mese.value)
        self._view.lst_result.controls.append(ft.Text("L'umidita' media nel mese selzionato e':"))
        self._view.lst_result.controls.append(ft.Text(f"Torino: {umidita_torino}"))
        self._view.lst_result.controls.append(ft.Text(f"Milano: {umidita_milano}"))
        self._view.lst_result.controls.append(ft.Text(f"Genova: {umidita_genova}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        itinerario, costo_sequenza = self._model.trova_percorso(self._view.dd_mese.value)
        # costo_sequenza = self._model.get_costo(itinerario, self._view.dd_mese.value)  ## DA USARE SOLO SE NON PRENDE IL VALORE DELLLA TUPLA
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha un costo di {costo_sequenza} ed e': "))
        for tappa in itinerario:
            self._view.lst_result.controls.append(ft.Text(tappa))  # CONTROLLA CHE CHIAMI L __str___()
            # mi sa che nella list view poi anche solo chiamare l __str__() invece che il f"[{tappa.localita} - {
            # tappa.data}] Umidita': {tappa.umidita}"
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)
