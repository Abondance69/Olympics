const express = require('express');
const router = express.Router();

// GET /api/predictions/paris2024 - Prédictions pour Paris 2024
router.get('/paris2024', async (req, res) => {
  try {
    const predictions = {
      france: {
        gold: 28,
        silver: 26,
        bronze: 22,
        total: 76,
        confidence: 0.85,
        model: 'Random Forest',
        rank: 8
      },
      top25: [
        { rank: 1, country: 'USA', gold: 113, silver: 91, bronze: 71, total: 275 },
        { rank: 2, country: 'China', gold: 88, silver: 70, bronze: 61, total: 219 },
        { rank: 3, country: 'Japan', gold: 58, silver: 41, bronze: 37, total: 136 },
        { rank: 4, country: 'Great Britain', gold: 50, silver: 45, bronze: 43, total: 138 },
        { rank: 5, country: 'ROC', gold: 47, silver: 52, bronze: 50, total: 149 },
        { rank: 6, country: 'Australia', gold: 46, silver: 38, bronze: 38, total: 122 },
        { rank: 7, country: 'Germany', gold: 37, silver: 36, bronze: 38, total: 111 },
        { rank: 8, country: 'France', gold: 28, silver: 26, bronze: 22, total: 76 }
        // ... Top 25
      ],
      lastUpdated: new Date().toISOString(),
      modelMetrics: {
        accuracy: 0.87,
        rmse: 2.3,
        mae: 1.8
      }
    };
    
    res.json(predictions);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des prédictions' });
  }
});

// GET /api/predictions/athletes - Prédiction des athlètes médaillés
router.get('/athletes', async (req, res) => {
  try {
    const athletePredictions = [
      {
        name: 'Teddy Riner',
        sport: 'Judo',
        country: 'France',
        predictedMedal: 'Gold',
        probability: 0.92,
        category: 'Heavyweight'
      },
      {
        name: 'Léon Marchand',
        sport: 'Swimming',
        country: 'France',
        predictedMedal: 'Gold',
        probability: 0.88,
        category: '400m Individual Medley'
      },
      {
        name: 'Clarisse Agbegnenou',
        sport: 'Judo',
        country: 'France',
        predictedMedal: 'Gold',
        probability: 0.85,
        category: '-63kg'
      }
      // ... plus d'athlètes
    ];
    
    res.json(athletePredictions);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des prédictions athlètes' });
  }
});

// GET /api/predictions/clustering - Clustering des pays
router.get('/clustering', async (req, res) => {
  try {
    const clustering = {
      optimalK: 5,
      silhouetteScore: 0.73,
      clusters: [
        {
          id: 1,
          name: 'Super Powers',
          countries: ['USA', 'China', 'Russia', 'Germany', 'Great Britain'],
          avgMedals: 250,
          characteristics: 'Dominance historique, grandes ressources'
        },
        {
          id: 2,
          name: 'Strong Performers',
          countries: ['France', 'Japan', 'Australia', 'Italy', 'Netherlands'],
          avgMedals: 85,
          characteristics: 'Performance constante, spécialisation sports'
        },
        {
          id: 3,
          name: 'Emerging Nations',
          countries: ['Brazil', 'South Korea', 'Spain', 'Kenya', 'Jamaica'],
          avgMedals: 45,
          characteristics: 'Croissance récente, niches sportives'
        },
        {
          id: 4,
          name: 'Moderate Performers',
          countries: ['Canada', 'Poland', 'Sweden', 'Switzerland', 'Norway'],
          avgMedals: 30,
          characteristics: 'Performance stable, focus sports d\'hiver'
        },
        {
          id: 5,
          name: 'Occasional Medalists',
          countries: ['...', '...'],
          avgMedals: 8,
          characteristics: 'Participation irrégulière'
        }
      ]
    };
    
    res.json(clustering);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération du clustering' });
  }
});

// GET /api/predictions/models - Comparaison des modèles ML/DL
router.get('/models', async (req, res) => {
  try {
    const models = [
      {
        name: 'Random Forest',
        type: 'Machine Learning',
        accuracy: 0.87,
        rmse: 2.3,
        trainTime: '45s',
        selected: true
      },
      {
        name: 'Decision Tree',
        type: 'Machine Learning',
        accuracy: 0.82,
        rmse: 3.1,
        trainTime: '12s',
        selected: false
      },
      {
        name: 'SVM',
        type: 'Machine Learning',
        accuracy: 0.84,
        rmse: 2.8,
        trainTime: '120s',
        selected: false
      },
      {
        name: 'CNN',
        type: 'Deep Learning',
        accuracy: 0.89,
        rmse: 2.0,
        trainTime: '5m 30s',
        selected: false
      },
      {
        name: 'LSTM',
        type: 'Deep Learning',
        accuracy: 0.86,
        rmse: 2.4,
        trainTime: '8m 15s',
        selected: false
      }
    ];
    
    res.json(models);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des modèles' });
  }
});

module.exports = router;
