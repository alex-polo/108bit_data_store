import { Row, Spinner } from 'react-bootstrap';

import { NewsEntityTable } from './NewsEntityTable';
import { useAllNewsEntity } from '../../../../services/AdminPanelService/hooks';

export const NewsGatheringPage = () => {
  const queryNewsEntity = useAllNewsEntity();

  if (queryNewsEntity.isLoading) <Spinner animation="grow" variant="primary" />;
  return (
    <>
      <Row>
        <h1>Новостные ресурсы</h1>
      </Row>
      <Row>
        {queryNewsEntity.isError ? (
          <p>Ошибка получения данных</p>
        ) : (
          <NewsEntityTable serverData={queryNewsEntity.newsEntity} />
        )}
      </Row>
    </>
  );
};
