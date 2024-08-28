export type UserProfile = {
  email: string;
  access_token: string;
};

export interface IUserLoginData {
  login: string;
  password: string;
}

export interface IUserProfile {
  title?: string;
  children: React.ReactNode;
}

export interface IUserAccessToken {
  access_token: string;
  token_type: string;
}

export interface IUserProfile {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
  is_tg_bot: boolean;
}
