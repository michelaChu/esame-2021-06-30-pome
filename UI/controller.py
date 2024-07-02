import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._model.buildGraph()
        nN, nE = self._model.getGraphDetails()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {nN} nodi, {nE} archi."))
        self.fillDD()
        self._view.update_page()

    def fillDD(self):
        localizzazioni = self._model.getAllNodes()
        for l in localizzazioni:
            self._view.ddLocalizzazione.options.append(ft.dropdown.Option(l))
        self._view.update_page()

    def handle_statistiche(self, e):
        loc = self._view.ddLocalizzazione.value
        if loc is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Selezionare una localizzazione"))
            return

        list = self._model.statistiche(loc)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Adiacenti a: {loc}"))
        for l in list:
            self._view.txt_result.controls.append(ft.Text(f"{l[0]} - {l[1]}"))
        self._view.update_page()

    def handle_search(self, e):
        loc = self._view.ddLocalizzazione.value
        if loc is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Selezionare una localizzazione"))
            return

        path = self._model.getBestPath(loc)
        self._view.txt_result.clean()
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()




