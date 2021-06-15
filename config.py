import configparser


score_config = "Score"
documents_config = "Documents"


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

    def get_system_score(self):
        return self.config[score_config]["system_score"]

    def get_table_values_ratio(self):
        return self.config[score_config]["table_values_ratio"]

    def get_charts_ratio(self):
        return self.config[score_config]["charts_ratio"]

    def get_sheet_link_by_id(self, id):
        return self.config[documents_config][f"doc{id}"]
