import React, { createContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { IUserLoginData, IUserProfile, UserProfile } from '../auth/auth.types';

type Props = { children: React.ReactNode };

type UserContextType = {
  logout: () => void;
  isLoggedIn: () => boolean;
  loginUser: (loginUserData: IUserLoginData) => Promise<void>;
  getUserProfile: () => void;
};

const AuthContext = createContext<UserContextType>({} as UserContextType);

export const AuthProvider = ({ children }: Props) => {
  const navigate = useNavigate();
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {}, []);

  const loginUser = async (loginData: IUserLoginData) => {};

  const logout = async () => {};

  const isLoggedIn = () => {
    return false;
  };

  const getUserProfile = async () => {};

  return (
    <AuthContext.Provider value={{ loginUser, logout, isLoggedIn, getUserProfile }}>
      {isReady ? children : null}
    </AuthContext.Provider>
  );
};

export const useAuth = () => React.useContext(AuthContext);
