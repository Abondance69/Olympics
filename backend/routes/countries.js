const express = require('express');
const router = express.Router();

// GET /api/countries - Liste de tous les pays
router.get('/', async (req, res) => {
  try {
    const countries = [
      { code: 'FRA', name: 'France', flag: '🇫🇷', participations: 28 },
      { code: 'USA', name: 'United States', flag: '🇺🇸', participations: 28 },
      { code: 'GBR', name: 'Great Britain', flag: '🇬🇧', participations: 29 },
      { code: 'CHN', name: 'China', flag: '🇨🇳', participations: 11 },
      { code: 'JPN', name: 'Japan', flag: '🇯🇵', participations: 23 }
      // ... plus de pays
    ];
    
    res.json(countries);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des pays' });
  }
});

// GET /api/countries/:code - Détails d'un pays
router.get('/:code', async (req, res) => {
  try {
    const { code } = req.params;
    
    const countryDetails = {
      code: 'FRA',
      name: 'France',
      flag: '🇫🇷',
      totalMedals: 840,
      gold: 248,
      silver: 276,
      bronze: 316,
      firstParticipation: 1896,
      hostings: [
        { year: 1900, city: 'Paris', season: 'Summer' },
        { year: 1924, city: 'Paris', season: 'Summer' },
        { year: 1924, city: 'Chamonix', season: 'Winter' },
        { year: 1968, city: 'Grenoble', season: 'Winter' },
        { year: 1992, city: 'Albertville', season: 'Winter' },
        { year: 2024, city: 'Paris', season: 'Summer' }
      ],
      topSports: [
        { sport: 'Escrime', medals: 118 },
        { sport: 'Cyclisme', medals: 92 },
        { sport: 'Athlétisme', medals: 88 }
      ],
      bestOlympics: { year: 1900, medals: 101, city: 'Paris' },
      medalsByYear: [
        { year: 1896, total: 11 },
        { year: 1900, total: 101 },
        // ... historique complet
        { year: 2021, total: 33 }
      ]
    };
    
    res.json(countryDetails);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des détails du pays' });
  }
});

// GET /api/countries/compare - Comparer plusieurs pays
router.get('/compare', async (req, res) => {
  try {
    const { countries } = req.query; // Ex: ?countries=FRA,USA,CHN
    
    const comparison = {
      countries: ['FRA', 'USA', 'CHN'],
      data: [
        {
          country: 'FRA',
          totalMedals: 840,
          goldRate: 0.295,
          avgMedalsPerOlympics: 30
        },
        {
          country: 'USA',
          totalMedals: 2827,
          goldRate: 0.395,
          avgMedalsPerOlympics: 101
        },
        {
          country: 'CHN',
          totalMedals: 608,
          goldRate: 0.387,
          avgMedalsPerOlympics: 55
        }
      ]
    };
    
    res.json(comparison);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la comparaison des pays' });
  }
});

module.exports = router;
