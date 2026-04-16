# CURRENT IMPLEMENTATION: Google Sheets via gspread
# FUTURE MIGRATION: Replace this entire layer with SQL repository pattern (PostgreSQL recommended)
# Do NOT build business logic on top of this abstraction — only raw data access

# TODO (Phase 1 Scaling): Replace with SQL query:
# get_unplanned_rows() → SELECT * FROM plans WHERE status = 'unplanned'


import gspread
from google.oauth2.service_account import Credentials


class Reader:
    def __init__(self, cred_info: str, scopes:list=None) -> None:
        self.scopes = scopes or ["https://www.googleapis.com/auth/spreadsheets"]
        self.creds = Credentials.from_service_account_info(
            cred_info, scopes=self.scopes
        )
        self.target_sheet = None
        self.planned_col_index = None

    def connect_to_sheet(self, sheet_id: str, sheet_name: str) -> None:
        client = gspread.authorize(self.creds)
        workbook = client.open_by_key(sheet_id)
        self.target_sheet = workbook.worksheet(sheet_name)

    def get_planned_column_index(self) -> int:
        if self.target_sheet:
            headers = self.target_sheet.row_values(1)
            return headers.index("Planned") + 1

        else:
            raise Exception("self.target_sheet is not defined yet. Run the self.read_sheet method before processing.")

    def get_unplanned_rows(self) -> tuple[int, list[dict[str, int]]]:
        if self.target_sheet:
            rows = self.target_sheet.get_all_records()
            self.planned_col_index = self.get_planned_column_index()

            return self.__check_rows(rows)

        else:
            raise Exception("self.target_sheet is not defined yet. Run the self.read_sheet method before processing.")

    @staticmethod
    def __check_rows(rows: list[dict]) -> tuple[int, list[dict[str, int]]]:
        local_processed_rows = []
        local_number_of_rows = 0

        for idx, row in enumerate(rows, start=2):
            planned_value = str(row.get("Planned", "")).upper()

            if planned_value != "TRUE":
                local_number_of_rows += 1
                local_processed_rows.append({
                    "row_index": idx,
                    "data": row
                })

        return local_number_of_rows, local_processed_rows
