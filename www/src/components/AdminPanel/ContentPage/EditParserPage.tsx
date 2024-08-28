import { Container, Row, Spinner } from 'react-bootstrap';
import { useGetNewsParsers, useGetCatalogParsers } from '../../../services/AdminPanelService';
import { ParserTable } from './Tables/Table';

type Props = {
  //   system_name: string;
};

export const EditParserPage = (props: Props) => {
  const queryNewsParser = useGetNewsParsers();
  const queryCatalogParser = useGetCatalogParsers();

  if (queryNewsParser.isLoading) <Spinner animation="grow" variant="primary" />;

  //   if (queryNewsParser.isError) {
  //     return (
  //       <>
  //         <h3>Error</h3>
  //       </>
  //     );
  //   }

  //   if (queryNewsParser.data?.length === 0) {
  //     return <Navigate to={ApplicationRouting.USER_PROFILE.createObject} replace />;
  //   }

  return (
    <>
      <Container>
        <Row xs={6} md={6}>
          <h1>Редактирование парсера</h1>
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
