# 🚀 Guide de démarrage rapide

## Installation

### 1. Installer toutes les dépendances

```powershell
# Depuis la racine du projet
npm run install-all
```

OU installer manuellement :

```powershell
# Backend
cd backend
npm install

# Frontend
cd ..\frontend
npm install
```

### 2. Configurer les variables d'environnement

**Backend** : Copier `.env.example` vers `.env` dans le dossier `backend/`

```powershell
cd backend
Copy-Item .env.example .env
```

Modifier `backend/.env` avec vos informations de base de données.

**Frontend** : Copier `.env.example` vers `.env` dans le dossier `frontend/`

```powershell
cd ..\frontend
Copy-Item .env.example .env
```

### 3. Démarrer l'application

**Terminal 1 - Backend :**

```powershell
cd backend
npm start
```

**Terminal 2 - Frontend :**

```powershell
cd frontend
npm start
```

L'application sera accessible sur : http://localhost:3000

L'API sera accessible sur : http://localhost:5000

---

## 🗄️ Configuration Base de Données

### MySQL/MariaDB

1. Créer la base de données :

```sql
CREATE DATABASE olympics_db;
```

2. Importer les données (fichiers SQL à fournir)

### PostgreSQL

1. Créer la base de données :

```sql
CREATE DATABASE olympics_db;
```

2. Modifier `backend/.env` :

```env
DB_TYPE=postgres
DB_HOST=localhost
DB_PORT=5432
```

---

## 📝 Commandes utiles

```powershell
# Installer toutes les dépendances
npm run install-all

# Démarrer le backend (production)
npm run start-backend

# Démarrer le backend (développement avec nodemon)
npm run dev-backend

# Démarrer le frontend
npm run start-frontend

# Build du frontend pour production
npm run build-frontend
```

---

## 🔧 Troubleshooting

### Erreur de connexion à la base de données

- Vérifier que MySQL/PostgreSQL est démarré
- Vérifier les credentials dans `backend/.env`
- Tester la connexion manuellement

### Port déjà utilisé

Si le port 3000 ou 5000 est déjà utilisé :

**Frontend** : Accepter d'utiliser un autre port lorsque proposé

**Backend** : Modifier `PORT` dans `backend/.env`

### Modules non trouvés

```powershell
# Supprimer node_modules et réinstaller
rm -r -fo node_modules
npm install
```

---

## 📱 Accès à l'application

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:5000
- **API Test** : http://localhost:5000/api/stats/overview

---

Pour plus d'informations, consulter le [README principal](README.md)
