import requests
import pandas as pd
import openpyxl
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Steam API Information
API_KEY = os.getenv('STEAM_API_KEY')  # Use environment variable
if not API_KEY:
    raise ValueError("STEAM_API_KEY environment variable is required")
STEAM_ID = '76561198074846013'

# URL for the Steam API GetOwnedGames method
url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={STEAM_ID}&include_appinfo=true"

# Fetching owned games from Steam API
response = requests.get(url)
if response.status_code == 200:
    games_data = response.json().get('response', {}).get('games', [])
    print(f"Games data retrieved: {len(games_data)} games found.")
else:
    print("Failed to fetch data from Steam API.")
    games_data = []

# List of games with their names and playtime in hours
games_list = []
for game in games_data:
    game_info = {
        "Game Name": game.get('name', 'Unknown'),
        "App ID": game.get('appid', 'Unknown'),
        "Playtime (hours)": round(game.get('playtime_forever', 0) / 60, 2)
    }
    games_list.append(game_info)

# Convert the list to a DataFrame for easy handling
df = pd.DataFrame(games_list)

# Path to the spreadsheet
spreadsheet_path = 'steam_games_playtime.xlsx'

# Write the DataFrame to the spreadsheet
if not df.empty:
    try:
        with pd.ExcelWriter(spreadsheet_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Steam Games Playtime', index=False)
        print(f"Spreadsheet updated at {spreadsheet_path}")
    except Exception as e:
        print(f"Error saving spreadsheet: {e}")
else:
    print("No games to save.")


