import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { getFranceStats, getMedalsByYear } from '../../services/api';
import './France.css';

const France: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [medalsByYear, setMedalsByYear] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, medalsRes] = await Promise.all([
        getFranceStats(),
        getMedalsByYear('FRA')
      ]);

      setStats(statsRes.data);
      setMedalsByYear(medalsRes.data);
    } catch (error) {
      console.error('Error fetching France data:', error);
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

  const years = medalsByYear.map(d => d.year);
  const totalMedals = medalsByYear.map(d => d.gold + d.silver + d.bronze);

  return (
    <div className="france-page fade-in">
      <div className="hero hero-france">
        <div className="container">
          <h1 className="hero-title">🇫🇷 La France aux Jeux Olympiques</h1>
          <p className="hero-subtitle">
            Performance, histoire et excellence sportive
          </p>
        </div>
      </div>

      <div className="container">
        {/* Medal Stats */}
        <section className="section">
          <h2 className="section-title">Bilan des médailles</h2>
          <div className="stats-grid">
            <div className="stat-card stat-total">
              <div className="stat-icon">🏅</div>
              <div className="stat-value">{stats?.totalMedals}</div>
              <div className="stat-label">Total</div>
            </div>
            <div className="stat-card stat-gold">
              <div className="stat-icon">🥇</div>
              <div className="stat-value">{stats?.gold}</div>
              <div className="stat-label">Or</div>
            </div>
            <div className="stat-card stat-silver">
              <div className="stat-icon">🥈</div>
              <div className="stat-value">{stats?.silver}</div>
              <div className="stat-label">Argent</div>
            </div>
            <div className="stat-card stat-bronze">
              <div className="stat-icon">🥉</div>
              <div className="stat-value">{stats?.bronze}</div>
              <div className="stat-label">Bronze</div>
            </div>
          </div>
        </section>

        {/* Best/Worst Performance */}
        <section className="section">
          <h2 className="section-title">Performance aux JO</h2>
          <div className="grid grid-2">
            <div className="performance-card best">
              <h3>🏆 Meilleure performance</h3>
              <div className="performance-content">
                <div className="performance-year">{stats?.bestYear.year}</div>
                <div className="performance-medals">{stats?.bestYear.medals} médailles</div>
                <p>Année exceptionnelle pour la délégation française</p>
              </div>
            </div>
            <div className="performance-card worst">
              <h3>📉 Performance la plus faible</h3>
              <div className="performance-content">
                <div className="performance-year">{stats?.worstYear.year}</div>
                <div className="performance-medals">{stats?.worstYear.medals} médailles</div>
                <p>La France n'a pas participé ou envoyé une petite délégation</p>
              </div>
            </div>
          </div>
        </section>

        {/* Evolution Chart */}
        <section className="section">
          <h2 className="section-title">Évolution du nombre total de médailles</h2>
          <div className="chart-container">
            <Plot
              data={[
                {
                  x: years,
                  y: totalMedals,
                  type: 'scatter',
                  mode: 'lines+markers',
                  fill: 'tozeroy',
                  line: { color: '#0066cc', width: 3 },
                  marker: { size: 8, color: '#0066cc' }
                }
              ]}
              layout={{
                title: 'Médailles totales par édition des JO',
                xaxis: { title: 'Année' },
                yaxis: { title: 'Nombre total de médailles' },
                autosize: true,
                hovermode: 'x'
              }}
              useResizeHandler={true}
              style={{ width: '100%', height: '500px' }}
            />
          </div>
        </section>

        {/* French Hosting */}
        <section className="section">
          <h2 className="section-title">JO organisés par la France</h2>
          <div className="hosting-grid">
            <div className="hosting-card">
              <div className="hosting-year">1900</div>
              <h4>Paris - Été</h4>
              <p>Première édition parisienne, participation féminine inaugurale</p>
            </div>
            <div className="hosting-card">
              <div className="hosting-year">1924</div>
              <h4>Paris - Été</h4>
              <p>Deuxième édition parisienne, année olympique historique</p>
            </div>
            <div className="hosting-card">
              <div className="hosting-year">1924</div>
              <h4>Chamonix - Hiver</h4>
              <p>Naissance des Jeux Olympiques d'hiver</p>
            </div>
            <div className="hosting-card">
              <div className="hosting-year">1968</div>
              <h4>Grenoble - Hiver</h4>
              <p>JO d'hiver modernes et innovants</p>
            </div>
            <div className="hosting-card">
              <div className="hosting-year">1992</div>
              <h4>Albertville - Hiver</h4>
              <p>Derniers JO d'hiver organisés la même année que les JO d'été</p>
            </div>
            <div className="hosting-card active">
              <div className="hosting-year">2024</div>
              <h4>Paris - Été</h4>
              <p>🔥 Édition actuelle - 3ème fois à Paris</p>
            </div>
          </div>
        </section>

        {/* Sports Excellence */}
        <section className="section">
          <h2 className="section-title">Sports d'excellence</h2>
          <p className="section-subtitle">
            Disciplines où la France excelle historiquement
          </p>
          <div className="sports-excellence-grid">
            <div className="excellence-card">
              <div className="sport-emoji">🤺</div>
              <h4>Escrime</h4>
              <p className="medal-count">118 médailles</p>
              <p className="description">Domination historique mondiale</p>
            </div>
            <div className="excellence-card">
              <div className="sport-emoji">🚴</div>
              <h4>Cyclisme</h4>
              <p className="medal-count">92 médailles</p>
              <p className="description">Excellence en piste et route</p>
            </div>
            <div className="excellence-card">
              <div className="sport-emoji">🏃</div>
              <h4>Athlétisme</h4>
              <p className="medal-count">88 médailles</p>
              <p className="description">Performances régulières</p>
            </div>
            <div className="excellence-card">
              <div className="sport-emoji">🥋</div>
              <h4>Judo</h4>
              <p className="medal-count">55 médailles</p>
              <p className="description">Puissance moderne</p>
            </div>
          </div>
        </section>

        {/* Fun Facts */}
        <section className="section">
          <h2 className="section-title">Le saviez-vous ?</h2>
          <div className="fun-facts-grid">
            <div className="fact-card">
              <div className="fact-icon">🎯</div>
              <p>La France est le 2ème pays à avoir organisé le plus de JO après les USA</p>
            </div>
            <div className="fact-card">
              <div className="fact-icon">❄️</div>
              <p>Les JO d'hiver sont nés à Chamonix en 1924</p>
            </div>
            <div className="fact-card">
              <div className="fact-icon">👩</div>
              <p>Paris 1900 : premières femmes aux JO</p>
            </div>
            <div className="fact-card">
              <div className="fact-icon">🏅</div>
              <p>L'escrime est le sport français par excellence</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default France;
