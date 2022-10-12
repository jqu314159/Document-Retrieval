import logging
import pandas as pd

"""
print(df['I1'])
print(df['TID'])
print(df['TID'][1])
print("0000",df.keys())
"""

class dataset_process:
    def __init__(
        self,
    ):
        self.dateset = {}

    def _get_config(self, args):
        assert isinstance(args, (tuple, list))
        config = self.config
        for arg in args:
            try:
                config = config[arg]
            except ValueError:
                logging.error("Missing configuration '{arg}'!")
        return config
    
    def scan_dataset(self, df):
        for doc_id_maber in df.keys():
            count_word = 0
            for team_ in df[doc_id_maber]:
                count_word += 1
                if team_ not in self.dateset:
                    self.dateset[team_] = {doc_id_maber: {}}
                    self.dateset[team_] = {'team_frequency': 1}
                    self.dateset[team_][doc_id_maber] = {'pos': [count_word], 'doc_frequency': 1}
                else:
                    self.dateset[team_]['team_frequency'] += 1
                    if doc_id_maber not in self.dateset[team_]:
                        self.dateset[team_][doc_id_maber] = {'pos': [count_word], 'doc_frequency': 1}
                    else:
                        self.dateset[team_][doc_id_maber]['doc_frequency'] += 1
                        self.dateset[team_][doc_id_maber]['pos'].append(count_word) 

test = dataset_process()
df = pd.read_csv ('2.csv')
test.scan_dataset(df)
print(test.dateset)