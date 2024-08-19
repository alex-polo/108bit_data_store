import { ReactElement } from 'react';
import { useOutlet } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import { AuthProvider } from '../components/context/AuthProvider';

export const RootLayout = (): ReactElement => {
  const outlet = useOutlet();

  return (
    <>
      <AuthProvider>
        <div className="wrapper">
          {outlet}
          <ToastContainer autoClose={7000} />
        </div>
      </AuthProvider>
    </>
  );
};
