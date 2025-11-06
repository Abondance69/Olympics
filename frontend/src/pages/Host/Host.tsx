import React, { useEffect, useState } from 'react';
import { getGames, getCountriesClusters } from '../../services/api';
import './Host.css';

export default function Host() {
  const [games, setGames] = useState([]);
  const [clusters, setClusters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [seasonFilter, setSeasonFilter] = useState('all');
  const [showAllGames, setShowAllGames] = useState(false);
  const [showAllClusters, setShowAllClusters] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [gamesRes, clustersRes] = await Promise.all([
          getGames(),
          getCountriesClusters()
        ]);
        setGames(gamesRes.data.data || []);
        setClusters(clustersRes.data.data || []);
      } catch (err) {
        setError('Error loading data. Please try again.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const filteredGames = seasonFilter === 'all' 
    ? games 
    : games.filter(game => game.game_season === seasonFilter);

  const displayedGames = showAllGames ? filteredGames : filteredGames.slice(0, 8);
  const displayedClusters = showAllClusters ? clusters : clusters.slice(0, 8);

  if (loading) {
    return (
      <div className="host-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading Olympic data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="host-container">
        <div className="error">
          <p>❌ {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="host-container">
      <h1>Olympic Games & Host Cities</h1>
      
      <section className="games-section">
        <div className="section-header">
          <h2>Games ({filteredGames.length})</h2>
          <div className="filter-buttons">
            <button 
              className={seasonFilter === 'all' ? 'active' : ''} 
              onClick={() => setSeasonFilter('all')}
            >
              All
            </button>
            <button 
              className={seasonFilter === 'Summer' ? 'active' : ''} 
              onClick={() => setSeasonFilter('Summer')}
            >
              ☀️ Summer
            </button>
            <button 
              className={seasonFilter === 'Winter' ? 'active' : ''} 
              onClick={() => setSeasonFilter('Winter')}
            >
              ❄️ Winter
            </button>
          </div>
        </div>
        <div className="games-grid">
          {displayedGames.map((game, index) => (
            <div key={index} className="game-card">
              <h3>{game.game_name}</h3>
              <p><strong>Year:</strong> {game.game_year}</p>
              <p><strong>Season:</strong> {game.game_season}</p>
              <p><strong>Location:</strong> {game.game_location}</p>
            </div>
          ))}
        </div>
        {filteredGames.length > 8 && (
          <div className="show-more-container">
            <button 
              className="show-more-btn" 
              onClick={() => setShowAllGames(!showAllGames)}
            >
              {showAllGames ? '▲ Show Less' : `▼ Show More (${filteredGames.length - 8} more)`}
            </button>
          </div>
        )}
      </section>

      <section className="clusters-section">
        <h2>Countries Clusters ({clusters.length})</h2>
        <div className="table-container">
          <table className="clusters-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Country</th>
                <th>Cluster</th>
                <th>Total Medals</th>
              </tr>
            </thead>
            <tbody>
              {displayedClusters.map((cluster, index) => (
                <tr key={index}>
                  <td>{index + 1}</td>
                  <td className="country-name">{cluster.country_name}</td>
                  <td>
                    <span className={`cluster-badge cluster-${cluster.cluster}`}>
                      Cluster {cluster.cluster}
                    </span>
                  </td>
                  <td className="medals-count">{cluster.total_medals}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {clusters.length > 8 && (
          <div className="show-more-container">
            <button 
              className="show-more-btn" 
              onClick={() => setShowAllClusters(!showAllClusters)}
            >
              {showAllClusters ? '▲ Show Less' : `▼ Show More (${clusters.length - 8} more)`}
            </button>
          </div>
        )}
      </section>
    </div>
  );
}
