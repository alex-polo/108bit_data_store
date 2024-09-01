import React, { createContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { IUserAccessToken, IUserLoginData, IUserProfile, UserProfile } from '../auth/auth.types';
import { getUserProfileAPI, loginAPI, logoutAPI } from '../../services/AuthService';
import { ApplicationRouting } from '../routes/Routes';
import apiClient from '../../api/AxiosInstance';
import axios from 'axios';

type Props = { children: React.ReactNode };

type UserContextType = {
  logout: () => void;
  isLoggedIn: () => boolean;
  loginUser: (loginUserData: IUserLoginData) => Promise<void>;
  getUserProfile: () => Promise<IUserProfile>;
};

const AuthContext = createContext<UserContextType>({} as UserContextType);

export const AuthProvider = ({ children }: Props) => {
  const navigate = useNavigate();

  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const userProfileLocalStorage = localStorage.getItem('userProfile');

    if (userProfileLocalStorage) {
      const profile: UserProfile = JSON.parse(userProfileLocalStorage);
      setUserProfile(profile);
      apiClient.defaults.headers['Authorization'] = `Bearer ${profile.access_token}`;
    } else {
      setUserProfile(null);
      apiClient.defaults.headers['Authorization'] = '';
    }

    setIsReady(true);
  }, []);

  const isLoggedIn = (): boolean => {
    return userProfile != null ? true : false;
  };

  const unauthorized = () => {
    localStorage.removeItem('userProfile');
    setUserProfile(null);
    navigate(ApplicationRouting.AUTH.login);
  };

  const loginUser = async (loginData: IUserLoginData): Promise<void> => {
    localStorage.removeItem('userProfile');
    setUserProfile(null);
    try {
      const accessData: IUserAccessToken = (await loginAPI(loginData)).data;
      const profile: UserProfile = { email: loginData.login, access_token: accessData.access_token };
      localStorage.setItem('userProfile', JSON.stringify(profile));
      setUserProfile(profile);
      apiClient.defaults.headers['Authorization'] = `Bearer ${profile.access_token}`;
      navigate(ApplicationRouting.USER_PROFILE_ROUTE.home);
    } catch (error) {
      console.log(error);
      throw new Error('Failed to login');
    }
  };

  const getUserProfile = async (): Promise<IUserProfile> => {
    try {
      const userProfileFormAPI: IUserProfile = (await getUserProfileAPI()).data;
      return userProfileFormAPI;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status == 401) {
          setUserProfile(null);
        }
      }
      console.log(error);
      throw new Error('Failed get user profile from server');
    }
  };

  const logout = async () => {
    if (userProfile != null) {
      logoutAPI();
    }
    unauthorized();
  };

  return (
    <AuthContext.Provider value={{ loginUser, logout, isLoggedIn, getUserProfile }}>
      {isReady ? children : null}
    </AuthContext.Provider>
  );
};

export const useAuth = () => React.useContext(AuthContext);
