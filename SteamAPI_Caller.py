import requests
import pandas as pd
import openpyxl
import os
from dotenv import load_dotenv

def get_api_key():
    """Get the Steam API key using the same method as the game lookup function."""
    load_dotenv()
    return os.getenv('STEAM_API_KEY')

# Steam API Information - will be loaded when needed
STEAM_ID = '76561198074846013'

def fetch_steam_games():
    """Fetch games data from Steam API."""
    API_KEY = get_api_key()
    if not API_KEY:
        print("Steam API key not found. Please check your .env file.")
        return []
    
    # URL for the Steam API GetOwnedGames method
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={STEAM_ID}&include_appinfo=true&include_played_free_games=true"

    # Fetching owned games from Steam API
    response = requests.get(url)
    if response.status_code == 200:
        games_data = response.json().get('response', {}).get('games', [])
        print(f"Games data retrieved: {len(games_data)} games found.")
        return games_data
    else:
        print("Failed to fetch data from Steam API.")
        return []

def update_spreadsheet():
    """Update the spreadsheet with latest Steam game data."""
    games_data = fetch_steam_games()
    
    # Process games data
    games_list = []
    
    for game in games_data:
        app_id = game.get('appid', 'Unknown')
        game_name = game.get('name', 'Unknown')
        
        game_info = {
            "Game Name": game_name,
            "App ID": app_id,
            "Hours Played": round(game.get('playtime_forever', 0) / 60, 2),
            "Purchase Cost": "",  # Will be filled by CSV import or manual entry
            "Purchase Date": "",  # Will be filled by CSV import or manual entry
            "Purchase Method": ""  # Will be filled by CSV import or manual entry
        }
        
        games_list.append(game_info)
    
    # Sort games alphabetically by name
    games_list.sort(key=lambda x: x["Game Name"].lower())

    # Convert the list to a DataFrame
    df = pd.DataFrame(games_list)

    # Path to the spreadsheet (updating to match SteamRunner.py expectation)
    spreadsheet_path = r'D:\SteamHours\ExcelFiles\steam_games_playtime.xlsx'

    # Write the DataFrame to the spreadsheet
    if not df.empty:
        try:
            with pd.ExcelWriter(spreadsheet_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Steam Games Playtime', index=False)
            print(f"Spreadsheet updated at {spreadsheet_path}")
            print(f"Total games processed: {len(games_list)}")
            
        except Exception as e:
            print(f"Error saving spreadsheet: {e}")
    else:
        print("No games to save.")

def get_total_games_and_hours(sheet):
    """Calculate total games and hours from an Excel sheet."""
    total_games = 0
    total_hours = 0.0
    
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
        if row[0]:  # If Game Name exists
            total_games += 1
            if row[2]:  # If Hours Played exists
                total_hours += float(row[2])
    
    return total_games, total_hours



def get_steam_price(app_id, country_code='US'):
    """Get the current price of a game from Steam Store API."""
    try:
        # Steam Store API endpoint for price details
        url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&filters=price_overview&cc={country_code}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            if str(app_id) in data and data[str(app_id)]['success']:
                game_data = data[str(app_id)]['data']
                
                # Check if data is a list (empty) or dict with price info
                if isinstance(game_data, dict) and 'price_overview' in game_data:
                    price_overview = game_data['price_overview']
                    
                    if price_overview:
                        # Price is in cents, convert to dollars
                        final_price = price_overview.get('final', 0) / 100.0
                        initial_price = price_overview.get('initial', 0) / 100.0
                        
                        return {
                            'current_price': final_price,
                            'original_price': initial_price,
                            'currency': price_overview.get('currency', 'USD'),
                            'discount_percent': price_overview.get('discount_percent', 0)
                        }
                
                # If no price data available, return free game defaults
                return {
                    'current_price': 0.0,
                    'original_price': 0.0,
                    'currency': 'USD',
                    'discount_percent': 0
                }
            else:
                print(f"Failed to get price data for app ID {app_id}")
                return None
        else:
            print(f"HTTP error {response.status_code} when fetching price for app ID {app_id}")
            return None
            
    except Exception as e:
        print(f"Error fetching price for app ID {app_id}: {e}")
        return None

def get_bundle_prices(app_ids):
    """Get Steam original prices for multiple games (bundle)."""
    prices = {}
    total_steam_value = 0.0
    
    print(f"Fetching Steam original prices for {len(app_ids)} games...")
    
    for app_id in app_ids:
        price_info = get_steam_price(app_id)
        if price_info:
            # Use original price (before any discounts)
            price = price_info['original_price']
            prices[app_id] = price
            total_steam_value += price
            print(f"  App ID {app_id}: ${price:.2f} (original)")
        else:
            # If we can't get the price, assume $0 (free game or unavailable)
            prices[app_id] = 0.0
            print(f"  App ID {app_id}: Price unavailable, assuming $0.00")
    
    print(f"Total Steam value (original prices): ${total_steam_value:.2f}")
    return prices, total_steam_value


# Main execution (when run directly)
if __name__ == "__main__":
    games_data = fetch_steam_games()
    
    # Process games data
    games_list = []
    
    for game in games_data:
        app_id = game.get('appid', 'Unknown')
        game_name = game.get('name', 'Unknown')
        
        game_info = {
            "Game Name": game_name,
            "App ID": app_id,
            "Hours Played": round(game.get('playtime_forever', 0) / 60, 2),
            "Purchase Cost": "",  # Will be filled by CSV import or manual entry
            "Purchase Date": "",  # Will be filled by CSV import or manual entry
            "Purchase Method": ""  # Will be filled by CSV import or manual entry
        }
        
        games_list.append(game_info)
    
    # Sort games alphabetically by name
    games_list.sort(key=lambda x: x["Game Name"].lower())

    # Convert the list to a DataFrame
    df = pd.DataFrame(games_list)

    # Path to the spreadsheet
    spreadsheet_path = 'ExcelFiles/steam_games_playtime.xlsx'

    # Write the DataFrame to the spreadsheet
    if not df.empty:
        try:
            with pd.ExcelWriter(spreadsheet_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Steam Games Playtime', index=False)
            print(f"Spreadsheet updated at {spreadsheet_path}")
            print(f"Total games processed: {len(games_list)}")
            
        except Exception as e:
            print(f"Error saving spreadsheet: {e}")
    else:
        print("No games to save.")
