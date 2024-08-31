const BASE_ENDPOINT = 'http://127.0.0.1:8443';

const Endpoints = {
  BASE_URL: BASE_ENDPOINT,
  AUTH: {
    login: `${BASE_ENDPOINT}/auth/jwt/login`,
    logout: `${BASE_ENDPOINT}/auth/jwt/logout`,
    user_profile: `${BASE_ENDPOINT}/users/me`,
  },
  DASHBOARD: {
    get_metrics: `${BASE_ENDPOINT}/frontend/get-metrics`,
    get_news_parsers: `${BASE_ENDPOINT}/admin-panel/get-news-parsers`,
    get_catalog_parsers: `${BASE_ENDPOINT}/admin-panel/get-catalog-parsers`,
    get_parser: `${BASE_ENDPOINT}/admin-panel/get-parser`,
    save_parser: `${BASE_ENDPOINT}/admin-panel/save-change-parser`,
    get_all_news_entity: `${BASE_ENDPOINT}/admin-panel/get-all-news-gathering`,
    create_news_entity: `${BASE_ENDPOINT}/admin-panel/create-news-gathering`,
    get_active_news_parsers: `${BASE_ENDPOINT}/admin-panel/get-active-news-parsers`,
  },
};

export default Endpoints;
