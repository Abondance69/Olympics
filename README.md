# 🏅 Olympics Analytics & Predictions

> **120 ans d'histoire olympique analysés par l'IA**  
> Athènes 1896 → Paris 2024

![Olympics](https://img.shields.io/badge/Olympics-1896--2024-blue)
![React](https://img.shields.io/badge/React-18.2-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6?logo=typescript)
![Node.js](https://img.shields.io/badge/Node.js-Express-339933?logo=node.js)

---

## 📋 Table des matières

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Technologies](#technologies)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [API Endpoints](#api-endpoints)
- [Déploiement](#déploiement)
- [Équipe](#équipe)
- [Ressources](#ressources)

---

## 🎯 À propos

Ce projet a été développé dans le cadre d'un **hackathon** visant à :

1. **Explorer** 120 ans de données olympiques (1896-2022)
2. **Visualiser** les performances historiques avec des graphiques interactifs
3. **Prédire** les résultats des JO Paris 2024 avec Machine Learning & Deep Learning
4. **Analyser** les performances de la France aux Jeux Olympiques

### 📊 Données utilisées

- **21,000+** médailles décernées
- **162,000+** résultats d'épreuves
- **74,000+** athlètes participants
- **53** pays hôtes
- Source : [Olympics.com](https://olympics.com)

---

## ✨ Fonctionnalités

### 🏠 Accueil
- Vue d'ensemble des statistiques olympiques
- Timeline des événements marquants
- Navigation intuitive

### 📊 Statistiques
- Évolution des médailles par année
- Sports dominants (graphiques Plotly interactifs)
- Pays organisateurs
- Événements historiques vérifiés

### 🤖 Prédictions IA
- **France** : Prédiction médailles Paris 2024 (Or, Argent, Bronze)
- **Top 25** pays participants
- **Athlètes** susceptibles de médailler
- **Clustering** des pays par performance
- **Comparaison** des modèles ML/DL

### 🇫🇷 Focus France
- Bilan des 840 médailles françaises
- Meilleure/pire performance aux JO
- Sports d'excellence (Escrime, Cyclisme, etc.)
- JO organisés par la France

### ℹ️ À propos
- Présentation du projet
- Technologies utilisées
- Modèles d'IA développés

---

## 🛠️ Technologies

### Frontend
- **React** 18.2 + **TypeScript** 5.3
- **Plotly.js** - Visualisations interactives
- **React Router** - Navigation
- **Axios** - Requêtes HTTP
- **CSS3** - Design responsive

### Backend
- **Node.js** + **Express.js**
- **CORS** & **dotenv**
- **MySQL/MariaDB** ou **PostgreSQL**
- REST API

### Intelligence Artificielle
- **Python** - Pandas / PySpark
- **Scikit-learn** - Machine Learning
- **TensorFlow** - Deep Learning
- Modèles : Random Forest, SVM, CNN, LSTM

---

## 📦 Installation

### Prérequis

- Node.js (v16+)
- npm ou yarn
- Base de données (MySQL/MariaDB ou PostgreSQL)

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/hackathon-olympics.git
cd hackathon-olympics
```

### 2. Installation Backend

```bash
cd backend
npm install
```

Créer un fichier `.env` basé sur `.env.example` :

```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=votre_utilisateur
DB_PASSWORD=votre_mot_de_passe
DB_NAME=olympics_db
PORT=5000
NODE_ENV=development
```

### 3. Installation Frontend

```bash
cd ../frontend
npm install
```

Créer un fichier `.env` dans `frontend/` :

```env
REACT_APP_API_URL=http://localhost:5000/api
```

---

## 🚀 Utilisation

### Démarrer le backend

```bash
cd backend
npm start
# ou en mode développement
npm run dev
```

Le serveur démarre sur `http://localhost:5000`

### Démarrer le frontend

```bash
cd frontend
npm start
```

L'application s'ouvre sur `http://localhost:3000`

### Tests API

Tester les endpoints :

```bash
# Test de connexion
curl http://localhost:5000

# Statistiques
curl http://localhost:5000/api/stats/overview
curl http://localhost:5000/api/stats/france

# Prédictions
curl http://localhost:5000/api/predictions/paris2024
```

---

## 📁 Structure du projet

```
hackathon-olympics/
├── backend/
│   ├── config/
│   │   └── database.js          # Configuration BD
│   ├── routes/
│   │   ├── stats.js             # Routes statistiques
│   │   ├── predictions.js       # Routes prédictions
│   │   ├── countries.js         # Routes pays
│   │   └── athletes.js          # Routes athlètes
│   ├── server.js                # Serveur Express
│   ├── package.json
│   └── .env.example
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header/
│   │   │   └── Footer/
│   │   ├── pages/
│   │   │   ├── Home/
│   │   │   ├── Statistics/
│   │   │   ├── Predictions/
│   │   │   ├── France/
│   │   │   └── About/
│   │   ├── services/
│   │   │   └── api.ts           # Service API
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── index.css
│   ├── package.json
│   └── tsconfig.json
│
└── README.md
```

---

## 🌐 API Endpoints

### Statistiques

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/stats/overview` | Statistiques globales |
| GET | `/api/stats/france` | Statistiques France |
| GET | `/api/stats/medals-by-year?country=FRA` | Médailles par année |
| GET | `/api/stats/top-sports` | Sports dominants |
| GET | `/api/stats/host-countries` | Pays organisateurs |
| GET | `/api/stats/historic-events` | Événements marquants |

### Prédictions

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/predictions/paris2024` | Prédictions Paris 2024 |
| GET | `/api/predictions/athletes` | Athlètes médaillés |
| GET | `/api/predictions/clustering` | Clustering pays |
| GET | `/api/predictions/models` | Comparaison modèles |

### Pays

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/countries` | Liste des pays |
| GET | `/api/countries/:code` | Détails d'un pays |
| GET | `/api/countries/compare?countries=FRA,USA` | Comparer pays |

### Athlètes

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/athletes` | Liste athlètes |
| GET | `/api/athletes/legends` | Athlètes légendaires |
| GET | `/api/athletes/:id` | Détails athlète |

---

## 🚢 Déploiement

### Frontend (Vercel / Netlify)

```bash
cd frontend
npm run build
# Déployer le dossier build/
```

### Backend (Heroku / Railway)

```bash
cd backend
# Ajouter Procfile
echo "web: node server.js" > Procfile
# Push vers Heroku
```

### Base de données

- **Production** : AlwaysData, Azure, AWS RDS
- **Connexion** : Mettre à jour les variables d'environnement

---

## 👥 Équipe

### Répartition des tâches

- **DBA** : Configuration base de données, gestion privilèges
- **M1** : Pandas, Machine Learning (sklearn), Frontend React
- **M2** : Spark, Deep Learning (TensorFlow), Architecture

### Gestion de projet

📋 **Trello** : [Lien vers le board Trello](#)

### Présentation

📊 **Slides** : [Lien vers Google Slides](#)

---

## 📚 Ressources

### Documentation officielle

- [React](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Express.js](https://expressjs.com/)
- [Plotly.js](https://plotly.com/javascript/)

### Cheat Sheets

- [PySpark SQL](https://www.codecademy.com/learn/big-data-pyspark/modules/spark-data-frames-with-py-spark-sql/cheatsheet)
- [Pandas](https://nbhosting.inria.fr/builds/ue12-p23-numerique/handouts/latest/_downloads/d7e00a6ac60d14256515f7c2cafd935b/cheatsheet-pandas.pdf)
- [Scikit-Learn](https://images.datacamp.com/image/upload/v1676302389/Marketing/Blog/Scikit-Learn_Cheat_Sheet.pdf)

### Articles de référence

- [Nielsen Gracenote - Medal Predictions](https://www.nielsen.com/fr/news-center/2022/nielsen-gracenote-releases-final-virtual-medal-table-forecast/)
- [Predicting Tokyo 2020](https://fonseca-carlos.medium.com/predicting-tokyo-2020-total-medal-count-f808e80e4406)

---

## 📄 Licence

Ce projet a été développé dans un cadre éducatif (Hackathon).

---

## 🏅 Screenshots

### Page d'accueil
![Home]()

### Statistiques interactives
![Statistics]()

### Prédictions IA
![Predictions]()

### Focus France
![France]()

---

**Développé avec ❤️ pour le Hackathon Olympics** | Paris 2024 🇫🇷
