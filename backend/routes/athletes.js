const express = require('express');
const router = express.Router();

// GET /api/athletes - Liste des athlètes
router.get('/', async (req, res) => {
  try {
    const { country, sport, limit = 50 } = req.query;
    
    const athletes = [
      {
        id: 1,
        name: 'Michael Phelps',
        country: 'USA',
        sport: 'Swimming',
        totalMedals: 28,
        gold: 23,
        silver: 3,
        bronze: 2,
        photo: '/images/athletes/phelps.jpg'
      },
      {
        id: 2,
        name: 'Usain Bolt',
        country: 'Jamaica',
        sport: 'Athletics',
        totalMedals: 8,
        gold: 8,
        silver: 0,
        bronze: 0,
        photo: '/images/athletes/bolt.jpg'
      }
      // ... plus d'athlètes
    ];
    
    res.json(athletes);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des athlètes' });
  }
});

// GET /api/athletes/legends - Athlètes légendaires
router.get('/legends', async (req, res) => {
  try {
    const legends = [
      {
        name: 'Michael Phelps',
        country: 'USA',
        sport: 'Swimming',
        medals: 28,
        fact: 'Plus médaillé de l\'histoire olympique'
      },
      {
        name: 'Johnny Weissmuller',
        country: 'USA',
        sport: 'Swimming',
        medals: 5,
        fact: 'A joué Tarzan dans 12 films'
      },
      {
        name: 'Christa Ludinger-Rothenburger',
        country: 'Germany',
        sport: 'Speed Skating / Cycling',
        medals: 6,
        fact: 'Seule athlète médaillée hiver/été la même année (1988)'
      }
    ];
    
    res.json(legends);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des légendes' });
  }
});

// GET /api/athletes/:id - Détails d'un athlète
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    const athlete = {
      id: 1,
      name: 'Michael Phelps',
      country: 'USA',
      birthDate: '1985-06-30',
      sport: 'Swimming',
      height: 193,
      weight: 91,
      totalMedals: 28,
      gold: 23,
      silver: 3,
      bronze: 2,
      olympics: [
        { year: 2004, city: 'Athens', medals: { gold: 6, silver: 0, bronze: 2 } },
        { year: 2008, city: 'Beijing', medals: { gold: 8, silver: 0, bronze: 0 } },
        { year: 2012, city: 'London', medals: { gold: 4, silver: 2, bronze: 0 } },
        { year: 2016, city: 'Rio', medals: { gold: 5, silver: 1, bronze: 0 } }
      ],
      records: [
        '23 médailles d\'or olympiques',
        '8 médailles d\'or en une seule édition (2008)',
        'Plus médaillé de l\'histoire'
      ]
    };
    
    res.json(athlete);
  } catch (error) {
    console.error('Erreur:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération de l\'athlète' });
  }
});

module.exports = router;
