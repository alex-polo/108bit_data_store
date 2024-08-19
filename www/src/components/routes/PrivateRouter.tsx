import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthProvider';
import { Routes } from './Routes';

type Props = { children: React.ReactNode };

const ProtectedRoute = ({ children }: Props) => {
  const location = useLocation();
  const { isLoggedIn } = useAuth();

  return isLoggedIn() ? <>{children}</> : <Navigate to={Routes.AUTH.login} state={{ from: location }} replace />;
};

export default ProtectedRoute;
