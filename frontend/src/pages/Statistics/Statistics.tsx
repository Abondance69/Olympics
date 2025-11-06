import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";
import "./Statistics.css";

// -------------------------------
// 🧩 Types
// -------------------------------
interface Result {
  country_name: string;
  discipline_title: string;
  medal_type: string;
  slug_game: string;
  event_title: string;
}

interface Cluster {
  country_name: string;
  total_medals: number;
  game_year: number;
  season_encoded: number;
  cluster: number;
}

interface Game {
  game_name: string;
  game_year: number;
  game_season: string;
  game_location: string;
}

interface Metrics {
  status: string;
  country_medals: Record<string, any>;
  athlete: Record<string, any>;
}

// -------------------------------
// 📊 Composant principal
// -------------------------------
const Statistics: React.FC = () => {
  const [results, setResults] = useState<Result[]>([]);
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const [games, setGames] = useState<Game[]>([]);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [resResults, resClusters, resGames, resMetrics] = await Promise.all([
          axios.get("http://localhost:8000/api/results"),
          axios.get("http://localhost:8000/api/countries/clusters"),
          axios.get("http://localhost:8000/api/games"),
          axios.get("http://localhost:8000/api/metrics"),
        ]);

        setResults(resResults.data.data || []);
        setClusters(resClusters.data.data || []);
        setGames(resGames.data.data || []);
        setMetrics(resMetrics.data || null);
      } catch (err) {
        console.error("❌ Erreur lors du chargement des statistiques :", err);
      } finally {
        setLoading(false);
      }
    };
    fetchAll();
  }, []);

  if (loading) return <div className="loading">Chargement des statistiques...</div>;

  // -------------------------------
  // 🥇 Calcul : Top 10 pays les plus médaillés
  // -------------------------------
  const medalCountByCountry = results.reduce<Record<string, number>>((acc, r) => {
    acc[r.country_name] = (acc[r.country_name] || 0) + 1;
    return acc;
  }, {});

  const sortedCountries = Object.entries(medalCountByCountry)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 10);

  const countries = sortedCountries.map(([c]) => c);
  const medals = sortedCountries.map(([, m]) => m);

  // -------------------------------
  // 🖼️ Rendu principal
  // -------------------------------
  return (
    <div className="statistics-page fade-in">
      <div className="container">
        <h1 className="page-title">📊 Statistiques Olympiques</h1>
        <p className="page-subtitle">
          Analyse des performances des pays, des athlètes et de l’intelligence artificielle.
        </p>

        {/* 🌍 Graphique : Clusters */}
        <section className="section">
          <h2>🌍 Clusters de performance</h2>
          <p>
            Regroupement automatique des pays selon leurs performances moyennes et années de participation.
          </p>
          <Plot
            data={[
              {
                x: clusters.map((c) => c.total_medals),
                y: clusters.map((c) => c.game_year),
                mode: "markers",
                marker: { size: 10, color: clusters.map((c) => c.cluster), colorscale: "Viridis" },
                text: clusters.map((c) => c.country_name),
              },
            ]}
            layout={{
              title: "Répartition des pays par clusters",
              xaxis: { title: "Total Médailles" },
              yaxis: { title: "Année des Jeux" },
            }}
            style={{ width: "100%", height: "500px" }}
          />
        </section>

        {/* 🏟️ Graphique : Chronologie des Jeux */}
        <section className="section">
          <h2>🏟️ Évolution des Jeux Olympiques</h2>
          <Plot
            data={[
              {
                x: games.map((g) => g.game_year),
                y: games.map((g) => (g.game_season === "Summer" ? 1 : 0)),
                mode: "markers+lines" as any, // 👈 Cast explicite
                text: games.map((g) => `${g.game_name} – ${g.game_location}`),
                marker: { color: "#FF9800", size: 10 },
              },
            ]}
            layout={{
              title: "Chronologie des éditions (Été = 1 / Hiver = 0)",
              xaxis: { title: "Année" },
              yaxis: { title: "Saison" },
            }}
            style={{ width: "100%", height: "400px" }}
          />
        </section>



        {/* 🥇 Graphique : Top 10 pays */}
        <section className="section">
          <h2>🏅 Top 10 des pays les plus médaillés</h2>
          <Plot
            data={[
              {
                type: "bar",
                x: countries,
                y: medals,
                marker: { color: "#0052a3" },
              },
            ]}
            layout={{
              title: "Nombre total de médailles par pays",
              xaxis: { title: "Pays" },
              yaxis: { title: "Médailles" },
            }}
            style={{ width: "100%", height: "450px" }}
          />
        </section>

        {/* 🤖 Section : Performances des modèles IA */}
        <section className="section metrics-section">
          <h2>🤖 Performances des modèles IA</h2>

          {metrics ? (
            <>
              {/* ======= Bloc Athlète ======= */}
              <div className="ai-metrics-grid">
                <div className="ai-card athlete-model">
                  <h3>🏃 Modèle Athlète</h3>
                  <div className="ai-values">
                    <div>
                      <span>🎯 Accuracy</span>
                      <strong>{(metrics.athlete?.accuracy * 100).toFixed(1)}%</strong>
                    </div>
                    <div>
                      <span>📈 Précision</span>
                      <strong>{(metrics.athlete?.precision * 100).toFixed(1)}%</strong>
                    </div>
                    <div>
                      <span>🔁 Recall</span>
                      <strong>{(metrics.athlete?.recall * 100).toFixed(1)}%</strong>
                    </div>
                    <div>
                      <span>⚖️ F1-Score</span>
                      <strong>{(metrics.athlete?.f1 * 100).toFixed(1)}%</strong>
                    </div>
                  </div>
                </div>

                {/* ======= Bloc Pays ======= */}
                <div className="ai-card country-models">
                  <h3>🌍 Modèles de prédiction par pays</h3>
                  <div className="model-table">
                    <table>
                      <thead>
                        <tr>
                          <th>Modèle</th>
                          <th>R²</th>
                          <th>MAE</th>
                          <th>RMSE</th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(metrics.country_medals || {}).map(([name, v]) => (
                          <tr key={name}>
                            <td><strong>{name}</strong></td>
                            <td>{v.R2.toFixed(3)}</td>
                            <td>{v.MAE.toFixed(1)}</td>
                            <td>{v.RMSE.toFixed(1)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              {/* ======= Graphique comparatif ======= */}
              <div className="ai-chart">
                <h3>📊 Comparaison des modèles (R²)</h3>
                <Plot
                  data={[
                    {
                      x: Object.keys(metrics.country_medals),
                      y: Object.values(metrics.country_medals).map((v: any) => v.R2),
                      type: "bar",
                      marker: { color: ["#007bff", "#28a745", "#ff9800"] },
                    },
                  ]}
                  layout={{
                    title: "",
                    xaxis: { title: "Modèles" },
                    yaxis: { title: "Score R²", range: [0, 1] },
                    margin: { t: 30, l: 60, r: 20, b: 50 },
                  }}
                  style={{ width: "100%", height: "400px" }}
                />
              </div>
            </>
          ) : (
            <p>Aucune métrique disponible pour le moment.</p>
          )}
        </section>
      </div>
    </div>
  );
};

export default Statistics;
