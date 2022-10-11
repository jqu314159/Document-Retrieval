import logging
dataset = dict(
    terms = dict(
        Document_index = dict(
            pos = 0,
            frequency = 0,
        ),
    ),
),
class dataset_process:
    def __init__(
        self,
        dateset
    ):
        self.dateset = dateset

    def _get_config(self, args):
        assert isinstance(args, (tuple, list))
        config = self.config
        for arg in args:
            try:
                config = config[arg]
            except ValueError:
                logging.error("Missing configuration '{arg}'!")
        return config
    
    def scan_dataset(self):
        

