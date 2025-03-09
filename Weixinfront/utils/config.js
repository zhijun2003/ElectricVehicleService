// Weixinfront/utils/config.js
export const API_CONFIG = {
  baseURL: process.env.NODE_ENV === 'development'
    ? 'http://localhost:8000'
    : 'https://api.yourdomain.com',
  endpoints: {
    STATIONS: '/api/charging/stations',
    RECORDS: '/api/charging/records',
    REPAIRS: '/api/repairs',
    USER: '/api/users'
  }
}

export const BASE_URL = API_CONFIG.baseURL[ENV]