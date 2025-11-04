import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { getParis2024Predictions, getAthletePredictions, getClustering, getModelsComparison } from '../../services/api';
import './Predictions.css';

interface CountryPrediction {
  rank: number;
  country: string;
  gold: number;
  silver: number;
  bronze: number;
  total: number;
}

interface AthletePrediction {
  name: string;
  sport: string;
  country: string;
  predictedMedal: string;
  probability: number;
  category: string;
}

const Predictions: React.FC = () => {
  const [predictions, setPredictions] = useState<any>(null);
  const [athletes, setAthletes] = useState<AthletePrediction[]>([]);
  const [clustering, setClustering] = useState<any>(null);
  const [models, setModels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      const [predRes, athRes, clusterRes, modelsRes] = await Promise.all([
        getParis2024Predictions(),
        getAthletePredictions(),
        getClustering(),
        getModelsComparison()
      ]);

      setPredictions(predRes.data);
      setAthletes(athRes.data);
      setClustering(clusterRes.data);
      setModels(modelsRes.data);
    } catch (error) {
      console.error('Error fetching predictions:', error);
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

  // Préparer les données pour le graphique Top 25
  const top25Countries = predictions?.top25.slice(0, 10).map((c: CountryPrediction) => c.country) || [];
  const top25Gold = predictions?.top25.slice(0, 10).map((c: CountryPrediction) => c.gold) || [];
  const top25Silver = predictions?.top25.slice(0, 10).map((c: CountryPrediction) => c.silver) || [];
  const top25Bronze = predictions?.top25.slice(0, 10).map((c: CountryPrediction) => c.bronze) || [];

  return (
    <div className="predictions-page fade-in">
      <div className="hero">
        <div className="container">
          <h1 className="hero-title">🤖 Prédictions Paris 2024</h1>
          <p className="hero-subtitle">
            Prédictions basées sur Machine Learning & Deep Learning
          </p>
        </div>
      </div>

      <div className="container">
        {/* France Prediction */}
        <section className="section">
          <h2 className="section-title">🇫🇷 Prédiction pour la France</h2>
          <div className="france-prediction-card">
            <div className="prediction-header">
              <h3>Classement prédit: #{predictions?.france.rank}</h3>
              <div className="confidence-badge">
                Confiance: {(predictions?.france.confidence * 100).toFixed(0)}%
              </div>
            </div>
            <div className="medals-prediction">
              <div className="medal-pred">
                <span className="medal-icon">🥇</span>
                <span className="medal-count">{predictions?.france.gold}</span>
                <span className="medal-label">Or</span>
              </div>
              <div className="medal-pred">
                <span className="medal-icon">🥈</span>
                <span className="medal-count">{predictions?.france.silver}</span>
                <span className="medal-label">Argent</span>
              </div>
              <div className="medal-pred">
                <span className="medal-icon">🥉</span>
                <span className="medal-count">{predictions?.france.bronze}</span>
                <span className="medal-label">Bronze</span>
              </div>
              <div className="medal-pred total">
                <span className="medal-icon">🏅</span>
                <span className="medal-count">{predictions?.france.total}</span>
                <span className="medal-label">Total</span>
              </div>
            </div>
            <div className="model-info">
              <p>Modèle utilisé: <strong>{predictions?.france.model}</strong></p>
              <p>Précision: <strong>{(predictions?.modelMetrics.accuracy * 100).toFixed(1)}%</strong></p>
            </div>
          </div>
        </section>

        {/* Top 25 Chart */}
        <section className="section">
          <h2 className="section-title">Top 10 des pays (Prédiction)</h2>
          <div className="chart-container">
            <Plot
              data={[
                {
                  x: top25Countries,
                  y: top25Gold,
                  name: 'Or',
                  type: 'bar',
                  marker: { color: '#FFD700' }
                },
                {
                  x: top25Countries,
                  y: top25Silver,
                  name: 'Argent',
                  type: 'bar',
                  marker: { color: '#C0C0C0' }
                },
                {
                  x: top25Countries,
                  y: top25Bronze,
                  name: 'Bronze',
                  type: 'bar',
                  marker: { color: '#CD7F32' }
                }
              ]}
              layout={{
                barmode: 'stack',
                title: 'Répartition des médailles prédites',
                xaxis: { title: 'Pays' },
                yaxis: { title: 'Nombre de médailles' },
                autosize: true
              }}
              useResizeHandler={true}
              style={{ width: '100%', height: '500px' }}
            />
          </div>
        </section>

        {/* Athletes Predictions */}
        <section className="section">
          <h2 className="section-title">Athlètes français susceptibles de médailler</h2>
          <div className="athletes-grid">
            {athletes.map((athlete, index) => (
              <div key={index} className="athlete-card">
                <div className={`medal-badge badge-${athlete.predictedMedal.toLowerCase()}`}>
                  {athlete.predictedMedal === 'Gold' && '🥇'}
                  {athlete.predictedMedal === 'Silver' && '🥈'}
                  {athlete.predictedMedal === 'Bronze' && '🥉'}
                </div>
                <h3>{athlete.name}</h3>
                <p className="sport">{athlete.sport}</p>
                <p className="category">{athlete.category}</p>
                <div className="probability-bar">
                  <div 
                    className="probability-fill" 
                    style={{ width: `${athlete.probability * 100}%` }}
                  ></div>
                </div>
                <p className="probability-text">
                  Probabilité: {(athlete.probability * 100).toFixed(0)}%
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Models Comparison */}
        <section className="section">
          <h2 className="section-title">Comparaison des modèles IA</h2>
          <div className="models-table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Modèle</th>
                  <th>Type</th>
                  <th>Précision</th>
                  <th>RMSE</th>
                  <th>Temps d'entraînement</th>
                  <th>Sélectionné</th>
                </tr>
              </thead>
              <tbody>
                {models.map((model, index) => (
                  <tr key={index} className={model.selected ? 'selected-row' : ''}>
                    <td><strong>{model.name}</strong></td>
                    <td>
                      <span className={`badge ${model.type === 'Machine Learning' ? 'badge-ml' : 'badge-dl'}`}>
                        {model.type}
                      </span>
                    </td>
                    <td>{(model.accuracy * 100).toFixed(1)}%</td>
                    <td>{model.rmse}</td>
                    <td>{model.trainTime}</td>
                    <td>
                      {model.selected ? '✅' : ''}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Clustering */}
        <section className="section">
          <h2 className="section-title">Clustering des pays</h2>
          <p className="text-center mb-4">
            Nombre optimal de clusters: <strong>{clustering?.optimalK}</strong> | 
            Silhouette Score: <strong>{clustering?.silhouetteScore}</strong>
          </p>
          <div className="clusters-grid">
            {clustering?.clusters.map((cluster: any) => (
              <div key={cluster.id} className="cluster-card">
                <h3>{cluster.name}</h3>
                <p className="cluster-avg">
                  Moyenne: {cluster.avgMedals} médailles
                </p>
                <div className="cluster-countries">
                  {cluster.countries.slice(0, 5).join(', ')}
                  {cluster.countries.length > 5 && '...'}
                </div>
                <p className="cluster-characteristics">
                  {cluster.characteristics}
                </p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default Predictions;
