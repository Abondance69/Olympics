const express = require('express');
const router = express.Router();
const axios = require('axios');

// URL de l'API ML Python
const ML_API_URL = process.env.ML_API_URL || 'http://localhost:5001';

/**
 * Proxy vers l'API ML Python Flask
 * Permet au frontend de passer uniquement par le backend Express
 */

// GET /api/ml/health - Vérifier le statut de l'API ML
router.get('/health', async (req, res) => {
  try {
    const response = await axios.get(`${ML_API_URL}/api/ml/health`, {
      timeout: 5000
    });
    res.json(response.data);
  } catch (error) {
    console.error('❌ API ML non disponible:', error.message);
    res.status(503).json({ 
      error: 'API ML non disponible',
      message: 'Le service de prédiction ML n\'est pas accessible. Assurez-vous que le serveur Python Flask est démarré.',
      status: 'offline'
    });
  }
});

// GET /api/ml/predict/paris2024 - Prédictions Paris 2024 (TOP 25)
router.get('/predict/paris2024', async (req, res) => {
  try {
    const response = await axios.get(`${ML_API_URL}/api/ml/predict/paris2024`, {
      timeout: 10000
    });
    
    // Enrichir avec des données de la base si disponible
    const predictions = response.data;
    
    res.json({
      success: true,
      source: 'ml-api',
      predictions: predictions.predictions || predictions,
      metadata: predictions.metadata || {
        model: 'Ensemble (Linear + Random Forest)',
        lastUpdated: new Date().toISOString()
      }
    });
  } catch (error) {
    console.error('❌ Erreur prédictions Paris 2024:', error.message);
    
    // Fallback sur données mockées si ML API down
    res.status(error.response?.status || 500).json({ 
      error: 'Erreur lors de la récupération des prédictions',
      message: error.message,
      fallback: true
    });
  }
});

// GET /api/ml/predict/country/:name - Prédiction pour un pays spécifique
router.get('/predict/country/:name', async (req, res) => {
  try {
    const countryName = req.params.name;
    const response = await axios.get(
      `${ML_API_URL}/api/ml/predict/country/${encodeURIComponent(countryName)}`,
      { timeout: 5000 }
    );
    
    res.json({
      success: true,
      country: countryName,
      prediction: response.data
    });
  } catch (error) {
    console.error(`❌ Erreur prédiction ${req.params.name}:`, error.message);
    
    if (error.response?.status === 404) {
      res.status(404).json({ 
        error: 'Pays non trouvé',
        message: `Aucune prédiction disponible pour "${req.params.name}"`
      });
    } else {
      res.status(500).json({ 
        error: 'Erreur lors de la récupération de la prédiction',
        message: error.message
      });
    }
  }
});

// GET /api/ml/models/info - Informations sur les modèles ML
router.get('/models/info', async (req, res) => {
  try {
    const response = await axios.get(`${ML_API_URL}/api/ml/models/info`, {
      timeout: 5000
    });
    res.json(response.data);
  } catch (error) {
    console.error('❌ Erreur info modèles:', error.message);
    res.status(500).json({ 
      error: 'Erreur lors de la récupération des informations',
      message: error.message
    });
  }
});

// POST /api/ml/retrain - Réentraîner les modèles (ADMIN)
router.post('/retrain', async (req, res) => {
  try {
    console.log('🔄 Début du réentraînement des modèles ML...');
    
    const response = await axios.post(`${ML_API_URL}/api/ml/retrain`, req.body, {
      timeout: 60000 // 60 secondes pour le training
    });
    
    console.log('✅ Modèles réentraînés avec succès');
    res.json({
      success: true,
      message: 'Modèles réentraînés avec succès',
      data: response.data
    });
  } catch (error) {
    console.error('❌ Erreur réentraînement:', error.message);
    res.status(500).json({ 
      error: 'Erreur lors du réentraînement',
      message: error.message
    });
  }
});

// GET /api/ml/predictions/history - Historique des prédictions (à intégrer avec MySQL)
router.get('/predictions/history', async (req, res) => {
  try {
    // TODO: Récupérer depuis la base MySQL quand disponible
    // const [rows] = await db.query('SELECT * FROM predictions_history ORDER BY created_at DESC LIMIT 10');
    
    res.json({
      success: true,
      message: 'Feature en cours de développement - nécessite base de données MySQL',
      history: []
    });
  } catch (error) {
    console.error('❌ Erreur historique:', error.message);
    res.status(500).json({ 
      error: 'Erreur lors de la récupération de l\'historique',
      message: error.message
    });
  }
});

module.exports = router;
