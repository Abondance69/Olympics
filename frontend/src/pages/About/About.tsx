import React from 'react';
import './About.css';

const About: React.FC = () => {
  return (
    <div className="about-page fade-in">
      <div className="hero">
        <div className="container">
          <h1 className="hero-title">À propos du projet</h1>
          <p className="hero-subtitle">
            Hackathon - 120 ans d'histoire olympique
          </p>
        </div>
      </div>

      <div className="container">
        <section className="section">
          <div className="about-content">
            <div className="about-section">
              <h2>🎯 Objectif du projet</h2>
              <p>
                Ce projet a été développé dans le cadre d'un hackathon visant à analyser
                120 ans d'histoire olympique (1896-2022) et à prédire les résultats des
                Jeux Olympiques de Paris 2024 en utilisant l'Intelligence Artificielle.
              </p>
            </div>

            <div className="about-section">
              <h2>📊 Données utilisées</h2>
              <ul className="feature-list">
                <li>✅ +21,000 médailles décernées</li>
                <li>✅ +162,000 résultats d'épreuves</li>
                <li>✅ +74,000 athlètes participants</li>
                <li>✅ 53 pays hôtes</li>
                <li>✅ Données scrapées depuis olympics.com</li>
              </ul>
            </div>

            <div className="about-section">
              <h2>🛠️ Technologies utilisées</h2>
              <div className="tech-grid">
                <div className="tech-card">
                  <h3>Frontend</h3>
                  <ul>
                    <li>React 18</li>
                    <li>TypeScript</li>
                    <li>CSS3 (Responsive Design)</li>
                  </ul>
                </div>
                <div className="tech-card">
                  <h3>Backend</h3>
                  <ul>
                    <li>Flask</li>
                    <li>REST API</li>
                    <li>CORS</li>
                  </ul>
                </div>
                <div className="tech-card">
                  <h3>Base de données</h3>
                  <ul>
                    <li>MySQL</li>
                    <li>Support multi-SGBD</li>
                  </ul>
                </div>
                <div className="tech-card">
                  <h3>Intelligence Artificielle</h3>
                  <ul>
                    <li>Python</li>
                    <li>Scikit-learn</li>
                    <li>Pandas</li>
                  </ul>
                </div>
              </div>
            </div>


            <div className="about-section">
              <h2>📈 Fonctionnalités principales</h2>
              <div className="features-grid">
                <div className="feature-item">
                  <span className="feature-icon">📊</span>
                  <div>
                    <h4>Statistiques interactives</h4>
                    <p>Exploration de 120 ans de données olympiques avec graphiques Plotly</p>
                  </div>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">🤖</span>
                  <div>
                    <h4>Prédictions IA</h4>
                    <p>Prédictions Paris 2024 basées sur ML/DL pour pays et athlètes</p>
                  </div>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">🇫🇷</span>
                  <div>
                    <h4>Focus France</h4>
                    <p>Analyse détaillée des performances françaises aux JO</p>
                  </div>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">📱</span>
                  <div>
                    <h4>Design Responsive</h4>
                    <p>Interface adaptée mobile, tablette et desktop</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="about-section">
              <h2>👥 Équipe & Méthodologie</h2>
              <p>
                Ce projet a été réalisé en collaboration entre étudiants de M1 et M2,
                chacun apportant son expertise en <strong>data science</strong>,
                <strong>développement web</strong> et <strong>analyse prédictive</strong>.
              </p>
              <ul className="team-list">
                <li>🤝 Collaboration étroite et comparaison des résultats entre les membres.</li>
                <li>📋 Gestion du projet via Trello et GitHub (suivi agile des tâches).</li>
                <li>🚀 Intégration continue entre le backend Flask et le frontend React.</li>
                <li>📊 Analyse collective des performances et interprétation des résultats.</li>
              </ul>
            </div>

            <div className="about-section cta-section">
              <h2>🔗 Ressources</h2>
              <div className="resources-links">
                <a href="https://github.com/Abondance69/Olympics" className="resource-btn" target="_blank" rel="noopener noreferrer">
                  <span>💻</span> GitHub Repository
                </a>
                <a href="https://olympics.com" className="resource-btn" target="_blank" rel="noopener noreferrer">
                  <span>🏅</span> Olympics.com
                </a>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default About;
