# 🏅 Olympics Analytics - Backend API (Python/Flask)

Backend principal de l'application Olympics Analytics. Cette API Flask consolidée regroupe toutes les routes nécessaires basées sur les spécifications du projet.

## 🎯 Architecture

```
Frontend (React)
       ↓
Backend API (Python/Flask) - Port 5000
       ↓
MySQL Database (AlwaysData) + ML Predictions
```

## 📋 Prérequis

- Python 3.8+
- pip
- MySQL Database (AlwaysData)
- Fichier `.env` avec les credentials

## 🚀 Installation

```bash
# Se placer dans le dossier backend
cd backend

# Créer un environnement virtuel (optionnel)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

## ⚙️ Configuration

Assurez-vous d'avoir un fichier `.env` à la racine du projet avec :

```env
DB_HOST=mysql-abondance69.alwaysdata.net
DB_USER=votre_user
DB_PASSWORD=votre_password
DB_DATABASE=abondance69_olympics
DB_PORT=3306
```

## 🏃 Démarrage

```bash
# Démarrer le serveur
python app.py
```

Le serveur démarre sur `http://localhost:5000`

## 📡 Endpoints API

### A. API Générales (infos de base)

#### 1. Health Check
```http
GET /api/health
```
Vérifie que l'API et la base de données sont opérationnels.

**Réponse:**
```json
{
  "status": "healthy",
  "message": "API operational",
  "database": "connected"
}
```

#### 2. Liste des Jeux Olympiques
```http
GET /api/hosts
```
**Utilisation:** Dropdown ou timeline sur le site

**Réponse:**
```json
{
  "success": true,
  "data": [
    {
      "game_name": "Paris 2024",
      "game_year": 2024,
      "game_season": "Summer",
      "game_location": "Paris, France"
    }
  ]
}
```

#### 3. Détails d'un JO spécifique
```http
GET /api/hosts/<year>
```
**Utilisation:** Page de détails d'un événement

#### 4. Liste des athlètes
```http
GET /api/athletes?limit=50&country=FR&sport=Athletics
```
**Utilisation:** Liste d'athlètes avec recherche

**Paramètres:**
- `limit` (optional): Nombre de résultats (défaut: 50)
- `country` (optional): Code pays (ex: FR, US, CN)
- `sport` (optional): Nom du sport

#### 5. Profil d'un athlète
```http
GET /api/athletes/<name>
```
**Utilisation:** Profil d'un athlète

#### 6. Résultats filtrables
```http
GET /api/results?country=FR&sport=Athletics&year=2020&medal_type=GOLD&limit=100
```
**Utilisation:** Table des résultats filtrables

**Paramètres:**
- `country` (optional): Code pays
- `sport` (optional): Discipline
- `year` (optional): Année olympique
- `medal_type` (optional): GOLD, SILVER, BRONZE
- `limit` (optional): Nombre de résultats

#### 7. Liste des pays
```http
GET /api/countries
```
**Utilisation:** Dropdown de filtres par pays

### B. API Analytiques (stats dynamiques pour dashboards)

#### 1. Statistiques globales
```http
GET /api/stats/overview
```
**Utilisation:** Dashboard principal

**Réponse:**
```json
{
  "success": true,
  "data": {
    "totalMedals": 21697,
    "totalCountries": 150,
    "totalEvents": 265,
    "totalSports": 50
  }
}
```

#### 2. Statistiques France
```http
GET /api/stats/france
```

#### 3. Médailles par pays
```http
GET /api/stats/medals-by-country?limit=10
```
**Utilisation:** Graphique "Top 10 pays"

#### 4. Médailles par année
```http
GET /api/stats/medals-by-year?country=FR
```
**Utilisation:** Graphique d'évolution

#### 5. Médailles par discipline
```http
GET /api/stats/medals-by-discipline?limit=10&country=FR
```
**Utilisation:** Diagramme circulaire ou barres

#### 6. Ratio de genre
```http
GET /api/stats/gender-ratio
```
**Utilisation:** Donut chart

#### 7. Distribution d'âge
```http
GET /api/stats/age-distribution
```
**Utilisation:** Histogramme dynamique

#### 8. Résumé des JO
```http
GET /api/stats/hosts-summary
```
**Utilisation:** Dashboard principal

### C. API IA / Prédiction

#### 1. Prédictions Paris 2024
```http
GET /api/predictions/paris2024
```
**Utilisation:** Affichage des prédictions ML

**Réponse:**
```json
{
  "success": true,
  "data": [
    {
      "country_code": "US",
      "country_name": "United States",
      "predicted_gold": 39,
      "predicted_silver": 41,
      "predicted_bronze": 33,
      "predicted_total": 113
    }
  ],
  "olympics": "Paris 2024",
  "total_countries": 25
}
```

#### 2. Prédiction par pays
```http
GET /api/predictions/country/<code>
```
**Exemple:** `/api/predictions/country/FR`

## 📊 Format des réponses

### Succès
```json
{
  "success": true,
  "data": { ... }
}
```

### Erreur
```json
{
  "success": false,
  "error": "Message d'erreur"
}
```

## 🔧 Structure du projet

```
backend/
├── app.py              # Application principale avec toutes les routes
├── requirements.txt    # Dépendances Python
├── README.md          # Cette documentation
└── routes/            # Dossier vide (structure pour extension future)
```

## 🛡️ Sécurité

- ✅ CORS activé pour le frontend
- ✅ Requêtes SQL paramétrées (protection SQL injection)
- ✅ Variables d'environnement pour les credentials
- ⚠️ À ajouter : Rate limiting, authentication

## 🐛 Debugging

Pour activer les logs détaillés, modifier dans `app.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 🧪 Tests

```bash
# Test de l'API avec curl
curl http://localhost:5000/api/health
curl http://localhost:5000/api/stats/overview
curl http://localhost:5000/api/hosts
```

## 📚 Intégration Frontend

Dans le frontend React, utiliser cette URL de base :
```javascript
const API_BASE_URL = 'http://localhost:5000/api';

// Exemple d'appel
fetch(`${API_BASE_URL}/stats/overview`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## 🔮 Améliorations futures

- [ ] Caching avec Redis
- [ ] Rate limiting
- [ ] Authentication JWT
- [ ] WebSocket pour real-time
- [ ] Tests unitaires
- [ ] Documentation Swagger/OpenAPI
- [ ] Logging avancé
- [ ] Monitoring

## 🤝 Contribution

Voir [CONTRIBUTING.md](../CONTRIBUTING.md)

## 📝 Notes

- Les données de genre et d'âge sont actuellement estimées
- Les prédictions ML nécessitent d'avoir exécuté le modèle au préalable
- La base de données contient 21,697+ médailles historiques

---

Développé avec ❤️ pour le Hackathon Olympics
