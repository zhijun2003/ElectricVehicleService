// Weixinfront/utils/config.js
export const API_CONFIG = {
  baseURL: 'http://localhost:8000',
  endpoints: {
    STATIONS: '/api/charging/stations',
    RECORDS: '/api/charging/records',
    REPAIRS: '/api/repairs',
    USER: '/api/users'
  }
}

export const BASE_URL = API_CONFIG.baseURL[ENV]