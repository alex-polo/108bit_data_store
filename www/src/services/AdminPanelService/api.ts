import { AxiosResponse } from 'axios';
import apiClient from '../../api/AxiosInstance';
import { IParserChangeData, IParserData } from './service.types';
import Endpoints from '../../api/Endpoints';

export const getNewsParsersAPI = async (): Promise<AxiosResponse> => {
  return apiClient.get<IParserData[]>(Endpoints.DASHBOARD.get_news_parsers);
};

export const getCatalogParsersAPI = async (): Promise<AxiosResponse> => {
  return apiClient.get<IParserData[]>(Endpoints.DASHBOARD.get_catalog_parsers);
};

export const getParsersAPI = async (parserSystemName: string): Promise<AxiosResponse> => {
  return apiClient.get<IParserData>(Endpoints.DASHBOARD.get_parser, {
    params: { parser_system_name: parserSystemName },
  });
};

export const saveChangedParserAPI = async (data: IParserChangeData): Promise<AxiosResponse> => {
  return apiClient.post<IParserChangeData>(Endpoints.DASHBOARD.save_parser, {
    system_name: data.system_name,
    parser_name: data.parser_name,
    description: data.description,
    is_enable: data.is_enable,
  });
};
