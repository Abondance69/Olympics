import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour gérer les erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Stats endpoints
export const getOverviewStats = () => api.get('/stats/overview');
export const getFranceStats = () => api.get('/stats/france');
export const getMedalsByYear = (country?: string) => 
  api.get('/stats/medals-by-year', { params: { country } });
export const getTopSports = () => api.get('/stats/top-sports');
export const getHostCountries = () => api.get('/stats/host-countries');
export const getHistoricEvents = () => api.get('/stats/historic-events');

// Predictions endpoints
export const getParis2024Predictions = () => api.get('/predictions/paris2024');
export const getAthletePredictions = () => api.get('/predictions/athletes');
export const getClustering = () => api.get('/predictions/clustering');
export const getModelsComparison = () => api.get('/predictions/models');

// Countries endpoints
export const getAllCountries = () => api.get('/countries');
export const getCountryDetails = (code: string) => api.get(`/countries/${code}`);
export const compareCountries = (countries: string[]) => 
  api.get('/countries/compare', { params: { countries: countries.join(',') } });

// Athletes endpoints
export const getAthletes = (params?: { country?: string; sport?: string; limit?: number }) => 
  api.get('/athletes', { params });
export const getLegends = () => api.get('/athletes/legends');
export const getAthleteDetails = (id: number) => api.get(`/athletes/${id}`);

export default api;
