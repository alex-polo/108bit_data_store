import axios, { AxiosResponse } from 'axios';
import apiClient from '../api/AxiosInstance';
import Endpoints from '../api/Endpoints';
import { IUserAccessToken, IUserLoginData, IUserProfile } from '../components/auth/auth.types';
// import { useQuery } from '@tanstack/react-query';

// export const loginAPI = async (login: string, password: string): Promise<AxiosResponse> => {
//   return await axiosInstance.post<IUserAccessToken>(
//     Endpoints.AUTH.login,
//     { username: login, password: password },
//     { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
//   );
// };

export const loginAPI = async (loginData: IUserLoginData): Promise<AxiosResponse> => {
  return apiClient.post<IUserAccessToken>(
    Endpoints.AUTH.login,
    { username: loginData.login, password: loginData.password },
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  );
  // return useQuery({
  //   queryKey: ['userLogin'],
  //   queryFn: () => {
  //     return apiClient.post<IUserAccessToken>(
  //       Endpoints.AUTH.login,
  //       { username: loginData.login, password: loginData.password },
  //       { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  //     );
  //   },
  //   select: ({ data }) => data,
  // });

  // return axiosInstance.post<IUserAccessToken>(
  //   Endpoints.AUTH.login,
  //   { username: login, password: password },
  //   { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  // );
};

export const logoutAPI = async () => {
  try {
    await apiClient.post(Endpoints.AUTH.logout, {});
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log(error.response?.data);
    } else {
      console.log(error);
    }
  }
};

export const getUserProfileAPI = async (): Promise<AxiosResponse> => {
  return apiClient.get<IUserProfile>(Endpoints.AUTH.user_profile);
};

// export const useGetUserOrganizations = () => {
//   return useQuery({
//     queryKey: ['userLogin'],
//     queryFn: getOrganizationAPI,
//     select: ({ data }) => data,
//   });
// };
