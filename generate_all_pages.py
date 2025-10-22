#!/usr/bin/env python
# encoding=utf-8
"""
Master script to generate all World Series pages:
- Main schedule page
- Team roster pages
- Individual player profile pages
"""

import subprocess
import sys

def main():
    print("=" * 60)
    print("  GÉNÉRATION COMPLÈTE DES PAGES SÉRIE MONDIALE")
    print("=" * 60)
    print()

    scripts = [
        ("world_series_schedule.py", "Page de calendrier principal"),
        ("world_series_teams.py", "Pages de roster des équipes"),
        ("world_series_players.py", "Profils individuels des joueurs")
    ]

    for script, description in scripts:
        print(f"[PAGE] {description}...")
        print(f"   Exécution de {script}...")
        try:
            result = subprocess.run(
                [sys.executable, script],
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
            if result.stderr:
                print("Avertissements:", result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"[ERREUR] Erreur lors de l'exécution de {script}")
            print(e.stderr)
            return False
        print()

    print("=" * 60)
    print("[OK] GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
    print("=" * 60)
    print()
    print("Pages générées:")
    print("  [CALENDRIER] world_series_schedule.html - Page d'accueil avec le calendrier")
    print("  [EQUIPE] team_141_roster.html - Roster des Blue Jays")
    print("  [EQUIPE] team_119_roster.html - Roster des Dodgers")
    print("  [JOUEUR] player_*.html - Profils individuels de tous les joueurs")
    print()
    print("Pour voir les pages, ouvrez 'world_series_schedule.html' dans votre navigateur!")
    print()

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
