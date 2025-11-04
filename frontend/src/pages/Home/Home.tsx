import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getOverviewStats } from '../../services/api';
import './Home.css';

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
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await getOverviewStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-page fade-in">
      {/* Hero Section */}
      <section className="hero-modern">
        <div className="hero-overlay"></div>
        <div className="container">
          <div className="hero-content">
            <img 
              src="/images/olympic-rings.png" 
              alt="Olympic Rings" 
              className="olympic-rings-image pulse"
            />
            <h1 className="hero-title-modern">RACE TO THE FINISH LINE</h1>
            <div className="hero-subtitle-modern">
              Olympic Data Analysis & Machine Learning Predictions
            </div>
            <p className="hero-dates-modern">
              Athens 1896 → Paris 2024 → LA 2028
            </p>
          </div>
          <div className="scroll-indicator">
            <span>↓</span>
          </div>
        </div>
      </section>

      {/* Project Objectives Section */}
      <section className="objectives-section">
        <div className="container">
          <h2 className="section-title-modern">PROJECT OBJECTIVES</h2>
          <div className="objectives-grid">
            <div className="objective-card">
              <div className="objective-number">1</div>
              <h3>Analyze Historical Data</h3>
              <p>
                Explore 120+ years of Olympic history (1896-2024) to uncover which countries 
                dominate over time, by season, and by sport. Visualize trends in medal counts, 
                athlete performance, and sport popularity.
              </p>
            </div>
            <div className="objective-card">
              <div className="objective-number">2</div>
              <h3>Machine Learning Predictions</h3>
              <p>
                Utilize advanced ML models (Linear Regression, Random Forest, Neural Networks) 
                to predict medal counts for Paris 2024. Analyze factors like GDP, population, 
                and historical performance.
              </p>
            </div>
            <div className="objective-card">
              <div className="objective-number">3</div>
              <h3>Interactive Visualizations</h3>
              <p>
                Create dynamic charts and graphs using Plotly.js to provide insights into 
                Olympic trends, country comparisons, and sport-specific analytics with 
                real-time data exploration.
              </p>
            </div>
          </div>
        </div>
      </section>

      <div className="container">
        {/* Stats Overview */}
        {loading ? (
          <div className="loading">
            <div className="spinner"></div>
          </div>
        ) : (
          <section className="section">
            <div className="stats-grid-modern">
              <div className="stat-card-modern">
                <div className="stat-icon">🏅</div>
                <div className="stat-value">{stats?.totalMedals.toLocaleString()}</div>
                <div className="stat-label">Total Medals</div>
              </div>
              <div className="stat-card-modern">
                <div className="stat-icon">👥</div>
                <div className="stat-value">{stats?.totalAthletes.toLocaleString()}</div>
                <div className="stat-label">Athletes</div>
              </div>
              <div className="stat-card-modern">
                <div className="stat-icon">🌍</div>
                <div className="stat-value">{stats?.totalCountries}</div>
                <div className="stat-label">Countries</div>
              </div>
              <div className="stat-card-modern">
                <div className="stat-icon">🎯</div>
                <div className="stat-value">{stats?.totalEvents.toLocaleString()}</div>
                <div className="stat-label">Events</div>
              </div>
            </div>
          </section>
        )}

        {/* Features Section */}
        <section className="features-section-modern">
          <h2 className="section-title-modern">EXPLORE THE DATA</h2>
          <div className="features-grid">
            <Link to="/statistics" className="feature-card-modern">
              <div className="feature-icon-modern">📊</div>
              <h3>STATISTICS</h3>
              <p>Dive into 120 years of Olympic data with interactive visualizations and insights</p>
              <span className="feature-link-modern">EXPLORE →</span>
            </Link>

            <Link to="/predictions" className="feature-card-modern">
              <div className="feature-icon-modern">🤖</div>
              <h3>ML PREDICTIONS</h3>
              <p>AI-powered predictions for Paris 2024 Olympics using advanced machine learning models</p>
              <span className="feature-link-modern">VIEW PREDICTIONS →</span>
            </Link>

            <Link to="/france" className="feature-card-modern">
              <div className="feature-icon-modern">🇫🇷</div>
              <h3>FRANCE ANALYSIS</h3>
              <p>Comprehensive analysis of France's Olympic performance through history</p>
              <span className="feature-link-modern">DISCOVER →</span>
            </Link>
          </div>
        </section>

        {/* Team Section */}
        <section className="team-section">
          <h2 className="section-title-modern">THE TEAM</h2>
          <div className="team-grid">
            <div className="team-member">
              <div className="member-avatar">👨‍💻</div>
              <h3>Data Scientist</h3>
              <p>Machine Learning & Predictions</p>
            </div>
            <div className="team-member">
              <div className="member-avatar">👩‍💻</div>
              <h3>Frontend Developer</h3>
              <p>UI/UX & Visualizations</p>
            </div>
            <div className="team-member">
              <div className="member-avatar">👨‍💼</div>
              <h3>Backend Developer</h3>
              <p>API & Database</p>
            </div>
            <div className="team-member">
              <div className="member-avatar">👩‍🔬</div>
              <h3>Data Analyst</h3>
              <p>Statistics & Insights</p>
            </div>
          </div>
        </section>

        {/* Key Takeaways Section */}
        <section className="takeaways-section">
          <h2 className="section-title-modern">KEY TAKEAWAYS</h2>
          <div className="takeaways-grid">
            <div className="takeaway-card success">
              <h3>🎯 WHAT WENT WELL</h3>
              <ul>
                <li>Interactive visualizations with Plotly.js</li>
                <li>Real-time data updates via RESTful API</li>
                <li>Responsive design for all devices</li>
                <li>Advanced ML models for predictions</li>
                <li>Clean and modern UI/UX</li>
              </ul>
            </div>
            <div className="takeaway-card challenge">
              <h3>💪 CHALLENGES WE OVERCAME</h3>
              <ul>
                <li>Implementing complex ML algorithms</li>
                <li>Optimizing large dataset queries</li>
                <li>Cross-browser compatibility</li>
                <li>TypeScript integration with React</li>
                <li>Performance optimization for charts</li>
              </ul>
            </div>
          </div>
          <div className="tech-stack">
            <h3>TECHNOLOGIES USED</h3>
            <div className="tech-badges">
              <span className="badge">React</span>
              <span className="badge">TypeScript</span>
              <span className="badge">Plotly.js</span>
              <span className="badge">Node.js</span>
              <span className="badge">Express</span>
              <span className="badge">MySQL</span>
              <span className="badge">Machine Learning</span>
              <span className="badge">Python</span>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Home;
