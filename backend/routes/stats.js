const express = require('express');
const router = express.Router();
const db = require('../config/database');

// GET /api/stats/overview - Statistiques globales
router.get('/overview', async (req, res) => {
  try {
    // Exemple de données - adapter selon votre schéma de BD
    const stats = {
      totalMedals: 21000,
      totalAthletes: 74000,
      totalCountries: 206,
      totalEvents: 162000
    };
    
    res.json(stats);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des statistiques' });
  }
});

// GET /api/stats/france - Statistiques de la France
router.get('/france', async (req, res) => {
  try {
    // TODO: Requête SQL pour récupérer les médailles de la France
    const query = `
      SELECT 
        COUNT(*) as total_medals,
        SUM(CASE WHEN medal_type = 'Gold' THEN 1 ELSE 0 END) as gold,
        SUM(CASE WHEN medal_type = 'Silver' THEN 1 ELSE 0 END) as silver,
        SUM(CASE WHEN medal_type = 'Bronze' THEN 1 ELSE 0 END) as bronze
      FROM medals
      WHERE country_code = 'FRA'
    `;
    
    // Exemple de données
    const franceStats = {
      totalMedals: 840,
      gold: 248,
      silver: 276,
      bronze: 316,
      bestYear: { year: 1900, medals: 101 },
      worstYear: { year: 1904, medals: 0 }
    };
    
    res.json(franceStats);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des stats France' });
  }
});

// GET /api/stats/medals-by-year - Médailles par année
router.get('/medals-by-year', async (req, res) => {
  try {
    const { country } = req.query;
    
    // Exemple de données pour visualisation
    const data = [
      { year: 1896, gold: 5, silver: 4, bronze: 2 },
      { year: 1900, gold: 26, silver: 41, bronze: 34 },
      { year: 1904, gold: 0, silver: 0, bronze: 0 },
      // ... plus de données
      { year: 2020, gold: 10, silver: 12, bronze: 11 }
    ];
    
    res.json(data);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des médailles par année' });
  }
});

// GET /api/stats/top-sports - Sports dominants
router.get('/top-sports', async (req, res) => {
  try {
    const topSports = [
      { sport: 'Athlétisme', medals: 150, percentage: 17.9 },
      { sport: 'Natation', medals: 85, percentage: 10.1 },
      { sport: 'Escrime', medals: 118, percentage: 14.0 },
      { sport: 'Cyclisme', medals: 92, percentage: 11.0 },
      { sport: 'Judo', medals: 55, percentage: 6.5 }
    ];
    
    res.json(topSports);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des sports' });
  }
});

// GET /api/stats/host-countries - Pays organisateurs
router.get('/host-countries', async (req, res) => {
  try {
    const hosts = [
      { country: 'USA', count: 8, cities: ['Los Angeles', 'Atlanta', 'Salt Lake City'] },
      { country: 'France', count: 6, cities: ['Paris', 'Chamonix', 'Grenoble', 'Albertville'] },
      { country: 'UK', count: 3, cities: ['London'] },
      { country: 'Japan', count: 4, cities: ['Tokyo', 'Sapporo', 'Nagano'] }
    ];
    
    res.json(hosts);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des pays hôtes' });
  }
});

// GET /api/stats/historic-events - Événements marquants
router.get('/historic-events', async (req, res) => {
  try {
    const events = [
      {
        id: 1,
        year: 1924,
        title: 'Premiers JO d\'hiver à Chamonix',
        description: 'Naissance des Jeux Olympiques d\'hiver',
        verified: true
      },
      {
        id: 2,
        year: 1900,
        title: 'Participation féminine',
        description: 'Les femmes participent pour la première fois aux JO à Paris',
        verified: true
      },
      {
        id: 3,
        year: 2012,
        title: 'Égalité des sexes',
        description: 'Tous les pays participants ont envoyé des athlètes féminines',
        verified: true
      }
    ];
    
    res.json(events);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des événements' });
  }
});

module.exports = router;
