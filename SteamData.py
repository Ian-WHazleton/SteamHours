import openpyxl
import logging

logging.basicConfig(level=logging.INFO)

def get_data_from_spreadsheet(spreadsheet_path=r'D:\SteamHours\steam_games_playtime.xlsx'):
    """Get total games and total hours from the spreadsheet."""
    try:
        workbook = openpyxl.load_workbook(spreadsheet_path)
        if 'Hours' in workbook.sheetnames:
            sheet = workbook['Hours']
            total_games = 0
            total_hours = 0.0

            # Iterate over the rows to count the games and sum the playtime (column C)
            for row in sheet.iter_rows(min_row=2, values_only=True):
                playtime = row[2]  # Column C: Hours

                if playtime is not None:
                    try:
                        playtime = float(playtime)
                        total_games += 1
                        total_hours += playtime
                    except ValueError:
                        logging.warning(f"Invalid playtime value: {playtime}")
                        continue

            if total_games == 0:
                logging.info("No games found in the spreadsheet.")
                return 0, 0.0, 0.0

            average_playtime = round(total_hours / total_games, 2)
            return total_games, round(total_hours, 2), average_playtime
        else:
            logging.error("Sheet 'Hours' does not exist.")
            return 0, 0.0, 0.0
    except FileNotFoundError:
        logging.error(f"Spreadsheet not found at path: {spreadsheet_path}")
        return 0, 0.0, 0.0
    except openpyxl.utils.exceptions.InvalidFileException:
        logging.error(f"Invalid spreadsheet file: {spreadsheet_path}")
        return 0, 0.0, 0.0
    except Exception as e:
        logging.error(f"Unexpected error reading spreadsheet: {e}")
        return 0, 0.0, 0.0