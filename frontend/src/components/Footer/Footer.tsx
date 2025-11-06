import React from 'react';
import './Footer.css';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>Olympics Analytics</h3>
            <p>120 ans d'histoire olympique analysés et prédits par l'IA</p>
          </div>

          <div className="footer-section">
            <h4>Navigation</h4>
            <ul>
              <li><a href="/">Accueil</a></li>
              <li><a href="/statistics">Statistiques</a></li>
              <li><a href="/predictions">Prédictions</a></li>
              <li><a href="/france">France</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Technologies</h4>
            <ul>
              <li>React + TypeScript</li>
              <li>Flask</li>
              <li>Plotly.js</li>
              <li>Machine Learning</li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Sources</h4>
            <ul>
              <li><a href="https://olympics.com" target="_blank" rel="noopener noreferrer">Olympics.com</a></li>
              <li><a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a></li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; {currentYear} Olympics Analytics - Hackathon Project</p>
          <p>Données historiques 1896-2022 | Prédictions Paris 2024</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
