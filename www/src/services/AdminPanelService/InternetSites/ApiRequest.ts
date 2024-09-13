import { AxiosResponse } from 'axios';
import apiClient from '../../../api/AxiosInstance';
import Endpoints from '../../../api/Endpoints';
import { IInternetSiteDTO } from '../service.types';

export const getAllInternetSitesAPI = async (): Promise<AxiosResponse> => {
  return apiClient.get<IInternetSiteDTO[]>(Endpoints.DASHBOARD.get_all_internet_sites);
};
