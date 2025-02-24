from tallyoverlayclient.models import AppDataModel


class OverlayWindowViewModel:
    def __init__(self, model: AppDataModel) -> None:
        self.tally_state = model.tally_state
