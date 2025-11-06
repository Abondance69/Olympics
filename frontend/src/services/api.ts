import axios from 'axios';
import { apiUrl } from 'data';

const api = axios.create({
  baseURL: apiUrl,
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

// Games & Clusters endpoints
export const getGames = () => axios.get(`${apiUrl}/games`);
export const getCountriesClusters = () => axios.get(`${apiUrl}/countries/clusters`);

// Results endpoint
export const getResults = (params?: { country?: string; game?: string; season?: string }) => 
  axios.get(`${apiUrl}`, { params });

// Athlete prediction endpoint
export const predictAthlete = (data: { age?: number; athlete_year_birth?: number; games_participations: number }) => 
  axios.post(`${apiUrl}/predict/athlete`, data);

// Athletes list endpoint
export const getAthletesList = (params?: { year_birth?: number; games_participations?: number; limit?: number }) => 
  axios.get(`${apiUrl}/athletes`, { params });

export default api;
