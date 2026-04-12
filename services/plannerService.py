from models.reader import Reader
from models.plannerAI import PlannerLLM
from models.validator_normaliser import ValidatorAndNormaliser


class PlannerApplicationService:
    def __init__(self, config):
        self.config = config

    def __get_sheet(self):
        local_reader = Reader(self.config['CREDENTIALS_FILE'], self.config['SCOPES'])
        local_reader.connect_to_sheet(self.config['WORKBOOK_ID'], self.config['SHEET_NAME'])
        return local_reader

    @staticmethod
    def __load_prompt(file):
        with open(file) as f:
            return f.read()

    def fetch_unplanned_rows(self):
        local_reader = self.__get_sheet()
        row_results = local_reader.get_unplanned_rows()
        return row_results

    @staticmethod
    def validate(data):
        validator = ValidatorAndNormaliser(data)
        return validator.validate_normalise()

    def get_planner(self):
        generate_prompt = self.__load_prompt(self.config['GENERATE_PROMPT_FILE'])
        refine_prompt = self.__load_prompt(self.config['REFINE_PROMPT_FILE'])
        return PlannerLLM(generate_prompt, refine_prompt, self.config['OLLAMA_API_KEY'])

    def mark_row_complete(self, row):
        local_reader = self.__get_sheet()
        local_reader.target_sheet.update_cell(row, local_reader.get_planned_column_index(), "TRUE")
