import React, { useEffect, useState } from 'react';
import { getResults } from '../../services/api';
import './Result.css';

interface ResultData {
  country_name: string;
  discipline_title: string;
  medal_type: string;
  slug_game: string;
  event_title: string;
}

export default function Result() {
  const [results, setResults] = useState<ResultData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [countryFilter, setCountryFilter] = useState('');
  const [gameFilter, setGameFilter] = useState('');
  const [medalFilter, setMedalFilter] = useState('all');
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getResults();
      setResults(response.data.data || []);
    } catch (err: any) {
      setError('Error loading results. Please try again.');
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
      if (countryFilter) params.country = countryFilter;
      if (gameFilter) params.game = gameFilter;
      
      const response = await getResults(params);
      setResults(response.data.data || []);
      setShowAll(false);
    } catch (err: any) {
      setError('Error loading results. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setCountryFilter('');
    setGameFilter('');
    setMedalFilter('all');
    setShowAll(false);
    fetchResults();
  };

  const filteredResults = medalFilter === 'all' 
    ? results 
    : results.filter(result => result.medal_type === medalFilter);

  const displayedResults = showAll ? filteredResults : filteredResults.slice(0, 20);

  const getMedalColor = (type: string | null) => {
    if (!type) return '';
    switch (type.toUpperCase()) {
      case 'GOLD': return 'gold-medal';
      case 'SILVER': return 'silver-medal';
      case 'BRONZE': return 'bronze-medal';
      default: return '';
    }
  };

  if (loading) {
    return (
      <div className="result-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading Olympic Results...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="result-container">
        <div className="error">
          <p>❌ {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="result-container">
      <h1>Olympic Results</h1>

      {/* Filters Section */}
      <div className="filters-section">
        <div className="search-filters">
          <input
            type="text"
            placeholder="Search by country..."
            value={countryFilter}
            onChange={(e) => setCountryFilter(e.target.value)}
            className="filter-input"
          />
          <input
            type="text"
            placeholder="Search by game (e.g., paris-2024)..."
            value={gameFilter}
            onChange={(e) => setGameFilter(e.target.value)}
            className="filter-input"
          />
          <button onClick={handleSearch} className="search-btn">🔍 Search</button>
          <button onClick={handleReset} className="reset-btn">🔄 Reset</button>
        </div>

        <div className="medal-filters">
          <button 
            className={medalFilter === 'all' ? 'active' : ''} 
            onClick={() => setMedalFilter('all')}
          >
            All Medals
          </button>
          <button 
            className={medalFilter === 'GOLD' ? 'active gold-btn' : 'gold-btn'} 
            onClick={() => setMedalFilter('GOLD')}
          >
            🥇 Gold
          </button>
          <button 
            className={medalFilter === 'SILVER' ? 'active silver-btn' : 'silver-btn'} 
            onClick={() => setMedalFilter('SILVER')}
          >
            🥈 Silver
          </button>
          <button 
            className={medalFilter === 'BRONZE' ? 'active bronze-btn' : 'bronze-btn'} 
            onClick={() => setMedalFilter('BRONZE')}
          >
            🥉 Bronze
          </button>
        </div>
      </div>

      {/* Results Count */}
      <div className="results-count">
        <p>Showing {displayedResults.length} of {filteredResults.length} results</p>
      </div>

      {/* Results Table */}
      <div className="table-container">
        <table className="results-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Country</th>
              <th>Event</th>
              <th>Discipline</th>
              <th>Game</th>
              <th>Medal</th>
            </tr>
          </thead>
          <tbody>
            {displayedResults.map((result, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td className="country-cell">{result.country_name || 'N/A'}</td>
                <td className="event-cell">{result.event_title || 'N/A'}</td>
                <td>{result.discipline_title || 'N/A'}</td>
                <td className="game-cell">{result.slug_game || 'N/A'}</td>
                <td>
                  <span className={`medal-badge ${getMedalColor(result.medal_type)}`}>
                    {result.medal_type || 'N/A'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Show More Button */}
      {filteredResults.length > 20 && (
        <div className="show-more-container">
          <button 
            className="show-more-btn" 
            onClick={() => setShowAll(!showAll)}
          >
            {showAll ? '▲ Show Less' : `▼ Show More (${filteredResults.length - 20} more)`}
          </button>
        </div>
      )}
    </div>
  );
}
