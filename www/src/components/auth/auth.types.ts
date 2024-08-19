export type UserProfile = {
  email: string;
  access_token: string;
};

export interface IUserLoginData {
  title?: string;
  children: React.ReactNode;
}

export interface IUserProfile {
  title?: string;
  children: React.ReactNode;
}
