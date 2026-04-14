from models.reader import Reader
from models.plannerAI import PlannerLLM
from models.validator_normaliser import ValidatorAndNormaliser
from models.implementor import PDFMaker
from models.authetication import Authenticator
import json


class PlannerApplicationService:
    def __init__(self, config):
        self.config = config
        self.planner = None

    def __get_sheet(self):
        local_reader = Reader(self.config['CREDENTIALS_FILE'], self.config['SCOPES'])
        local_reader.connect_to_sheet(self.config['WORKBOOK_ID'], self.config['SHEET_NAME'])
        return local_reader

    @staticmethod
    def __load_prompt(file):
        print(f"LOADING PROMPT: {file}")
        with open(file) as f:
            return f.read()

    @staticmethod
    def validate(data):
        validator = ValidatorAndNormaliser(data)
        return validator.validate_normalise()

    def make_pdf(self, data):
        structured_data = ""
        for partial_response in self.planner.structure_data(data):
            structured_data = partial_response
        structured_data = json.loads(structured_data)
        print(structured_data)
        pdf_maker = PDFMaker()
        return pdf_maker.generate_pdf_content(structured_data)

    def fetch_unplanned_rows(self):
        local_reader = self.__get_sheet()
        row_results = local_reader.get_unplanned_rows()
        return row_results

    def get_planner(self):
        generate_prompt = self.__load_prompt(self.config['GENERATE_PROMPT_FILE'])
        refine_prompt = self.__load_prompt(self.config['REFINE_PROMPT_FILE'])
        structure_prompt = self.__load_prompt(self.config['STRUCTURE_PROMPT_FILE'])
        self.planner = PlannerLLM(generate_prompt, refine_prompt, structure_prompt, self.config['OLLAMA_API_KEY'])
        # return PlannerLLM(generate_prompt, refine_prompt, structure_prompt, self.config['OLLAMA_API_KEY'])
        return self.planner

    def mark_row_complete(self, row):
        local_reader = self.__get_sheet()
        local_reader.target_sheet.update_cell(row, local_reader.get_planned_column_index(), "TRUE")

    def is_login_valid(self, user, passw):
        auth = Authenticator(self.config['LOGIN_USERS_FILE'])
        return auth.check_login(user, passw)
