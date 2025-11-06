import React, { useEffect, useState } from 'react';
import { getAthletesList } from '../../services/api';
import './athlete.css';

interface AthleteData {
  athlete_full_name: string;
  games_participations: number;
  athlete_year_birth: number;
}

export default function Athlete() {
  const [athletes, setAthletes] = useState<AthleteData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [yearBirthFilter, setYearBirthFilter] = useState('');
  const [gamesFilter, setGamesFilter] = useState('');
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    fetchAthletes();
  }, []);

  const fetchAthletes = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getAthletesList();
      setAthletes(response.data.data || []);
    } catch (err: any) {
      setError('Error loading athletes. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    try {
      const params: any = {};
      if (yearBirthFilter) params.year_birth = parseInt(yearBirthFilter);
      if (gamesFilter) params.games_participations = parseInt(gamesFilter);

      const response = await getAthletesList(params);
      setAthletes(response.data.data || []);
      setShowAll(false);
    } catch (err: any) {
      setError('Error loading athletes. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setYearBirthFilter('');
    setGamesFilter('');
    setShowAll(false);
    fetchAthletes();
  };

  const displayedAthletes = showAll ? athletes : athletes.slice(0, 20);

  const calculateAge = (yearBirth: number) => {
    return 2025 - yearBirth;
  };

  if (loading) {
    return (
      <div className="athlete-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading Athletes...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="athlete-container">
        <div className="error">
          <p>❌ {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="athlete-container">
      <h1>🏃 Olympic Athletes</h1>
      <p className="subtitle">Explore the profiles of Olympic athletes</p>

      {/* Filters Section */}
      <div className="filters-section">
        <h3>🔍 Filters</h3>
        <div className="search-filters">
          <div className="filter-group">
            <label htmlFor="yearBirth">Year of Birth</label>
            <input
              id="yearBirth"
              type="number"
              min="1900"
              max="2010"
              value={yearBirthFilter}
              onChange={(e) => setYearBirthFilter(e.target.value)}
              placeholder="e.g., 1990"
              className="filter-input"
            />
          </div>

          <div className="filter-group">
            <label htmlFor="games">Games Participations</label>
            <input
              id="games"
              type="number"
              min="1"
              max="10"
              value={gamesFilter}
              onChange={(e) => setGamesFilter(e.target.value)}
              placeholder="e.g., 3"
              className="filter-input"
            />
          </div>

          <div className="filter-buttons">
            <button onClick={handleSearch} className="search-btn">� Search</button>
            <button onClick={handleReset} className="reset-btn">🔄 Reset</button>
          </div>
        </div>
      </div>

      {/* Results Count */}
      <div className="results-count">
        <p>Showing {displayedAthletes.length} of {athletes.length} athletes</p>
      </div>

      {/* Athletes Grid */}
      <div className="athletes-grid">
        {displayedAthletes.map((athlete, index) => (
          <div key={index} className="athlete-card">
            <div className="athlete-icon">�</div>
            <h3>{athlete.athlete_full_name}</h3>
            <div className="athlete-info">
              <div className="info-item">
                <span className="label">Born:</span>
                <span className="value">{athlete.athlete_year_birth}</span>
              </div>
              <div className="info-item">
                <span className="label">Age:</span>
                <span className="value">{calculateAge(athlete.athlete_year_birth)} years</span>
              </div>
              <div className="info-item">
                <span className="label">Games:</span>
                <span className="value games-badge">{athlete.games_participations}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Show More Button */}
      {athletes.length > 20 && (
        <div className="show-more-container">
          <button 
            className="show-more-btn" 
            onClick={() => setShowAll(!showAll)}
          >
            {showAll ? '▲ Show Less' : `▼ Show More (${athletes.length - 20} more)`}
          </button>
        </div>
      )}
    </div>
  );
}
