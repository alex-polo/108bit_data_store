import { Row } from 'react-bootstrap';
import { CatalogsEntityTable } from './CatalogsEntityTable';

export const CatalogsGathering = () => {
  return (
    <>
      <Row>
        <h1>Ресурсы каталогов</h1>
      </Row>
      <Row>
        <CatalogsEntityTable />
      </Row>
    </>
  );
};
