import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Predictions.css";
import { apiUrl } from "data";

interface PredictionResult {
  total_medals: number;
}

const Predictions: React.FC = () => {
  const [countries, setCountries] = useState<any[]>([]);
  const [selectedCountry, setSelectedCountry] = useState<string>("");
  const [selectedYear, setSelectedYear] = useState<any>(2028);
  const [season, setSeason] = useState<"Summer" | "Winter">("Summer");
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Chargement de la liste des pays
  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const res = await axios.get(`${apiUrl}/countries/clusters`);
        const uniqueCountries = [
          ...new Set(res.data.data.map((item: any) => item.country_name)),
        ].sort();
        setCountries(uniqueCountries);
      } catch (err) {
        console.error("Erreur chargement pays:", err);
      }
    };
    fetchCountries();
  }, []);

  // Génération automatique des 20 prochaines éditions des JO
  const years = Array.from({ length: 20 }, (_, i) => 2024 + i * 4);

  // Lancer la prédiction
  const handlePredict = async () => {
    if (!selectedCountry) {
      setError("Veuillez sélectionner un pays.");
      return;
    }

    setError(null);
    setLoading(true);
    setPrediction(null);

    try {
      const res = await axios.post("http://localhost:8000/api/predict/medals", {
        country_name: selectedCountry,
        game_year: selectedYear,
        game_season: season,
      });

      setPrediction(res.data.prediction);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.message || "Erreur de prédiction.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="predictions-page fade-in">
      <div className="container">
        <h1 className="hero-title">🏅 Prédiction de Médailles</h1>
        <p className="hero-subtitle">
          Prédisez le nombre total de médailles pour un pays et une édition
          future des Jeux Olympiques.
        </p>

        <div className="prediction-form">
          {/* Ligne Pays + Année */}
          <div className="form-row">
            <div className="form-group" style={{ flex: 1, marginRight: "10px" }}>
              <label>Pays</label>
              <select
                value={selectedCountry}
                onChange={(e) => setSelectedCountry(e.target.value)}
              >
                <option value="">-- Sélectionnez un pays --</option>
                {countries.map((country) => (
                  <option key={country} value={country}>
                    {country}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group" style={{ flex: 1 }}>
              <label>Année</label>
              <select
                value={selectedYear}
                onChange={(e) => setSelectedYear(parseInt(e.target.value))}
              >
                {years.map((year) => (
                  <option key={year} value={year}>
                    {year}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Sélection de la saison */}
          <div className="form-group">
            <label>Saison</label>
            <div className="season-toggle">
              <button
                className={season === "Summer" ? "active" : ""}
                onClick={() => setSeason("Summer")}
              >
                ☀️ Été
              </button>
              <button
                className={season === "Winter" ? "active" : ""}
                onClick={() => setSeason("Winter")}
              >
                ❄️ Hiver
              </button>
            </div>
          </div>

          {/* Bouton de prédiction */}
          <button className="predict-btn" onClick={handlePredict} disabled={loading}>
            {loading ? "Prédiction en cours..." : "🔮 Prédire"}
          </button>

          {/* Résultat ou erreur */}
          {error && <p className="error-text">{error}</p>}
          {prediction && (
            <div className="result-card fade-in">
              <h2>Résultat de la prédiction</h2>
              <p>
                🏆 <strong>{selectedCountry}</strong> devrait remporter environ{" "}
                <strong>{prediction.total_medals}</strong> médailles lors des Jeux{" "}
                {season === "Summer" ? "d'Été" : "d'Hiver"} de{" "}
                <strong>{selectedYear}</strong>.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Predictions;
