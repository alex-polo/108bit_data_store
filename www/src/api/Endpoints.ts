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
    // Schemes Parsers
    get_news_parsers: `${BASE_ENDPOINT}/admin-panel/get-news-parsers`,
    get_catalog_parsers: `${BASE_ENDPOINT}/admin-panel/get-catalog-parsers`,
    get_parser: `${BASE_ENDPOINT}/admin-panel/get-parser`,
    save_parser: `${BASE_ENDPOINT}/admin-panel/save-change-parser`,
    // News Gathering
    get_all_news_entity: `${BASE_ENDPOINT}/admin-panel/get-all-news-gathering`,
    create_news_entity: `${BASE_ENDPOINT}/admin-panel/create-news-gathering`,
    update_news_entity: `${BASE_ENDPOINT}/admin-panel/update-news-entity`,
    delete_news_gathering: `${BASE_ENDPOINT}/admin-panel/delete-news-gathering-by-id`,
    get_news_entity_by_name: `${BASE_ENDPOINT}/admin-panel/get-news-gathering-by-name`,
    get_active_news_parsers: `${BASE_ENDPOINT}/admin-panel/get-active-news-parsers`,
    // Catalog Gathering
    get_all_entity_catalogs_gathering: `${BASE_ENDPOINT}/admin-panel/get-all-entity-catalogs-gathering`,
    create_catalog_entity: `${BASE_ENDPOINT}/admin-panel/create-catalog-gathering`,
    update_catalog_entity: `${BASE_ENDPOINT}/admin-panel/update-catalog-gathering`,
    delete_catalog_entity: `${BASE_ENDPOINT}/admin-panel/delete-catalog-gathering-by-id`,
    get_catalog_entity_by_name: `${BASE_ENDPOINT}/admin-panel/get-catalog-gathering-by-name`,
    // Internet Sites
    get_all_internet_sites: `${BASE_ENDPOINT}/admin-panel/internet-sites/get-all-sites`,
  },
};

export default Endpoints;
