const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const db = require('./config/database');

// Charger les variables d'environnement
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logger middleware
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path} - ${new Date().toISOString()}`);
  next();
});

// Routes
const statsRoutes = require('./routes/stats');
const predictionsRoutes = require('./routes/predictions');
const countriesRoutes = require('./routes/countries');
const athletesRoutes = require('./routes/athletes');
const mlRoutes = require('./routes/ml'); // 🤖 Routes ML/AI

app.use('/api/stats', statsRoutes);
app.use('/api/predictions', predictionsRoutes);
app.use('/api/countries', countriesRoutes);
app.use('/api/athletes', athletesRoutes);
app.use('/api/ml', mlRoutes); // 🤖 API Machine Learning

// Route de test
app.get('/', (req, res) => {
  res.json({
    message: 'Olympics Analytics API',
    version: '2.0.0',
    endpoints: {
      stats: '/api/stats',
      predictions: '/api/predictions',
      countries: '/api/countries',
      athletes: '/api/athletes',
      ml: '/api/ml' // 🤖 Machine Learning endpoints
    },
    mlEndpoints: {
      health: '/api/ml/health',
      paris2024: '/api/ml/predict/paris2024',
      country: '/api/ml/predict/country/:name',
      modelsInfo: '/api/ml/models/info',
      retrain: '/api/ml/retrain (POST)'
    }
  });
});

// Gestion des erreurs 404
app.use((req, res) => {
  res.status(404).json({ error: 'Route non trouvée' });
});

// Gestion des erreurs globales
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ 
    error: 'Erreur serveur', 
    message: process.env.NODE_ENV === 'development' ? err.message : undefined 
  });
});

// Démarrage du serveur
app.listen(PORT, () => {
  console.log(`🚀 Serveur démarré sur le port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🗄️  Database: ${process.env.DB_TYPE || 'mysql'}`);
});
