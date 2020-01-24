import os
import pandas as pd
import json

class data:
    def __init__(self, _dir):
        filepaths = self._find_data_files(_dir)
        raw_data = self._load_data(filepaths)
        self.data = pd.DataFrame(raw_data).set_index("id").sort_index()

    def _find_data_files(self, _dir):
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), _dir)
        filepaths = []
        for filename in os.listdir(data_dir):
            path = os.path.join(data_dir, filename)
            if(os.path.isfile(path)):
                filepaths += [path]
        return filepaths

    def _refactor_question(self, question):
        if(not ("answers" in question)):
            return
        output = {
            "id": question["id"],
            "pos": question["question_number"],
            "question": question["text"],
            "answer_0": question["answers"][0]["text"],
            "ind_0": question["answers"][0]["correct"],
            "answer_1": question["answers"][1]["text"],
            "ind_1": question["answers"][1]["correct"],
            "answer_2": question["answers"][2]["text"],
            "ind_2": question["answers"][2]["correct"]
        }
        return output

    def _load_data(self, filepaths):
        data_agg = []
        for path in filepaths:
            with open(path) as json_file:
                data = json.load(json_file)
                if (data):
                    for games in data:
                        if(("questions" in games) and (games["game_type"]=="trivia")):
                            data_agg += [self._refactor_question(question) for question in games["questions"] if(question)]
        return data_agg


