# 🗄️ Configuration Base de Données MySQL - Olympics Analytics

## 📋 Instructions pour votre collègue

### 1. Export de la base de données

Demandez à votre collègue d'exporter la base avec cette commande :

```bash
# Export complet avec structure et données
mysqldump -u root -p olympics_db > olympics_db_export.sql

# OU avec compression
mysqldump -u root -p olympics_db | gzip > olympics_db_export.sql.gz
```

### 2. Import dans votre projet

Une fois que vous avez reçu le fichier `olympics_db_export.sql` :

#### Option A : Via ligne de commande
```bash
# Si vous avez MySQL/MariaDB installé localement
mysql -u root -p olympics_db < olympics_db_export.sql

# OU si c'est compressé
gunzip < olympics_db_export.sql.gz | mysql -u root -p olympics_db
```

#### Option B : Via phpMyAdmin / MySQL Workbench
1. Ouvrir phpMyAdmin (`http://localhost/phpmyadmin`)
2. Créer la base `olympics_db` si elle n'existe pas
3. Sélectionner la base
4. Onglet "Importer"
5. Choisir le fichier `.sql`
6. Cliquer "Exécuter"

### 3. Configuration du projet

Vérifiez que le fichier `.env` contient les bonnes informations :

```env
# Configuration MySQL
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=VOTRE_MOT_DE_PASSE
DB_NAME=olympics_db

# Server
PORT=5000
NODE_ENV=development
```

### 4. Structure attendue de la base de données

Le projet attend ces tables principales :

```sql
-- Table des pays
CREATE TABLE countries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(3) UNIQUE NOT NULL,
    continent VARCHAR(50),
    population BIGINT,
    gdp DECIMAL(15,2)
);

-- Table des Jeux Olympiques
CREATE TABLE olympics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    season VARCHAR(10) NOT NULL, -- 'Summer' ou 'Winter'
    city VARCHAR(100),
    country_code VARCHAR(3)
);

-- Table des médailles
CREATE TABLE medals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    olympic_id INT,
    country_code VARCHAR(3),
    sport VARCHAR(100),
    event VARCHAR(200),
    medal_type ENUM('Gold', 'Silver', 'Bronze'),
    athlete_name VARCHAR(200),
    FOREIGN KEY (olympic_id) REFERENCES olympics(id),
    FOREIGN KEY (country_code) REFERENCES countries(code)
);

-- Table des athlètes
CREATE TABLE athletes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    country_code VARCHAR(3),
    sport VARCHAR(100),
    birth_year INT,
    gender ENUM('M', 'F'),
    FOREIGN KEY (country_code) REFERENCES countries(code)
);

-- Table des statistiques par pays/olympiade
CREATE TABLE country_stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    olympic_id INT,
    country_code VARCHAR(3),
    gold_medals INT DEFAULT 0,
    silver_medals INT DEFAULT 0,
    bronze_medals INT DEFAULT 0,
    total_medals INT DEFAULT 0,
    athlete_count INT DEFAULT 0,
    FOREIGN KEY (olympic_id) REFERENCES olympics(id),
    FOREIGN KEY (country_code) REFERENCES countries(code)
);
```

### 5. Test de connexion

Une fois la base importée, testez la connexion :

```bash
cd backend
npm start
```

Vous devriez voir :
```
✅ MySQL/MariaDB pool créé
✅ Connexion MySQL/MariaDB établie
🚀 Serveur démarré sur le port 5000
```

### 6. Vérification des données

Testez les endpoints :
- http://localhost:5000/api/stats
- http://localhost:5000/api/countries
- http://localhost:5000/api/predictions/paris2024

---

## 🔧 Troubleshooting

### Erreur : "Access denied for user 'root'@'localhost'"
➡️ Vérifiez le mot de passe dans `.env`

### Erreur : "Unknown database 'olympics_db'"
➡️ Créez la base : `CREATE DATABASE olympics_db;`

### Erreur : "Table doesn't exist"
➡️ Assurez-vous d'avoir bien importé le fichier SQL complet

### Port 3306 déjà utilisé
➡️ Changez le port dans `.env` : `DB_PORT=3307`

---

## 📦 Fichiers à recevoir de votre collègue

✅ **OBLIGATOIRE** : `olympics_db_export.sql` (ou `.sql.gz`)
📄 **OPTIONNEL** : Documentation sur la structure des tables
📊 **OPTIONNEL** : Dataset CSV source si vous voulez réimporter

---

## 🚀 Prochaines étapes après l'import

1. ✅ Importer la base de données
2. ✅ Tester la connexion backend
3. ✅ Intégrer l'API ML avec les vraies données
4. ✅ Mettre à jour les requêtes SQL dans `/backend/routes/`
5. ✅ Tester le frontend avec données réelles
