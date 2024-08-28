import axios from 'axios';
import Endpoints from './Endpoints';

const apiClient = axios.create({
  baseURL: Endpoints.BASE_URL,
  headers: {
    'Content-type': 'application/json',
    Accept: 'application/json',
  },
});

// axiosInstance.defaults.timeout = 1000;
// axiosInstance.defaults.headers['Content-Type'] = 'application/json';
// axiosInstance.defaults.headers['Accept'] = 'application/json';

export default apiClient;
