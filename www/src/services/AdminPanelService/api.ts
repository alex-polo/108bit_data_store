import { AxiosResponse } from 'axios';
import apiClient from '../../api/AxiosInstance';
import { IParserData } from './service.types';
import Endpoints from '../../api/Endpoints';

export const getNewsParsersAPI = async (): Promise<AxiosResponse> => {
  return apiClient.get<IParserData>(Endpoints.DASHBOARD.get_news_parsers);
};

export const getCatalogParsersAPI = async (): Promise<AxiosResponse> => {
  return apiClient.get<IParserData>(Endpoints.DASHBOARD.get_catalog_parsers);
};
