# Traitement des Données des Athlètes Olympiques

## 📊 Résumé de l'Analyse

### Statistiques Clés
- **Total d'athlètes médaillés**: 12,889
- **Légendes olympiques** (5+ médailles d'or): 27 athlètes
- **Sports représentés**: 40+ disciplines
- **Période couverte**: 1896-2022

## 🏆 Top 10 Athlètes de Tous les Temps

1. **Michael PHELPS** (USA) - 16 médailles (13🥇 2🥈 1🥉)
2. **Larisa LATYNINA** (URSS) - 14 médailles (6🥇 5🥈 3🥉)
3. **Nikolay ANDRIANOV** (URSS) - 12 médailles (6🥇 3🥈 3🥉)
4. **Marit BJOERGEN** (Norvège) - 12 médailles (6🥇 3🥈 3🥉)
5. **Boris SHAKHLIN** (URSS) - 10 médailles (6🥇 2🥈 2🥉)
6. **Ireen WÜST** (Pays-Bas) - 10 médailles (5🥇 4🥈 1🥉)
7. **Takashi ONO** (Japon) - 10 médailles (3🥇 3🥈 4🥉)
8. **Alexei NEMOV** (Russie) - 10 médailles (3🥇 2🥈 5🥉)
9. **Paavo NURMI** (Finlande) - 9 médailles (6🥇 3🥈 0🥉)
10. **Björn DAEHLIE** (Norvège) - 9 médailles (6🥇 3🥈 0🥉)

## 👑 Légendes Olympiques (5+ Médailles d'Or)

| Rang | Athlète | Pays | Médailles d'Or | Total |
|------|---------|------|----------------|-------|
| 1 | Michael PHELPS | USA | 13 | 16 |
| 2 | Ray EWRY | USA | 8 | 8 |
| 3 | Vera CASLAVSKA | Tchécoslovaquie | 7 | 8 |
| 4 | Carl LEWIS | USA | 7 | 8 |
| 5 | Usain BOLT | Jamaïque | 6 | 6 |

## 🏃 Top 5 Sports par Nombre d'Athlètes

1. **Athlétisme** - 2,094 athlètes
2. **Lutte** - 1,101 athlètes
3. **Boxe** - 907 athlètes
4. **Natation** - 891 athlètes
5. **Tir** - 570 athlètes

## 🌍 Top 10 Pays par Nombre d'Athlètes Médaillés

| Rang | Pays | Athlètes | Médailles |
|------|------|----------|-----------|
| 1 | États-Unis | 1,848 | 2,616 |
| 2 | URSS | 749 | 1,077 |
| 3 | Allemagne | 657 | 923 |
| 4 | Grande-Bretagne | 625 | 812 |
| 5 | France | 569 | 746 |
| 6 | Chine | 475 | 734 |
| 7 | Italie | 439 | 618 |
| 8 | Suède | 392 | 555 |
| 9 | Russie | 377 | 511 |
| 10 | Japon | 358 | 508 |

## 🎯 Athlètes Polyvalents (2+ Sports)

Top 5 athlètes ayant gagné des médailles dans plusieurs sports:

1. **Arianna FONTANA** - 7 médailles dans 2 sports (Short Track)
2. **Gert FREDRIKSSON** - 7 médailles dans 2 sports (Canoe)
3. **Isabell WERTH** - 6 médailles dans 2 sports (Équitation)
4. **Johan GRØTTUMSBRÅTEN** - 6 médailles dans 2 sports (Ski de fond, Combiné nordique)
5. **Leontien ZIJLAARD-VAN MOORSEL** - 6 médailles dans 2 sports (Cyclisme)

## 📂 Fichiers JSON Générés

### 1. `top_athletes.json`
- **Contenu**: Top 100 athlètes médaillés de tous les temps
- **Structure**:
```json
{
  "name": "Michael PHELPS",
  "country": "United States of America",
  "country_code": "USA",
  "total_medals": 16,
  "gold": 13,
  "silver": 2,
  "bronze": 1
}
```

### 2. `olympic_legends.json`
- **Contenu**: 27 légendes olympiques (5+ médailles d'or)
- **Structure**: Identique à `top_athletes.json`

## 🚀 API Endpoints - Athlètes

### Base URL: `http://localhost:5002`

### 1. Liste des Athlètes (Filtrable)
```
GET /api/athletes?limit=50&country=FR&sport=Athletics
```
**Paramètres**:
- `limit` (optionnel): Nombre de résultats (défaut: 50)
- `country` (optionnel): Code pays (ex: FR, USA)
- `sport` (optionnel): Nom du sport (ex: Athletics, Swimming)

**Réponse**:
```json
{
  "success": true,
  "data": [
    {
      "athlete_full_name": "Carl LEWIS",
      "country": "United States of America",
      "total_medals": 8,
      "gold": 7,
      "silver": 1,
      "bronze": 0
    }
  ],
  "count": 50
}
```

### 2. Top Athlètes
```
GET /api/athletes/top?limit=10
```
**Paramètres**:
- `limit` (optionnel): Nombre de résultats (défaut: 10)

**Réponse**: Liste des athlètes avec le plus de médailles

### 3. Athlètes par Sport
```
GET /api/athletes/by-sport?limit=5
```
**Paramètres**:
- `limit` (optionnel): Nombre d'athlètes par sport (défaut: 5)

**Réponse**:
```json
{
  "success": true,
  "data": {
    "Athletics": [
      {
        "athlete_full_name": "Carl LEWIS",
        "country": "United States of America",
        "total_medals": 8,
        "gold": 7,
        "silver": 1,
        "bronze": 0
      }
    ],
    "Swimming": [...]
  }
}
```

### 4. Légendes Olympiques
```
GET /api/athletes/legends
```
**Réponse**: Athlètes avec 5+ médailles d'or avec liste des sports pratiqués

### 5. Statistiques Générales
```
GET /api/athletes/stats
```
**Réponse**:
```json
{
  "success": true,
  "data": {
    "total_athletes": 12889,
    "top_medalist": {
      "name": "Michael PHELPS",
      "total_medals": 16
    },
    "top_gold_medalist": {
      "name": "Michael PHELPS",
      "gold_medals": 13
    },
    "top_countries": [
      {
        "country": "United States of America",
        "athletes": 1848
      }
    ]
  }
}
```

## 🔧 Utilisation

### Script Python d'Analyse
```bash
cd c:\Users\SURFACEE\Desktop\hackathon-olympics
.venv\Scripts\python.exe database\analyze_athletes.py
```

### API Flask MySQL
```bash
.venv\Scripts\python.exe database\api_mysql.py
```
API disponible sur: `http://localhost:5002`

## 📝 Notes Techniques

### Source de Données
- **Base de données**: MySQL AlwaysData
- **Table**: `medals` (21,697 lignes)
- **Colonnes utilisées**: 
  - `athlete_full_name`
  - `country_name`, `country_code`
  - `discipline_title` (sport)
  - `medal_type` (GOLD, SILVER, BRONZE)
  - `slug_game` (identifiant des JO)

### Technologies
- **Python 3.13.2**
- **Bibliothèques**: pymysql, flask, flask-cors, python-dotenv
- **Format de sortie**: JSON (UTF-8)

### Conversion des Types
⚠️ Les résultats SQL MySQL retournent des types `Decimal` qui doivent être convertis en `int` avant la sérialisation JSON.

## 🎨 Intégration Frontend

Pour utiliser ces données dans le frontend React:

```typescript
// frontend/src/services/api.ts
export const getTopAthletes = (limit: number = 10) => {
  return api.get(`/athletes/top?limit=${limit}`);
};

export const getAthleteLegends = () => {
  return api.get('/athletes/legends');
};

export const getAthleteStats = () => {
  return api.get('/athletes/stats');
};
```

## 📊 Exemples de Visualisations

### Suggestions pour le Frontend:
1. **Podium des Légendes** - Top 3 athlètes avec animations
2. **Carte Interactive** - Pays avec le plus d'athlètes médaillés
3. **Timeline** - Évolution des records d'un athlète
4. **Racing Bar Chart** - Animation des pays par nombre d'athlètes
5. **Réseau de Sports** - Athlètes polyvalents

---

**Date de génération**: Janvier 2025  
**Source**: Base de données MySQL AlwaysData (olympic_hackaton)  
**Période**: Jeux Olympiques 1896-2022
