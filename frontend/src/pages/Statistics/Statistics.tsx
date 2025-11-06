/*
  api : http://localhost:8000/api/countries/clusters

  {
    "count": 2151,
    "data": [
        {
            "cluster": 1,
            "country_name": "Afghanistan",
            "game_season": "Summer",
            "game_year": 1996,
            "season_encoded": 0,
            "total_medals": 0
        },
    ]}
*/

import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { getMedalsByYear, getTopSports, getHostCountries, getHistoricEvents } from '../../services/api';
import './Statistics.css';

const Statistics: React.FC = () => {
  const [medalsByYear, setMedalsByYear] = useState<any[]>([]);
  const [topSports, setTopSports] = useState<any[]>([]);
  const [hosts, setHosts] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [medalsRes, sportsRes, hostsRes, eventsRes] = await Promise.all([
        getMedalsByYear('FRA'),
        getTopSports(),
        getHostCountries(),
        getHistoricEvents()
      ]);

      setMedalsByYear(medalsRes.data);
      setTopSports(sportsRes.data);
      setHosts(hostsRes.data);
      setEvents(eventsRes.data);
    } catch (error) {
      console.error('Error fetching statistics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  // Préparer les données pour les graphiques
  const years = medalsByYear.map(d => d.year);
  const goldMedals = medalsByYear.map(d => d.gold);
  const silverMedals = medalsByYear.map(d => d.silver);
  const bronzeMedals = medalsByYear.map(d => d.bronze);

  const sportsNames = topSports.map(s => s.sport);
  const sportsMedals = topSports.map(s => s.medals);
  // const sportsPercentages = topSports.map(s => s.percentage);

  return (
    <div className="statistics-page fade-in">
      <div className="hero">
        <div className="container">
          <h1 className="hero-title">📊 Statistiques Olympiques</h1>
          <p className="hero-subtitle">
            120 ans de données analysées avec visualisations interactives
          </p>
        </div>
      </div>

      <div className="container">
        {/* Medals by Year */}
        <section className="section">
          <h2 className="section-title">Évolution des médailles françaises</h2>
          <div className="chart-container">
            <Plot
              data={[
                {
                  x: years,
                  y: goldMedals,
                  name: 'Or',
                  type: 'scatter',
                  mode: 'lines+markers',
                  line: { color: '#FFD700', width: 3 },
                  marker: { size: 8 }
                },
                {
                  x: years,
                  y: silverMedals,
                  name: 'Argent',
                  type: 'scatter',
                  mode: 'lines+markers',
                  line: { color: '#C0C0C0', width: 3 },
                  marker: { size: 8 }
                },
                {
                  x: years,
                  y: bronzeMedals,
                  name: 'Bronze',
                  type: 'scatter',
                  mode: 'lines+markers',
                  line: { color: '#CD7F32', width: 3 },
                  marker: { size: 8 }
                }
              ]}
              layout={{
                title: 'Évolution des médailles olympiques (1896-2022)',
                xaxis: { title: 'Année' },
                yaxis: { title: 'Nombre de médailles' },
                autosize: true,
                hovermode: 'x unified'
              }}
              useResizeHandler={true}
              style={{ width: '100%', height: '500px' }}
            />
          </div>
        </section>

        {/* Top Sports */}
        <section className="section">
          <h2 className="section-title">Sports dominants de la France</h2>
          <div className="grid grid-2">
            <div className="chart-container">
              <Plot
                data={[
                  {
                    labels: sportsNames,
                    values: sportsMedals,
                    type: 'pie',
                    marker: {
                      colors: ['#0066cc', '#0052a3', '#003d7a', '#002952', '#FFD700']
                    },
                    textinfo: 'label+percent',
                    textposition: 'outside'
                  }
                ]}
                layout={{
                  title: 'Répartition des médailles par sport',
                  autosize: true
                }}
                useResizeHandler={true}
                style={{ width: '100%', height: '450px' }}
              />
            </div>

            <div className="sports-list">
              {topSports.map((sport, index) => (
                <div key={index} className="sport-item">
                  <div className="sport-rank">#{index + 1}</div>
                  <div className="sport-info">
                    <h4>{sport.sport}</h4>
                    <div className="sport-bar">
                      <div
                        className="sport-bar-fill"
                        style={{ width: `${sport.percentage}%` }}
                      ></div>
                    </div>
                    <p>{sport.medals} médailles ({sport.percentage}%)</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Host Countries */}
        <section className="section">
          <h2 className="section-title">Pays organisateurs</h2>
          <div className="hosts-grid">
            {hosts.map((host, index) => (
              <div key={index} className="host-card">
                <h3>{host.country}</h3>
                <div className="host-count">{host.count} JO organisés</div>
                <div className="host-cities">
                  {host.cities.map((city: string, i: number) => (
                    <span key={i} className="city-badge">{city}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Historic Events Verification */}
        <section className="section">
          <h2 className="section-title">Vérification des événements marquants</h2>
          <div className="events-list">
            {events.map((event) => (
              <div key={event.id} className="event-card">
                <div className="event-header">
                  <span className="event-year">{event.year}</span>
                  {event.verified && <span className="verified-badge">✓ Vérifié</span>}
                </div>
                <h4>{event.title}</h4>
                <p>{event.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Interactive Charts Section */}
        <section className="section">
          <h2 className="section-title">Analyses complémentaires</h2>
          <div className="grid grid-2">
            <div className="chart-container">
              <Plot
                data={[
                  {
                    x: hosts.map(h => h.country),
                    y: hosts.map(h => h.count),
                    type: 'bar',
                    marker: {
                      color: hosts.map(h => h.count),
                      colorscale: 'Blues'
                    }
                  }
                ]}
                layout={{
                  title: 'JO organisés par pays',
                  xaxis: { title: 'Pays' },
                  yaxis: { title: 'Nombre de JO' },
                  autosize: true
                }}
                useResizeHandler={true}
                style={{ width: '100%', height: '400px' }}
              />
            </div>

            <div className="chart-container">
              <Plot
                data={[
                  {
                    values: [248, 276, 316],
                    labels: ['Or', 'Argent', 'Bronze'],
                    type: 'pie',
                    marker: {
                      colors: ['#FFD700', '#C0C0C0', '#CD7F32']
                    },
                    hole: 0.4
                  }
                ]}
                layout={{
                  title: 'Répartition médailles France (Total)',
                  autosize: true
                }}
                useResizeHandler={true}
                style={{ width: '100%', height: '400px' }}
              />
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Statistics;
