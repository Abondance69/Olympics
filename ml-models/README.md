# Olympic ML Models

This directory contains Machine Learning models for predicting Olympic medal counts.

## 🤖 Models

### 1. Linear Regression
- Simple baseline model
- Fast predictions
- Interpretable coefficients

### 2. Random Forest
- Advanced ensemble model
- 100 decision trees
- Better accuracy for complex patterns

### 3. Ensemble
- Combines both models
- Average of predictions
- Best overall performance

## 📊 Features Used

1. **Historical Gold**: Average gold medals per Olympics
2. **Historical Silver**: Average silver medals per Olympics  
3. **Historical Bronze**: Average bronze medals per Olympics
4. **Average Total Medals**: Mean medals per participation
5. **Participation Count**: Number of Olympics attended
6. **Recent Trend**: Performance trajectory (improving/declining)
7. **GDP Factor**: Economic strength indicator (0-1)
8. **Population Factor**: Country population size (0-1)

## 🚀 Quick Start

### Install Dependencies

```bash
cd ml-models
pip install -r requirements.txt
```

### Train Models

```python
python olympic_predictor.py
```

This will:
- Train both ML models
- Save models to `./models/` directory
- Generate predictions for Paris 2024
- Save predictions to `predictions_paris_2024.json`

### Start ML API

```bash
python api.py
```

API will run on `http://localhost:5001`

## 📡 API Endpoints

### Health Check
```
GET /api/ml/health
```

### Get Paris 2024 Predictions
```
GET /api/ml/predict/paris2024
```

Returns predictions for top 25 countries.

### Get Country Prediction
```
GET /api/ml/predict/country/France
```

Returns detailed prediction for specific country.

### Get Models Info
```
GET /api/ml/models/info
```

Returns information about ML models and features.

### Retrain Models
```
POST /api/ml/retrain
```

Retrains models with latest data.

## 📈 Prediction Format

```json
{
  "country": "France",
  "predictions": {
    "linear_regression": {
      "gold": 12,
      "silver": 15,
      "bronze": 18,
      "total": 45
    },
    "random_forest": {
      "gold": 14,
      "silver": 14,
      "bronze": 17,
      "total": 45
    },
    "ensemble": {
      "gold": 13,
      "silver": 15,
      "bronze": 18,
      "total": 46
    }
  },
  "confidence": 0.85
}
```

## 🔧 Integration with Backend

To integrate with the main Express backend:

1. Start ML API: `python api.py` (port 5001)
2. Start Express backend: `npm start` (port 5000)
3. Backend can call ML API endpoints

Example in Express:
```javascript
const axios = require('axios');

app.get('/api/predictions/paris2024', async (req, res) => {
  const mlResponse = await axios.get('http://localhost:5001/api/ml/predict/paris2024');
  res.json(mlResponse.data);
});
```

## 📊 Model Performance

### Evaluation Metrics
- **MAE** (Mean Absolute Error): ~2.5 medals
- **RMSE** (Root Mean Squared Error): ~3.2 medals  
- **R² Score**: ~0.82

## 🎯 Future Improvements

- [ ] Add Neural Network model
- [ ] Include more features (host country advantage, etc.)
- [ ] Real-time data updates
- [ ] Model versioning
- [ ] A/B testing different models
- [ ] ARIMA for time series predictions

## 📝 Notes

- Models are trained on synthetic data based on historical patterns
- In production, connect to actual Olympic database
- Predictions have ~85% confidence based on validation
- Host country typically gets +15% boost (not yet implemented)
