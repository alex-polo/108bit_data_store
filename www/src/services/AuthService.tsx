import axios, { AxiosResponse } from 'axios';
import axiosInstance from '../api/AxiosInstance';
import Endpoints from '../api/Endpoints';
import { IUserAccessToken, IUserProfile } from '../components/auth/auth.types';
import { useQuery } from '@tanstack/react-query';

export const loginAPI = async (login: string, password: string): Promise<AxiosResponse> => {
  return await axiosInstance.post<IUserAccessToken>(
    Endpoints.AUTH.login,
    { username: login, password: password },
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  );
};

export const logoutAPI = async () => {
  try {
    await axiosInstance.post(Endpoints.AUTH.logout, {});
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log(error.response?.data);
    } else {
      console.log(error);
    }
  }
};

export const getProfileAPI = async (): Promise<AxiosResponse> => {
  return await axiosInstance.get<IUserProfile>(Endpoints.AUTH.user_profile);
};

export const useGetUserOrganizations = () => {
  return useQuery({
    queryKey: ['userLogin'],
    queryFn: getOrganizationAPI,
    select: ({ data }) => data,
  });
};
