// Weixinfront/utils/config.js
const ENV = 'dev' // 可切换为 prod

export const API_CONFIG = {
  baseURL: {
    dev: 'https://dev.your-api.com',
    prod: 'https://api.your-service.com'
  },
  endpoints: {
    STATIONS: '/api/charging/stations',
    RECORDS: '/api/charging/records',
    REPAIRS: '/api/repairs',
    USER: '/api/users'
  }
}

export const BASE_URL = API_CONFIG.baseURL[ENV]