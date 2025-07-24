# Steam Hours Tracker

A Python application to fetch and track Steam game playtime using the Steam Web API.

## Setup

### Prerequisites
- Python 3.7+
- Steam Web API Key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Ian-WHazleton/SteamHours.git
cd SteamHours
```

2. Install required packages:
```bash
pip install requests pandas openpyxl python-dotenv
```

3. Get a Steam Web API Key:
   - Go to https://steamcommunity.com/dev/apikey
   - Enter your domain name (can be localhost for personal use)
   - Copy your API key

4. Create a `.env` file in the project root:
```
STEAM_API_KEY=your_api_key_here
```

5. Update the `STEAM_ID` in `SteamAPI_Caller.py` with your Steam ID

### Usage

Run the main script:
```bash
python SteamAPI_Caller.py
```

This will fetch your Steam games and playtime, then save the data to `steam_games_playtime.xlsx`.

## Security Note

Never commit your `.env` file or expose your Steam API key in your code. The `.gitignore` file is configured to exclude sensitive files.
