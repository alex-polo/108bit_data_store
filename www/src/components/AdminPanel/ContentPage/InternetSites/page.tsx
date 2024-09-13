import { Row } from 'react-bootstrap';
import { TableInternetSites } from './table';

export const InternetSites = () => {
  return (
    <>
      <Row>
        <h1>Интернет ресурсы</h1>
      </Row>
      <Row>
        <TableInternetSites />
      </Row>
    </>
  );
};
