# 🏅 Olympics Analytics

Olympics Analytics est une application complète permettant l’exploration et l’analyse des données des Jeux Olympiques grâce à un tableau de bord interactif et des modèles d'intelligence artificielle.

Elle permet de :
- explorer et visualiser l’historique des performances olympiques,
- analyser des clusters de pays selon leurs résultats,
- prédire le nombre de médailles d’un pays pour une édition donnée,
- prédire les performances d’un athlète via un modèle de Machine Learning.

🚀 Technologies utilisées :  
- **Frontend :** React + Vite + Plotly (visualisation de données)
- **Backend :** Flask (API REST + training et exécution des modèles ML)
- **Machine Learning :** Scikit-Learn (régression, clustering)
- **Déploiement :** Netlify (Frontend) + Render (Backend/API)

Ce projet combine **Data Engineering + Machine Learning + FullStack Web** pour transformer des données brutes en insights visuels et en prédictions intelligentes.


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
│                   BACKEND (Flask)                      │
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
│            BASE DE DONNÉES (MySQL)               │
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
│  │ Pandas       │  │ Scikit-learn │  │  TensorFlow  │     │
│  │ Data Prep    │  │ ML Models    │  │              │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---


## 📁 Architecture du projet

```bash
OLYMPICS/
│
├── backend/ # API Flask (ML + connexion DB + endpoints)
│ ├── app.py # Point d’entrée du serveur Flask
│ ├── config.py # Gestion chemins ML et variables d'env
│ ├── utils.py # Helpers pour charger modèles & JSON
│ ├── requirements.txt # Dépendances backend
│ └── ml/
│ ├────  data_preparation.py # Nettoyage dataset
│ ├──── model_medals_prediction.py # Training modèle médailles
│ ├──── athlete_model_training.py # Training modèle athlète
│ └──── output/
│ ├──────── best_model.pkl
│ ├──────── country_encoder.pkl
│ ├──────── athlete_model.pkl
│ ├──────── clusters.csv
│ └──────── metrics_report.json
│
└── frontend/ # Application React (Vite)
├── src/
│ ├── components/
│ ├── pages/
│ └── App.tsx
├── public/
│ └── _redirects
├── vite.config.js
├── package.json
└── build/ # Généré après npm run build
```


## 🚀 Installation (Local)

### ⬇️ 1. Backend (Flask + ML)

```sh
cd backend
python -m venv venv
source venv/bin/activate       # Windows → venv\Scripts\activate
pip install -r requirements.txt
➡️ Lancer l’API Flask :

python app.py
L’API démarre sur :
👉 http://localhost:8000/api
```


### ⬇️ 2. Frontend (React + Vite)
```sh
cd frontend
npm install
npm run dev
➡️ Accès :
👉 http://localhost:5173
```

### 🔥 Endpoints API
```bash
Méthode	Route	Fonction
GET	/api/health	Vérifie modèles + encoder
GET	/api/countries/clusters	Retourne les clusters de pays
POST	/api/predict/medals	Prédit le nombre de médailles
POST	/api/predict/athlete	Prédit performance athlète
```

```json
// Exemple de json
{
  "country_name": "France",
  "game_year": 2024,
  "game_season": "Summer"
}
```

### ✅ Déploiement
#### 1.🌍 Frontend (Netlify)

Configuration Netlify :

Base directory :	frontend
Build command :	npm run build
Publish directory :	frontend/build
Frontend : https://690dc7aa65e9730008cf2824--olympics69.netlify.app/


#### 2. 🔧 Backend (Render)

Select repo : backend/
PORT : 8080
Backend : https://olympics-production-2b95.up.railway.app/



### 🧠 Models Machine Learning

- Prédiction médailles	LinearRegression / RandomForest	best_model.pkl
- Encodage pays	LabelEncoder	country_encoder.pkl
- Clusterisation pays	K-Means	clusters.csv


***📌 Variables d'environnement***
Créer un fichier :
```bash
DB_HOST
DB_USER
DB_PASSWORD
DB_DATABASE
DB_PORT
```



**👨Auteur**
Projet développé par 
👨‍💻 Abondance KAZADI 
👨‍💻 Mostafa BOUCHAMMA

Repo github : https://github.com/Abondance69/Olympics
Présentation : https://1drv.ms/p/c/9f6d69c5df427f6d/ET6KPkqsl1VNlX1mOOnjFUEBVwNQpTEnQgxS8Gq0aThNbQ?e=WHCPZh
Trello Url : https://trello.com/b/jQh0XcEo/olympics