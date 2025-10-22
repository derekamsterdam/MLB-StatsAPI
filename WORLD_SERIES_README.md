# 🏆 World Series - Système de Pages Interactives

## Vue d'ensemble

Ce système génère un site web complet de style magazine sportif pour la Série Mondiale entre les **Toronto Blue Jays** et les **Los Angeles Dodgers**.

## 📋 Structure du Système

### Pages Générées

1. **Page principale de calendrier** (`world_series_schedule.html`)
   - Affiche les matchs à venir
   - Date, heure et endroit pour chaque match
   - Liens cliquables vers les équipes

2. **Pages de roster d'équipe** (`team_141_roster.html`, `team_119_roster.html`)
   - Liste complète des joueurs
   - Séparation entre frappeurs et lanceurs
   - Statistiques en aperçu pour chaque joueur
   - Photos thumbnail des joueurs
   - Tous les éléments sont cliquables vers les profils individuels

3. **Profils individuels de joueurs** (`player_*.html`)
   - Photo de profil du joueur
   - Statistiques complètes de la saison
   - Informations biographiques
   - Design de magazine sportif professionnel

## 🎨 Caractéristiques du Design

### Style Magazine Sportif
- Couleurs d'équipe dynamiques (bleu/rouge pour Blue Jays, bleu/rouge pour Dodgers)
- Typographie audacieuse et moderne
- Animations au survol
- Design responsive (mobile et desktop)
- Photos haute résolution des joueurs

### Navigation
```
world_series_schedule.html
    ↓ (clic sur nom d'équipe)
team_141_roster.html (Blue Jays)
    ↓ (clic sur joueur)
player_592789.html (José Berríos)
    ↓ (retour au roster ou calendrier)
```

## 🚀 Utilisation

### Générer toutes les pages en une fois

```bash
python generate_all_pages.py
```

Ce script maître va:
1. ✅ Générer la page de calendrier principal
2. ✅ Générer les 2 pages de roster (Blue Jays et Dodgers)
3. ✅ Générer 22 profils de joueurs (11 par équipe)

### Générer les pages individuellement

```bash
# Page de calendrier uniquement
python world_series_schedule.py

# Pages de roster uniquement
python world_series_teams.py

# Profils de joueurs uniquement
python world_series_players.py
```

## 📊 Données Affichées

### Pour les Frappeurs
- Moyenne au bâton (AVG)
- Coups de circuit (HR)
- Points produits (RBI)
- Points marqués (Runs)
- Coups sûrs (Hits)
- Buts volés (SB)
- OPS (On-base + Slugging)

### Pour les Lanceurs
- Moyenne de points mérités (ERA)
- Victoires-Défaites (W-L)
- Retraits au bâton (K)
- Manches lancées (IP)
- WHIP
- Sauvetages (Saves) pour les releveurs

## 🖼️ Photos

Les photos des joueurs proviennent de l'API officielle MLB:
- URL de base: `https://img.mlbstatic.com/mlb-photos/`
- Format: headshots haute résolution
- Fallback automatique si l'image n'existe pas

## 📁 Fichiers du Projet

### Scripts Python
- `generate_all_pages.py` - Script maître pour tout générer
- `world_series_schedule.py` - Génère la page de calendrier
- `world_series_teams.py` - Génère les pages de roster
- `world_series_players.py` - Génère les profils de joueurs

### Fichiers HTML générés
- `world_series_schedule.html` - Page d'accueil
- `team_141_roster.html` - Roster Blue Jays
- `team_119_roster.html` - Roster Dodgers
- `player_*.html` - 22 profils de joueurs

## 🎯 Navigation Complète

### Depuis la Page Principale
Cliquez sur le nom d'une équipe dans un match → Accède au roster de l'équipe

### Depuis une Page de Roster
- Cliquez sur un joueur → Accède au profil du joueur
- Cliquez sur "Retour au calendrier" → Retour à la page principale

### Depuis un Profil de Joueur
- Cliquez sur "Retour au roster" → Retour à la page de l'équipe
- Cliquez sur "Calendrier" → Retour à la page principale

## 🌈 Personnalisation

### Couleurs d'Équipe
Définies dans `world_series_teams.py`:
```python
'primary_color': '#134A8E',    # Bleu Blue Jays
'secondary_color': '#E8291C',  # Rouge Blue Jays
```

### Ajouter des Joueurs
Modifiez `EXAMPLE_ROSTERS` dans `world_series_teams.py`

### Modifier le Design
Chaque script contient son propre CSS inline pour faciliter la personnalisation

## 🔗 Intégration API

Le système est conçu pour:
1. Tenter de récupérer les vraies données de l'API MLB Stats
2. Utiliser automatiquement des données d'exemple si l'API n'est pas disponible
3. Afficher une note visible quand les données sont des exemples

## 📱 Compatibilité

- ✅ Desktop (Chrome, Firefox, Safari, Edge)
- ✅ Tablette
- ✅ Mobile
- ✅ Design responsive adaptatif

## 🎭 Expérience Utilisateur

### Effets Visuels
- Animations de survol sur les cartes de joueurs
- Transitions fluides entre les pages
- Gradient dynamiques selon les couleurs d'équipe
- Ombres et profondeur pour un look moderne

### Performance
- CSS inline pour chargement rapide
- Images optimisées avec fallback
- Pas de dépendances externes

## 🏁 Pour Commencer

1. Générez toutes les pages:
```bash
python generate_all_pages.py
```

2. Ouvrez `world_series_schedule.html` dans votre navigateur

3. Explorez le site en cliquant sur les équipes et les joueurs!

---

**Développé pour la Série Mondiale 2025** 🏆⚾
