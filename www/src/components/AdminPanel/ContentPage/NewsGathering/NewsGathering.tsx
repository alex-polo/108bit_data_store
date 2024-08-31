import { Row } from 'react-bootstrap';

import { NewsEntityTable } from './NewsEntityTable';

export const NewsGatheringPage = () => {
  return (
    <>
      <Row>
        <h1>Новостные ресурсы</h1>
      </Row>
      <Row>
        <NewsEntityTable />
      </Row>
    </>
  );
};
