# 🏗️ Architecture du Projet

## Vue d'ensemble

Ce document décrit l'architecture technique de l'application Olympics Analytics.

---

## 📊 Diagramme d'architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        UTILISATEUR                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React/TS)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Pages      │  │  Components  │  │   Services   │     │
│  │ - Home       │  │ - Header     │  │ - api.ts     │     │
│  │ - Statistics │  │ - Footer     │  │              │     │
│  │ - Predictions│  │ - Charts     │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Plotly.js (Visualizations)              │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (Express.js)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Routes     │  │  Middleware  │  │   Config     │     │
│  │ - stats      │  │ - CORS       │  │ - database   │     │
│  │ - predictions│  │ - Logger     │  │              │     │
│  │ - countries  │  │ - Error      │  │              │     │
│  │ - athletes   │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │ SQL
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            BASE DE DONNÉES (MySQL/PostgreSQL)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Tables     │  │    Views     │  │   Triggers   │     │
│  │ - countries  │  │ - medals_by_ │  │              │     │
│  │ - olympics   │  │   country    │  │              │     │
│  │ - athletes   │  │ - top_athletes│ │              │     │
│  │ - medals     │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                       ▲
                       │
┌──────────────────────┴──────────────────────────────────────┐
│             INTELLIGENCE ARTIFICIELLE (Python)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Pandas/Spark │  │  Scikit-learn│  │  TensorFlow  │     │
│  │ Data Prep    │  │  ML Models   │  │  DL Models   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Frontend Architecture

### Technologies
- **Framework** : React 18.2
- **Language** : TypeScript 5.3
- **Routing** : React Router DOM 6
- **HTTP Client** : Axios
- **Visualizations** : Plotly.js
- **Styling** : CSS3 (Native)

### Structure des dossiers

```
frontend/src/
├── components/          # Composants réutilisables
│   ├── Header/
│   │   ├── Header.tsx
│   │   └── Header.css
│   └── Footer/
│       ├── Footer.tsx
│       └── Footer.css
│
├── pages/              # Pages de l'application
│   ├── Home/
│   ├── Statistics/
│   ├── Predictions/
│   ├── France/
│   └── About/
│
├── services/           # Services API
│   └── api.ts
│
├── types/              # Types TypeScript (à créer)
│   └── index.ts
│
├── utils/              # Utilitaires (à créer)
│   └── helpers.ts
│
├── App.tsx             # Composant racine
├── index.tsx           # Point d'entrée
├── App.css             # Styles globaux
└── index.css           # Styles de base
```

### Flux de données

```
User Action
    ↓
Component (React)
    ↓
Service API (axios)
    ↓
Backend API
    ↓
Database
    ↓
Response
    ↓
Component Update (setState)
    ↓
Re-render UI
```

### Patterns utilisés

#### 1. **Component Pattern**
```typescript
// Composant fonctionnel avec hooks
const MyComponent: React.FC<Props> = ({ data }) => {
  const [state, setState] = useState();
  
  useEffect(() => {
    // Side effects
  }, [dependencies]);
  
  return <div>{/* JSX */}</div>;
};
```

#### 2. **Service Pattern**
```typescript
// Centralisation des appels API
export const getStats = () => api.get('/stats/overview');
export const getPredictions = () => api.get('/predictions/paris2024');
```

#### 3. **Custom Hooks** (à développer)
```typescript
// Hook personnalisé
const useStats = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchStats();
  }, []);
  
  return { stats, loading };
};
```

---

## 🔧 Backend Architecture

### Technologies
- **Runtime** : Node.js
- **Framework** : Express.js 4
- **Database Drivers** : mysql2, pg
- **Middleware** : CORS, dotenv

### Structure des dossiers

```
backend/
├── config/              # Configuration
│   └── database.js      # Connexion BD
│
├── routes/              # Routes API
│   ├── stats.js
│   ├── predictions.js
│   ├── countries.js
│   └── athletes.js
│
├── controllers/         # Logique métier (à créer)
│   └── statsController.js
│
├── models/              # Modèles de données (à créer)
│   └── Medal.js
│
├── middleware/          # Middleware custom (à créer)
│   ├── auth.js
│   └── validator.js
│
├── utils/               # Utilitaires (à créer)
│   └── helpers.js
│
├── server.js            # Point d'entrée
├── database_schema.sql  # Schéma de base
├── package.json
└── .env.example
```

### Patterns utilisés

#### 1. **MVC Pattern** (à améliorer)
```javascript
// Model
class Medal {
  static async findByCountry(countryCode) {
    // Requête BD
  }
}

// Controller
const getMedalsByCountry = async (req, res) => {
  const medals = await Medal.findByCountry(req.params.code);
  res.json(medals);
};

// Route
router.get('/medals/:code', getMedalsByCountry);
```

#### 2. **Middleware Pattern**
```javascript
// Logger middleware
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next();
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Server error' });
});
```

#### 3. **Router Pattern**
```javascript
// Groupement de routes
const router = express.Router();
router.get('/overview', getOverview);
router.get('/france', getFranceStats);
app.use('/api/stats', router);
```

---

## 🗄️ Database Architecture

### Modèle relationnel

```
countries (1) ──< (N) medals
    │                   │
    │                   └──> (N) events ──> (N) sports
    │
    └──> (N) athletes
    │
    └──> (1) olympics (host)
```

### Tables principales

#### countries
- `country_id` (PK)
- `country_code` (UNIQUE)
- `country_name`
- Métadonnées

#### medals
- `medal_id` (PK)
- `athlete_id` (FK)
- `event_id` (FK)
- `country_id` (FK)
- `medal_type` (ENUM)

#### athletes
- `athlete_id` (PK)
- `full_name`
- `country_id` (FK)
- Statistiques de médailles

### Optimisations

#### Index
```sql
CREATE INDEX idx_medals_country_date ON medals(country_id, medal_date);
CREATE INDEX idx_athletes_country ON athletes(country_id);
```

#### Views
```sql
CREATE VIEW medals_by_country AS
SELECT country_code, COUNT(*) as total
FROM medals JOIN countries
GROUP BY country_code;
```

#### Triggers
```sql
-- Mise à jour automatique des compteurs
CREATE TRIGGER update_athlete_medals
AFTER INSERT ON medals
FOR EACH ROW
UPDATE athletes SET total_medals = total_medals + 1;
```

---

## 🤖 AI Architecture

### Pipeline ML/DL

```
1. DATA COLLECTION
   ├── Web Scraping (Olympics.com)
   ├── Open Data
   └── Database Export

2. DATA PREPROCESSING
   ├── Cleaning (Pandas/Spark)
   ├── Feature Engineering
   └── Normalization

3. MODEL TRAINING
   ├── ML Models (Scikit-learn)
   │   ├── Random Forest
   │   ├── Decision Tree
   │   └── SVM
   └── DL Models (TensorFlow)
       ├── CNN
       └── LSTM

4. EVALUATION
   ├── Accuracy
   ├── RMSE
   ├── Confusion Matrix
   └── GridSearch

5. PREDICTION
   └── Paris 2024 Results

6. DEPLOYMENT
   └── API Integration
```

### Features utilisées

- **Historique** : Médailles précédentes
- **Démographique** : Population, PIB
- **Sportif** : Nombre d'athlètes, sports pratiqués
- **Tendances** : Évolution sur 10-20 ans

---

## 🔄 Communication entre composants

### API REST Endpoints

| Endpoint | Méthode | Description | Données retournées |
|----------|---------|-------------|-------------------|
| `/api/stats/overview` | GET | Stats globales | `{ totalMedals, totalAthletes, ... }` |
| `/api/predictions/paris2024` | GET | Prédictions 2024 | `{ france: {...}, top25: [...] }` |
| `/api/countries/:code` | GET | Détails pays | `{ code, name, medals, ... }` |

### Format des réponses

```typescript
// Success
{
  data: { /* payload */ },
  status: 200
}

// Error
{
  error: "Message d'erreur",
  status: 500
}
```

---

## 🔒 Sécurité

### Frontend
- ✅ Variables d'environnement pour URLs
- ✅ Validation des inputs
- ✅ Sanitization des données affichées

### Backend
- ✅ CORS configuré
- ✅ Variables d'environnement (.env)
- ✅ Gestion des erreurs
- ⚠️ À améliorer : Rate limiting, authentication

### Database
- ✅ Parameterized queries (SQL injection protection)
- ✅ Utilisateurs avec privilèges limités
- ⚠️ À améliorer : Encryption at rest

---

## 📈 Performance

### Frontend
- **Code splitting** : Lazy loading des pages
- **Memoization** : useMemo, useCallback
- **Optimized renders** : React.memo pour composants
- **Bundle size** : < 500KB gzipped

### Backend
- **Connection pooling** : Pool de connexions BD
- **Caching** : À implémenter (Redis)
- **Compression** : Gzip responses
- **Response time** : < 500ms moyenne

### Database
- **Indexes** : Sur colonnes fréquemment requêtées
- **Views** : Pré-calcul des agrégations
- **Partitioning** : Par année olympique (à considérer)

---

## 🧪 Testing Strategy

### Frontend
```typescript
// Unit tests
- Composants individuels
- Services API
- Utilitaires

// Integration tests
- Flux complets
- Navigation

// E2E tests
- Scénarios utilisateur
```

### Backend
```javascript
// Unit tests
- Routes individuelles
- Fonctions utilitaires

// Integration tests
- API endpoints + Database
- Error handling

// Load tests
- Performance sous charge
```

---

## 🚀 Déploiement

### Environnements

```
Development (Local)
    ↓
Staging (Test)
    ↓
Production (Live)
```

### CI/CD Pipeline (à implémenter)

```
Git Push
    ↓
GitHub Actions
    ↓
Run Tests
    ↓
Build
    ↓
Deploy to Staging
    ↓
Manual Approval
    ↓
Deploy to Production
```

---

## 📊 Monitoring (à implémenter)

### Métriques à suivre
- **Frontend** : Page load time, user interactions
- **Backend** : API response time, error rate
- **Database** : Query time, connection pool usage

### Outils recommandés
- **Logging** : Winston, Morgan
- **Monitoring** : New Relic, DataDog
- **Analytics** : Google Analytics
- **Error tracking** : Sentry

---

## 🔮 Évolutions futures

### Court terme
- [ ] Authentication système
- [ ] Caching avec Redis
- [ ] Tests automatisés
- [ ] CI/CD pipeline

### Moyen terme
- [ ] WebSockets pour real-time
- [ ] PWA (Progressive Web App)
- [ ] Multi-language support
- [ ] Admin dashboard

### Long terme
- [ ] Machine Learning API service
- [ ] Mobile app (React Native)
- [ ] Microservices architecture
- [ ] GraphQL API

---

Pour toute question sur l'architecture, ouvrir une issue ou contacter l'équipe technique.
