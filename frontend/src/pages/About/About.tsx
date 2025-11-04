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
                    <li>Plotly.js (visualisations)</li>
                    <li>CSS3 (Responsive Design)</li>
                  </ul>
                </div>
                <div className="tech-card">
                  <h3>Backend</h3>
                  <ul>
                    <li>Node.js</li>
                    <li>Express.js</li>
                    <li>REST API</li>
                    <li>CORS & dotenv</li>
                  </ul>
                </div>
                <div className="tech-card">
                  <h3>Base de données</h3>
                  <ul>
                    <li>MySQL / MariaDB</li>
                    <li>PostgreSQL</li>
                    <li>Support multi-SGBD</li>
                  </ul>
                </div>
                <div className="tech-card">
                  <h3>Intelligence Artificielle</h3>
                  <ul>
                    <li>Python - Pandas / Spark</li>
                    <li>Scikit-learn (ML)</li>
                    <li>TensorFlow (DL)</li>
                    <li>GridSearch, métriques</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="about-section">
              <h2>🤖 Modèles d'IA développés</h2>
              <div className="models-info">
                <div className="model-category">
                  <h4>Machine Learning (M1)</h4>
                  <ul>
                    <li>Random Forest</li>
                    <li>Decision Tree</li>
                    <li>Support Vector Machine (SVM)</li>
                  </ul>
                </div>
                <div className="model-category">
                  <h4>Deep Learning (M2)</h4>
                  <ul>
                    <li>Convolutional Neural Networks (CNN)</li>
                    <li>Long Short-Term Memory (LSTM)</li>
                  </ul>
                </div>
              </div>
              <p className="model-note">
                Les modèles ont été optimisés avec GridSearch et évalués sur plusieurs 
                métriques (accuracy, RMSE, confusion matrix).
              </p>
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
                Ce projet a été réalisé en collaboration entre étudiants M1 et M2, 
                chacun apportant son expertise :
              </p>
              <ul className="team-list">
                <li>🎓 <strong>M1</strong> : Base de données, Pandas, Machine Learning</li>
                <li>🎓 <strong>M2</strong> : Spark, Deep Learning, Architecture avancée</li>
                <li>🤝 Collaboration étroite et comparaison des résultats</li>
                <li>📋 Gestion de projet via Trello</li>
              </ul>
            </div>

            <div className="about-section cta-section">
              <h2>🔗 Ressources</h2>
              <div className="resources-links">
                <a href="https://github.com" className="resource-btn" target="_blank" rel="noopener noreferrer">
                  <span>💻</span> GitHub Repository
                </a>
                <a href="https://olympics.com" className="resource-btn" target="_blank" rel="noopener noreferrer">
                  <span>🏅</span> Olympics.com
                </a>
                <button className="resource-btn" onClick={() => alert('Dataset disponible prochainement')}>
                  <span>📊</span> Dataset
                </button>
                <button className="resource-btn" onClick={() => alert('Documentation en cours de rédaction')}>
                  <span>📝</span> Documentation
                </button>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default About;
