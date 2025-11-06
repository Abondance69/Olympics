import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "./Home.css";
import { apiUrl } from "data";

interface OverviewStats {
  totalMedals: number;
  totalAthletes: number;
  totalCountries: number;
  totalEvents: number;
}

const Home: React.FC = () => {
  const [stats, setStats] = useState<OverviewStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axios.get(`${apiUrl}/overview`);
        const randomStats = {
          totalMedals: response?.data?.totalMedals || 0,
          totalAthletes: response?.data?.totalAthletes || 0,
          totalCountries: response?.data?.totalCountries || 0,
          totalEvents: response?.data?.totalEvents || 0,
        };
        setStats(randomStats);
      } catch (error) {
        console.error("Erreur lors du chargement :", error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="home-page fade-in">
      {/* ===== HERO ===== */}
      <section className="hero-modern">
        <div className="hero-overlay"></div>
        <div className="container">
          <div className="hero-content">
            <img
              src="/images/olympic-rings.png"
              alt="Olympic Rings"
              className="olympic-rings-image"
            />
            <h1 className="hero-title-modern">OLYMPICS ANALYTICS</h1>
            <p className="hero-subtitle-modern">
              Explore. Predict. Visualize the legacy of the Olympic Games.
            </p>
            <div className="hero-buttons">
              <Link to="/statistics" className="btn-primary">
                📊 Explore Data
              </Link>
              <Link to="/predictions" className="btn-secondary">
                🔮 Try Predictions
              </Link>
            </div>
          </div>
          <div className="scroll-indicator">↓</div>
        </div>
      </section>

      {/* ===== KEY METRICS ===== */}
      <section className="stats-section">
        <div className="container">
          <h2 className="section-title-modern">GLOBAL OLYMPIC SNAPSHOT</h2>
          {loading ? (
            <div className="loading">
              <div className="spinner"></div>
            </div>
          ) : (
            <div className="stats-grid-modern">
              <div className="stat-card-modern">
                <div className="stat-icon">🏅</div>
                <div className="stat-value">
                  {stats?.totalMedals.toLocaleString()}
                </div>
                <div className="stat-label">Medals</div>
              </div>
              <div className="stat-card-modern">
                <div className="stat-icon">👥</div>
                <div className="stat-value">
                  {stats?.totalAthletes.toLocaleString()}
                </div>
                <div className="stat-label">Athletes</div>
              </div>
              <div className="stat-card-modern">
                <div className="stat-icon">🌍</div>
                <div className="stat-value">{stats?.totalCountries}</div>
                <div className="stat-label">Countries</div>
              </div>
              <div className="stat-card-modern">
                <div className="stat-icon">🎯</div>
                <div className="stat-value">
                  {stats?.totalEvents.toLocaleString()}
                </div>
                <div className="stat-label">Events</div>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* ===== PROJECT GOALS ===== */}
      <section className="objectives-section">
        <div className="container">
          <h2 className="section-title-modern">PROJECT OBJECTIVES</h2>
          <div className="objectives-grid">
            <div className="objective-card">
              <div className="objective-number">1</div>
              <h3>Analyze Olympic History</h3>
              <p>
                Dive into more than 120 years of Olympic data and visualize
                patterns of success, diversity, and evolution across nations and
                sports.
              </p>
            </div>
            <div className="objective-card">
              <div className="objective-number">2</div>
              <h3>Predict Future Outcomes</h3>
              <p>
                Harness machine learning to forecast medal counts for upcoming
                Olympics using trends, population, and economic indicators.
              </p>
            </div>
            <div className="objective-card">
              <div className="objective-number">3</div>
              <h3>Interactive Data Stories</h3>
              <p>
                Present complex Olympic insights through modern, interactive,
                and accessible visualizations powered by Plotly and React.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ===== FEATURE NAVIGATION ===== */}
      <section className="features-section-modern">
        <div className="container">
          <h2 className="section-title-modern">EXPLORE OUR MODULES</h2>
          <div className="features-grid">
            <Link to="/statistics" className="feature-card-modern">
              <div className="feature-icon-modern">📊</div>
              <h3>Statistics</h3>
              <p>Visualize global Olympic trends and performance data.</p>
              <span className="feature-link-modern">Explore →</span>
            </Link>
            <Link to="/predictions" className="feature-card-modern">
              <div className="feature-icon-modern">🤖</div>
              <h3>Predictions</h3>
              <p>Discover medal forecasts powered by our AI models.</p>
              <span className="feature-link-modern">Predict →</span>
            </Link>
          </div>
        </div>
      </section>

      {/* ===== CTA ===== */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-card">
            <h2>Ready to Explore the Data?</h2>
            <p>
              Enter the world of Olympic analytics — discover, predict, and
              visualize greatness.
            </p>
            <div className="cta-buttons">
              <Link to="/statistics" className="btn-primary">
                Start Exploring
              </Link>
              <Link to="/predictions" className="btn-secondary">
                Predict Now
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
