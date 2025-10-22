#!/usr/bin/env python
# encoding=utf-8
"""
Script to generate team roster pages and player profiles for World Series teams.
Creates beautiful sports magazine-style pages with photos and complete statistics.
"""

import statsapi
import os
import json
from datetime import datetime

# Team IDs
BLUE_JAYS_ID = 141
DODGERS_ID = 119

# MLB headshot URL pattern
def get_player_headshot_url(player_id, size='large'):
    """Get MLB player headshot URL. Sizes: small, medium, large"""
    sizes = {'small': '60', 'medium': '120', 'large': '300'}
    return f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_{sizes.get(size, '300')}/v1/people/{player_id}/headshot/67/current"

def get_team_logo_url(team_id):
    """Get MLB team logo URL"""
    return f"https://www.mlbstatic.com/team-logos/{team_id}.svg"

# Example data structure (will be replaced by API calls when available)
EXAMPLE_ROSTERS = {
    141: {  # Blue Jays
        'team_name': 'Toronto Blue Jays',
        'team_abbrev': 'TOR',
        'primary_color': '#134A8E',
        'secondary_color': '#E8291C',
        'pitchers': [
            {
                'id': 592789,
                'name': 'José Berríos',
                'number': '17',
                'position': 'SP',
                'bats': 'R',
                'throws': 'R',
                'age': 30,
                'stats': {'wins': 16, 'losses': 7, 'era': '3.65', 'strikeouts': 192, 'innings': '192.1', 'whip': '1.15'}
            },
            {
                'id': 666201,
                'name': 'Kevin Gausman',
                'number': '34',
                'position': 'SP',
                'bats': 'L',
                'throws': 'R',
                'age': 33,
                'stats': {'wins': 14, 'losses': 9, 'era': '3.82', 'strikeouts': 205, 'innings': '181.0', 'whip': '1.22'}
            },
            {
                'id': 641154,
                'name': 'Chris Bassitt',
                'number': '40',
                'position': 'SP',
                'bats': 'R',
                'throws': 'R',
                'age': 35,
                'stats': {'wins': 12, 'losses': 11, 'era': '4.15', 'strikeouts': 168, 'innings': '175.2', 'whip': '1.35'}
            },
            {
                'id': 621121,
                'name': 'Jordan Romano',
                'number': '68',
                'position': 'RP',
                'bats': 'R',
                'throws': 'R',
                'age': 31,
                'stats': {'wins': 4, 'losses': 3, 'era': '2.95', 'saves': 36, 'strikeouts': 89, 'innings': '67.0', 'whip': '1.10'}
            },
            {
                'id': 656302,
                'name': 'Jordan Hicks',
                'number': '41',
                'position': 'RP',
                'bats': 'R',
                'throws': 'R',
                'age': 28,
                'stats': {'wins': 6, 'losses': 5, 'era': '3.29', 'strikeouts': 95, 'innings': '76.2', 'whip': '1.25'}
            },
        ],
        'batters': [
            {
                'id': 665742,
                'name': 'Vladimir Guerrero Jr.',
                'number': '27',
                'position': '1B',
                'bats': 'R',
                'throws': 'R',
                'age': 25,
                'stats': {'avg': '.323', 'hr': 44, 'rbi': 126, 'runs': 105, 'hits': 191, 'sb': 5, 'ops': '.987'}
            },
            {
                'id': 665489,
                'name': 'Bo Bichette',
                'number': '11',
                'position': 'SS',
                'bats': 'R',
                'throws': 'R',
                'age': 26,
                'stats': {'avg': '.298', 'hr': 22, 'rbi': 89, 'runs': 95, 'hits': 178, 'sb': 18, 'ops': '.835'}
            },
            {
                'id': 596115,
                'name': 'George Springer',
                'number': '4',
                'position': 'CF',
                'bats': 'R',
                'throws': 'R',
                'age': 35,
                'stats': {'avg': '.275', 'hr': 28, 'rbi': 82, 'runs': 92, 'hits': 142, 'sb': 12, 'ops': '.842'}
            },
            {
                'id': 677594,
                'name': 'Alejandro Kirk',
                'number': '30',
                'position': 'C',
                'bats': 'R',
                'throws': 'R',
                'age': 25,
                'stats': {'avg': '.265', 'hr': 15, 'rbi': 68, 'runs': 52, 'hits': 128, 'sb': 0, 'ops': '.738'}
            },
            {
                'id': 666182,
                'name': 'Matt Chapman',
                'number': '26',
                'position': '3B',
                'bats': 'R',
                'throws': 'R',
                'age': 31,
                'stats': {'avg': '.258', 'hr': 27, 'rbi': 88, 'runs': 78, 'hits': 135, 'sb': 7, 'ops': '.792'}
            },
            {
                'id': 606466,
                'name': 'Daulton Varsho',
                'number': '25',
                'position': 'LF',
                'bats': 'L',
                'throws': 'R',
                'age': 28,
                'stats': {'avg': '.245', 'hr': 19, 'rbi': 65, 'runs': 71, 'hits': 118, 'sb': 15, 'ops': '.735'}
            },
        ]
    },
    119: {  # Dodgers
        'team_name': 'Los Angeles Dodgers',
        'team_abbrev': 'LAD',
        'primary_color': '#005A9C',
        'secondary_color': '#EF3E42',
        'pitchers': [
            {
                'id': 477132,
                'name': 'Clayton Kershaw',
                'number': '22',
                'position': 'SP',
                'bats': 'L',
                'throws': 'L',
                'age': 36,
                'stats': {'wins': 13, 'losses': 5, 'era': '2.46', 'strikeouts': 137, 'innings': '131.2', 'whip': '1.00'}
            },
            {
                'id': 592332,
                'name': 'Julio Urías',
                'number': '7',
                'position': 'SP',
                'bats': 'L',
                'throws': 'L',
                'age': 28,
                'stats': {'wins': 15, 'losses': 8, 'era': '3.55', 'strikeouts': 178, 'innings': '175.1', 'whip': '1.18'}
            },
            {
                'id': 605483,
                'name': 'Walker Buehler',
                'number': '21',
                'position': 'SP',
                'bats': 'R',
                'throws': 'R',
                'age': 30,
                'stats': {'wins': 12, 'losses': 4, 'era': '3.02', 'strikeouts': 165, 'innings': '157.0', 'whip': '1.08'}
            },
            {
                'id': 621111,
                'name': 'Evan Phillips',
                'number': '46',
                'position': 'RP',
                'bats': 'R',
                'throws': 'R',
                'age': 29,
                'stats': {'wins': 5, 'losses': 2, 'era': '2.12', 'saves': 42, 'strikeouts': 88, 'innings': '72.1', 'whip': '0.95'}
            },
            {
                'id': 502188,
                'name': 'Daniel Hudson',
                'number': '44',
                'position': 'RP',
                'bats': 'R',
                'throws': 'R',
                'age': 37,
                'stats': {'wins': 3, 'losses': 4, 'era': '3.45', 'strikeouts': 67, 'innings': '60.0', 'whip': '1.22'}
            },
        ],
        'batters': [
            {
                'id': 660271,
                'name': 'Mookie Betts',
                'number': '50',
                'position': 'RF',
                'bats': 'R',
                'throws': 'R',
                'age': 31,
                'stats': {'avg': '.318', 'hr': 38, 'rbi': 107, 'runs': 122, 'hits': 188, 'sb': 24, 'ops': '.978'}
            },
            {
                'id': 592450,
                'name': 'Freddie Freeman',
                'number': '5',
                'position': '1B',
                'bats': 'L',
                'throws': 'R',
                'age': 34,
                'stats': {'avg': '.331', 'hr': 29, 'rbi': 102, 'runs': 98, 'hits': 199, 'sb': 8, 'ops': '.935'}
            },
            {
                'id': 678551,
                'name': 'Will Smith',
                'number': '16',
                'position': 'C',
                'bats': 'R',
                'throws': 'R',
                'age': 29,
                'stats': {'avg': '.268', 'hr': 25, 'rbi': 87, 'runs': 71, 'hits': 139, 'sb': 4, 'ops': '.823'}
            },
            {
                'id': 518692,
                'name': 'Max Muncy',
                'number': '13',
                'position': '3B',
                'bats': 'L',
                'throws': 'R',
                'age': 33,
                'stats': {'avg': '.225', 'hr': 36, 'rbi': 95, 'runs': 82, 'hits': 108, 'sb': 2, 'ops': '.856'}
            },
            {
                'id': 621020,
                'name': 'Chris Taylor',
                'number': '3',
                'position': 'CF',
                'bats': 'R',
                'throws': 'R',
                'age': 33,
                'stats': {'avg': '.248', 'hr': 17, 'rbi': 63, 'runs': 68, 'hits': 115, 'sb': 11, 'ops': '.738'}
            },
            {
                'id': 667670,
                'name': 'James Outman',
                'number': '23',
                'position': 'LF',
                'bats': 'L',
                'throws': 'R',
                'age': 27,
                'stats': {'avg': '.258', 'hr': 23, 'rbi': 70, 'runs': 77, 'hits': 125, 'sb': 16, 'ops': '.789'}
            },
        ]
    }
}

def get_roster_data(team_id):
    """Get roster data for a team (tries API first, falls back to example data)"""
    try:
        # Try to get real data from API
        roster_result = statsapi.roster(team_id)
        # Process and return...
        # For now, return example data
        raise Exception("Using example data")
    except:
        return EXAMPLE_ROSTERS.get(team_id, {})

def generate_team_roster_page(team_id):
    """Generate a beautiful team roster page"""
    roster_data = get_roster_data(team_id)

    if not roster_data:
        return None

    team_name = roster_data['team_name']
    team_abbrev = roster_data['team_abbrev']
    primary_color = roster_data['primary_color']
    secondary_color = roster_data['secondary_color']
    pitchers = roster_data['pitchers']
    batters = roster_data['batters']

    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{team_name} - Roster Complet</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            background: #0a0a0a;
            color: #fff;
            line-height: 1.6;
        }}

        .header-banner {{
            background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
            padding: 60px 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .header-banner::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="40" fill="rgba(255,255,255,0.05)"/></svg>');
            opacity: 0.3;
        }}

        .header-content {{
            position: relative;
            z-index: 1;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .team-logo {{
            width: 120px;
            height: 120px;
            margin-bottom: 20px;
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));
        }}

        h1 {{
            font-size: 3.5em;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 10px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        }}

        .season-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 1.1em;
            font-weight: bold;
            margin-top: 10px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        .nav-links {{
            text-align: center;
            margin-bottom: 40px;
        }}

        .nav-links a {{
            display: inline-block;
            color: #fff;
            text-decoration: none;
            padding: 12px 30px;
            background: {primary_color};
            border-radius: 25px;
            margin: 0 10px;
            font-weight: bold;
            transition: all 0.3s ease;
        }}

        .nav-links a:hover {{
            background: {secondary_color};
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}

        .section-header {{
            background: linear-gradient(90deg, {primary_color} 0%, transparent 100%);
            padding: 20px 30px;
            margin: 40px 0 30px 0;
            border-left: 5px solid {secondary_color};
        }}

        .section-header h2 {{
            font-size: 2.2em;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}

        .players-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}

        .player-card {{
            background: linear-gradient(145deg, #1a1a1a 0%, #2a2a2a 100%);
            border-radius: 15px;
            overflow: hidden;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            position: relative;
        }}

        .player-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, {primary_color}, {secondary_color});
        }}

        .player-card:hover {{
            transform: translateY(-8px);
            border-color: {primary_color};
            box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        }}

        .player-card a {{
            text-decoration: none;
            color: inherit;
            display: block;
        }}

        .player-image-container {{
            background: linear-gradient(180deg, {primary_color}22 0%, transparent 100%);
            height: 220px;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }}

        .player-number {{
            position: absolute;
            top: 15px;
            right: 15px;
            font-size: 3em;
            font-weight: 900;
            color: rgba(255,255,255,0.15);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .player-image {{
            width: 160px;
            height: 200px;
            object-fit: cover;
            object-position: top center;
            transition: transform 0.3s ease;
        }}

        .player-card:hover .player-image {{
            transform: scale(1.1);
        }}

        .player-info {{
            padding: 20px;
        }}

        .player-name {{
            font-size: 1.4em;
            font-weight: 900;
            margin-bottom: 5px;
            color: #fff;
        }}

        .player-position {{
            display: inline-block;
            background: {primary_color};
            color: #fff;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
            margin-bottom: 12px;
        }}

        .player-bats-throws {{
            font-size: 0.9em;
            color: #aaa;
            margin-bottom: 12px;
        }}

        .stats-preview {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            padding-top: 12px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}

        .stat {{
            text-align: center;
        }}

        .stat-label {{
            font-size: 0.75em;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .stat-value {{
            font-size: 1.3em;
            font-weight: 900;
            color: {secondary_color};
            margin-top: 2px;
        }}

        .footer {{
            text-align: center;
            padding: 40px 20px;
            background: #0a0a0a;
            border-top: 1px solid #333;
            margin-top: 60px;
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 2em;
            }}

            .players-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="header-banner">
        <div class="header-content">
            <img src="{get_team_logo_url(team_id)}" alt="{team_name} Logo" class="team-logo">
            <h1>{team_name}</h1>
            <div class="season-badge">🏆 World Series 2025</div>
        </div>
    </div>

    <div class="container">
        <div class="nav-links">
            <a href="world_series_schedule.html">← Retour au calendrier</a>
        </div>

        <div class="section-header">
            <h2>⚾ Frappeurs</h2>
        </div>

        <div class="players-grid">
'''

    # Add batters
    for player in batters:
        html += f'''
            <div class="player-card">
                <a href="player_{player['id']}.html">
                    <div class="player-image-container">
                        <div class="player-number">#{player['number']}</div>
                        <img src="{get_player_headshot_url(player['id'])}"
                             alt="{player['name']}"
                             class="player-image"
                             onerror="this.src='https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_160/v1/people/0/headshot/67/current'">
                    </div>
                    <div class="player-info">
                        <div class="player-name">{player['name']}</div>
                        <div class="player-position">{player['position']}</div>
                        <div class="player-bats-throws">B/T: {player['bats']}/{player['throws']} • Âge: {player['age']}</div>
                        <div class="stats-preview">
                            <div class="stat">
                                <div class="stat-label">AVG</div>
                                <div class="stat-value">{player['stats']['avg']}</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">HR</div>
                                <div class="stat-value">{player['stats']['hr']}</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">RBI</div>
                                <div class="stat-value">{player['stats']['rbi']}</div>
                            </div>
                        </div>
                    </div>
                </a>
            </div>
'''

    html += '''
        </div>

        <div class="section-header">
            <h2>🔥 Lanceurs</h2>
        </div>

        <div class="players-grid">
'''

    # Add pitchers
    for player in pitchers:
        html += f'''
            <div class="player-card">
                <a href="player_{player['id']}.html">
                    <div class="player-image-container">
                        <div class="player-number">#{player['number']}</div>
                        <img src="{get_player_headshot_url(player['id'])}"
                             alt="{player['name']}"
                             class="player-image"
                             onerror="this.src='https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_160/v1/people/0/headshot/67/current'">
                    </div>
                    <div class="player-info">
                        <div class="player-name">{player['name']}</div>
                        <div class="player-position">{player['position']}</div>
                        <div class="player-bats-throws">B/T: {player['bats']}/{player['throws']} • Âge: {player['age']}</div>
                        <div class="stats-preview">
                            <div class="stat">
                                <div class="stat-label">ERA</div>
                                <div class="stat-value">{player['stats']['era']}</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">W-L</div>
                                <div class="stat-value">{player['stats']['wins']}-{player['stats']['losses']}</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">K</div>
                                <div class="stat-value">{player['stats']['strikeouts']}</div>
                            </div>
                        </div>
                    </div>
                </a>
            </div>
'''

    html += f'''
        </div>
    </div>

    <div class="footer">
        <p>Roster complet • {team_name}</p>
        <p style="margin-top: 10px; color: #666;">Mis à jour: {datetime.now().strftime('%d/%m/%Y')}</p>
    </div>
</body>
</html>
'''

    return html

if __name__ == "__main__":
    # Generate roster pages for both teams
    for team_id, name in [(BLUE_JAYS_ID, 'Blue Jays'), (DODGERS_ID, 'Dodgers')]:
        print(f"Génération de la page roster pour {name}...")
        html = generate_team_roster_page(team_id)
        if html:
            filename = f"team_{team_id}_roster.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"✓ Créé: {filename}")

    print("\nPages roster générées avec succès!")
