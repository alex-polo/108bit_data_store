import { ReactElement } from 'react';
import { useOutlet } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import { AuthProvider } from '../components/context/AuthProvider';

import 'react-toastify/dist/ReactToastify.css';

export const RootLayout = (): ReactElement => {
  const outlet = useOutlet();

  return (
    <>
      <AuthProvider>
        <div className="wrapper">
          {/* <div className="d-flex justify-content-center align-items-center"> */}
          {outlet}
          <ToastContainer autoClose={7000} />
        </div>
      </AuthProvider>
    </>
  );
};
