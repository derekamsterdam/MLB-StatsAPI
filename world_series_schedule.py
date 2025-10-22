#!/usr/bin/env python
# encoding=utf-8
"""
Script to fetch and display upcoming World Series games between the Blue Jays and Dodgers.
"""

import statsapi
from datetime import datetime, timedelta

# Team IDs
BLUE_JAYS_ID = 141  # Toronto Blue Jays
DODGERS_ID = 119    # Los Angeles Dodgers

def get_world_series_games():
    """
    Fetch upcoming World Series games between the Blue Jays and Dodgers.
    Returns a list of game dictionaries with date, time, and venue information.
    """
    # Get current date and look ahead for the next 30 days to find World Series games
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')

    # Try to find games between these two teams
    # World Series game type is 'W'
    games = []

    # Try multiple approaches to fetch the schedule
    try:
        # Approach 1: Try with just one team (API might not support opponent param)
        jays_schedule = statsapi.schedule(
            start_date=start_date,
            end_date=end_date,
            team=BLUE_JAYS_ID
        )

        # Filter for games against Dodgers with game type 'W' (World Series)
        for game in jays_schedule:
            # Check if it's a World Series game against the Dodgers
            if (game.get('game_type') == 'W' and
                (game.get('home_id') == DODGERS_ID or game.get('away_id') == DODGERS_ID)):
                games.append(game)
    except Exception as e:
        print(f"Erreur lors de la récupération du calendrier des Blue Jays: {e}")

    # If no games found for Blue Jays, try Dodgers
    if not games:
        try:
            dodgers_schedule = statsapi.schedule(
                start_date=start_date,
                end_date=end_date,
                team=DODGERS_ID
            )

            for game in dodgers_schedule:
                if (game.get('game_type') == 'W' and
                    (game.get('home_id') == BLUE_JAYS_ID or game.get('away_id') == BLUE_JAYS_ID)):
                    games.append(game)
        except Exception as e:
            print(f"Erreur lors de la récupération du calendrier des Dodgers: {e}")

    return games

def get_example_games():
    """
    Generate example World Series games for demonstration purposes.
    This is used when no actual games are found in the API.
    """
    base_date = datetime(2025, 10, 25, 20, 0)  # Start date for World Series games

    example_games = []
    venues = [
        "Dodger Stadium, Los Angeles, CA",
        "Dodger Stadium, Los Angeles, CA",
        "Rogers Centre, Toronto, ON",
        "Rogers Centre, Toronto, ON",
        "Rogers Centre, Toronto, ON",
        "Dodger Stadium, Los Angeles, CA",
        "Dodger Stadium, Los Angeles, CA"
    ]

    for i in range(4):  # Show 4 example games
        game_date = base_date + timedelta(days=i*2)
        is_home_game_dodgers = i < 2  # First 2 games at Dodgers, next at Blue Jays

        game = {
            'game_datetime': game_date.isoformat() + 'Z',
            'game_date': game_date.strftime('%Y-%m-%d'),
            'game_type': 'W',
            'status': 'Prévu',
            'venue_name': venues[i],
            'home_name': 'Los Angeles Dodgers' if is_home_game_dodgers else 'Toronto Blue Jays',
            'away_name': 'Toronto Blue Jays' if is_home_game_dodgers else 'Los Angeles Dodgers',
            'home_id': DODGERS_ID if is_home_game_dodgers else BLUE_JAYS_ID,
            'away_id': BLUE_JAYS_ID if is_home_game_dodgers else DODGERS_ID
        }
        example_games.append(game)

    return example_games

def format_game_info(game):
    """
    Format game information for display.
    """
    game_datetime = datetime.fromisoformat(game['game_datetime'].replace('Z', '+00:00'))

    # Convert to local time (adjust timezone as needed)
    date_str = game_datetime.strftime('%A, %B %d, %Y')
    time_str = game_datetime.strftime('%I:%M %p %Z')

    return {
        'date': date_str,
        'time': time_str,
        'venue': game.get('venue_name', 'TBD'),
        'home_team': game.get('home_name', ''),
        'away_team': game.get('away_name', ''),
        'status': game.get('status', 'Scheduled')
    }

def generate_html(games, use_example_data=False):
    """
    Generate an HTML page with the World Series schedule.
    """
    example_note = '''
        <div style="background: #fff3cd; border: 2px solid #ffc107; border-radius: 10px; padding: 20px; margin-bottom: 20px; text-align: center;">
            <strong>Note:</strong> Ceci est une démonstration avec des données d'exemple.
            Aucun match réel n'a été trouvé dans l'API MLB.
        </div>
''' if use_example_data else ''

    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Série Mondiale - Blue Jays vs Dodgers</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .teams {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 3px solid #e9ecef;
        }

        .team {
            text-align: center;
            padding: 20px;
        }

        .team-name {
            font-size: 1.5em;
            font-weight: bold;
            color: #2a5298;
            margin-top: 10px;
        }

        .vs {
            font-size: 2em;
            font-weight: bold;
            color: #764ba2;
            margin: 0 30px;
        }

        .games-list {
            padding: 30px;
        }

        .game-card {
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .game-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        }

        .game-info {
            display: grid;
            gap: 15px;
        }

        .info-row {
            display: flex;
            align-items: center;
            font-size: 1.1em;
        }

        .info-label {
            font-weight: bold;
            color: #2a5298;
            min-width: 100px;
        }

        .info-value {
            color: #333;
        }

        .no-games {
            text-align: center;
            padding: 60px 30px;
            color: #666;
        }

        .no-games h2 {
            font-size: 2em;
            margin-bottom: 20px;
            color: #764ba2;
        }

        .footer {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 Série Mondiale</h1>
            <p>Matchs à venir</p>
        </div>

        <div class="teams">
            <div class="team">
                <div class="team-name">Toronto Blue Jays</div>
            </div>
            <div class="vs">VS</div>
            <div class="team">
                <div class="team-name">Los Angeles Dodgers</div>
            </div>
        </div>

        <div class="games-list">
''' + example_note + '''
'''

    if games:
        for idx, game in enumerate(games, 1):
            game_info = format_game_info(game)
            html += f'''
            <div class="game-card">
                <h3 style="color: #764ba2; margin-bottom: 15px;">Match {idx}</h3>
                <div class="game-info">
                    <div class="info-row">
                        <span class="info-label">📅 Date:</span>
                        <span class="info-value">{game_info['date']}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">🕐 Heure:</span>
                        <span class="info-value">{game_info['time']}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">📍 Endroit:</span>
                        <span class="info-value">{game_info['venue']}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">⚾ Équipes:</span>
                        <span class="info-value">
                            <a href="team_{game['away_id']}_roster.html" style="color: #667eea; text-decoration: none; font-weight: bold;">{game_info['away_team']}</a>
                            @
                            <a href="team_{game['home_id']}_roster.html" style="color: #667eea; text-decoration: none; font-weight: bold;">{game_info['home_team']}</a>
                        </span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">📊 Statut:</span>
                        <span class="info-value">{game_info['status']}</span>
                    </div>
                </div>
            </div>
'''
    else:
        html += '''
            <div class="no-games">
                <h2>Aucun match prévu</h2>
                <p>Il n'y a actuellement aucun match de Série Mondiale prévu entre les Blue Jays et les Dodgers.</p>
                <p style="margin-top: 20px;">Veuillez vérifier ultérieurement pour les mises à jour du calendrier.</p>
            </div>
'''

    html += '''
        </div>

        <div class="footer">
            <p>Données fournies par MLB Stats API</p>
            <p>Dernière mise à jour: ''' + datetime.now().strftime('%d/%m/%Y à %H:%M') + '''</p>
        </div>
    </div>
</body>
</html>
'''

    return html

def main():
    """
    Main function to generate the World Series schedule page.
    """
    print("Récupération des matchs de la Série Mondiale...")
    games = get_world_series_games()

    use_example_data = False
    if not games:
        print("Aucun match trouvé dans l'API.")
        print("Utilisation de données d'exemple pour la démonstration...")
        games = get_example_games()
        use_example_data = True

    print(f"Affichage de {len(games)} match(s)")

    html_content = generate_html(games, use_example_data)

    output_file = 'world_series_schedule.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"[OK] Page générée: {output_file}")
    print(f"Ouvrez le fichier dans votre navigateur pour voir le calendrier.")

    if games:
        print("\nAperçu des matchs:")
        for idx, game in enumerate(games, 1):
            game_info = format_game_info(game)
            print(f"\nMatch {idx}:")
            print(f"  Date: {game_info['date']}")
            print(f"  Heure: {game_info['time']}")
            print(f"  Endroit: {game_info['venue']}")
            print(f"  {game_info['away_team']} @ {game_info['home_team']}")

if __name__ == "__main__":
    main()
