# 🚀 Guide de Déploiement

## Table des matières
- [Déploiement Frontend](#déploiement-frontend)
- [Déploiement Backend](#déploiement-backend)
- [Base de données en production](#base-de-données-en-production)

---

## 📱 Déploiement Frontend

### Option 1 : Vercel (Recommandé)

1. **Créer un compte sur [Vercel](https://vercel.com)**

2. **Installer Vercel CLI** (optionnel)
```powershell
npm install -g vercel
```

3. **Déployer**
```powershell
cd frontend
npm run build
vercel --prod
```

OU via l'interface web :
- Connecter votre repository GitHub
- Vercel détecte automatiquement React
- Build command : `npm run build`
- Output directory : `build`

4. **Variables d'environnement**
- Ajouter `REACT_APP_API_URL` dans les settings Vercel
- Valeur : URL de votre backend (ex: `https://your-api.herokuapp.com/api`)

### Option 2 : Netlify

1. **Build local**
```powershell
cd frontend
npm run build
```

2. **Déployer**
- Aller sur [Netlify](https://netlify.com)
- "Add new site" → "Deploy manually"
- Drag & drop le dossier `build/`

3. **Variables d'environnement**
- Site settings → Environment variables
- Ajouter `REACT_APP_API_URL`

---

## 🖥️ Déploiement Backend

### Option 1 : Heroku

1. **Créer une app Heroku**
```powershell
heroku login
cd backend
heroku create olympics-api-backend
```

2. **Ajouter un Procfile**
```powershell
echo "web: node server.js" > Procfile
```

3. **Configuration**
```powershell
# Variables d'environnement
heroku config:set DB_TYPE=postgres
heroku config:set DB_HOST=your-db-host
heroku config:set DB_USER=your-db-user
heroku config:set DB_PASSWORD=your-db-password
heroku config:set DB_NAME=olympics_db
heroku config:set NODE_ENV=production
```

4. **Déployer**
```powershell
git init
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Option 2 : Railway

1. **Créer un compte sur [Railway](https://railway.app)**

2. **Nouveau projet**
- "New Project" → "Deploy from GitHub repo"
- Sélectionner votre repository
- Root directory : `/backend`

3. **Variables d'environnement**
- Ajouter toutes les variables du fichier `.env`

4. **Déploiement automatique**
- Railway détecte Node.js automatiquement
- Chaque push déclenche un nouveau déploiement

### Option 3 : Render

1. **Créer un Web Service sur [Render](https://render.com)**

2. **Configuration**
- Build Command : `npm install`
- Start Command : `node server.js`
- Environment : Node

3. **Variables d'environnement**
- Ajouter dans le dashboard Render

---

## 🗄️ Base de données en Production

### Option 1 : AlwaysData (Recommandé pour étudiants)

1. **Créer un compte gratuit sur [AlwaysData](https://www.alwaysdata.com/fr/)**

2. **Créer une base de données**
- Bases de données → MariaDB ou PostgreSQL
- Noter les informations de connexion

3. **Importer les données**
- Via phpMyAdmin (MySQL)
- Via pgAdmin (PostgreSQL)

4. **Configuration**
```env
DB_HOST=mysql-votre-compte.alwaysdata.net
DB_PORT=3306
DB_USER=votre_user
DB_PASSWORD=votre_password
DB_NAME=votre_db
```

### Option 2 : Azure Database

1. **Créer une base Azure**
- Azure Portal → Create resource → Azure Database for MySQL/PostgreSQL

2. **Configuration firewall**
- Autoriser les IPs de votre backend

3. **Connection string**
```env
DB_HOST=your-server.mysql.database.azure.com
DB_USER=your-admin@your-server
DB_PASSWORD=your-password
DB_NAME=olympics_db
```

### Option 3 : Heroku Postgres (avec Heroku Backend)

```powershell
# Ajouter l'addon Postgres
heroku addons:create heroku-postgresql:hobby-dev

# La variable DATABASE_URL est automatiquement créée
```

Modifier `config/database.js` pour supporter `DATABASE_URL`.

### Option 4 : PlanetScale (MySQL)

1. **Créer un compte [PlanetScale](https://planetscale.com/)**

2. **Créer une base de données**
- New database → olympics_db

3. **Connection strings**
- PlanetScale fournit les credentials

---

## ✅ Checklist de déploiement

### Frontend
- [ ] Build réussi localement (`npm run build`)
- [ ] Variables d'environnement configurées
- [ ] URL de l'API mise à jour
- [ ] Tests sur mobile/tablette
- [ ] HTTPS activé

### Backend
- [ ] Tests API en local
- [ ] Variables d'environnement production
- [ ] Base de données accessible
- [ ] CORS configuré pour le frontend
- [ ] Logs configurés

### Base de données
- [ ] Tables créées
- [ ] Données importées
- [ ] Utilisateurs et privilèges configurés
- [ ] Backups configurés
- [ ] Indexes optimisés

---

## 🔒 Sécurité

### À faire absolument :

1. **Ne jamais commit `.env`**
```powershell
# Vérifier .gitignore
cat .gitignore | Select-String ".env"
```

2. **Utiliser des mots de passe forts**

3. **Limiter les CORS en production**
```javascript
// server.js
const corsOptions = {
  origin: 'https://votre-frontend.vercel.app',
  optionsSuccessStatus: 200
};
app.use(cors(corsOptions));
```

4. **Rate limiting**
```javascript
const rateLimit = require('express-rate-limit');
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);
```

---

## 📊 Monitoring

### Frontend
- Google Analytics
- Vercel Analytics (intégré)
- Sentry pour les erreurs

### Backend
- Logs Heroku : `heroku logs --tail`
- New Relic / DataDog
- Uptime monitoring (UptimeRobot)

---

## 🆘 Support

### Erreurs communes

**CORS Error**
```javascript
// Vérifier que le frontend origin est autorisé
app.use(cors({ origin: process.env.FRONTEND_URL }));
```

**Database connection timeout**
- Vérifier les credentials
- Vérifier le firewall
- Augmenter `connectionTimeoutMillis`

**Build failed**
- Nettoyer le cache : `npm cache clean --force`
- Supprimer `node_modules` et réinstaller

---

## 📚 Ressources

- [Vercel Documentation](https://vercel.com/docs)
- [Heroku Node.js Guide](https://devcenter.heroku.com/articles/deploying-nodejs)
- [Railway Docs](https://docs.railway.app/)
- [AlwaysData Documentation](https://help.alwaysdata.com/)

---

**Bon déploiement ! 🚀**
