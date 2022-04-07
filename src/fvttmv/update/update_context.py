class UpdateContext:
    """
    Used when updating data.
    Helps keeping track of whether the data was updated or not.
    """

    data: str
    data_was_updated: bool = False

    def __init__(self,
                 data: str):
        self.data = data

    def override_data(self,
                      new_data: str) -> None:
        self.data = new_data
        self.data_was_updated = True
