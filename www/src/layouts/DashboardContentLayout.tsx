import { ReactElement } from 'react';
import { useOutlet } from 'react-router-dom';

import 'react-toastify/dist/ReactToastify.css';
import { Container } from 'react-bootstrap';

export const DashboardContentLayout = (): ReactElement => {
  const outlet = useOutlet();

  return (
    <>
      <Container fluid>{outlet}</Container>
    </>
  );
};
