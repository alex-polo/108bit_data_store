import { Container, Row, Spinner } from 'react-bootstrap';

import { ParserTable } from './ParsersTable';
import { useGetCatalogParsers, useGetNewsParsers } from '../../../../services/AdminPanelService/hooks';

export const ParsersPage = () => {
  const queryNewsParser = useGetNewsParsers();
  const queryCatalogParser = useGetCatalogParsers();

  if (queryNewsParser.isLoading) <Spinner animation="grow" variant="primary" />;

  return (
    <>
      <Container fluid>
        <Row xs={6} md={6}>
          <h1>Парсеры</h1>
        </Row>
        <Row>
          <h2>Новостные парсеры</h2>
          {queryNewsParser.isError ? (
            <p>Ошибка получения новостных парсеров</p>
          ) : (
            <ParserTable serverData={queryNewsParser.data} />
          )}
        </Row>
        <Row>
          <h2>Парсеры каталогов</h2>
          {queryCatalogParser.isError ? (
            <p>Ошибка получения парсеров каталогов</p>
          ) : (
            <ParserTable serverData={queryCatalogParser.data} />
          )}
        </Row>
      </Container>
    </>
  );
};
