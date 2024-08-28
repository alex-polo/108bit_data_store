import { Container, Row, Spinner } from 'react-bootstrap';
import { useGetNewsParsers } from '../../../services/AdminPanelService';

export const ParsersPage = () => {
  const queryNewsParser = useGetNewsParsers();

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
      <Container fluid>
        <Row xs={6} md={6}>
          <h1>Парсеры</h1>
        </Row>
        <Row>
          <h2>Новостные парсеры</h2>
          {queryNewsParser.isError ? (
            <p>Ошибка получения новостных парсеров</p>
          ) : (
            // queryNewsParser.data?.map((parserData) => {
            //   <p key={parserData.id}>1</p>;
            // })
            <p>{queryNewsParser.data?.length}</p>
          )}
        </Row>
      </Container>
    </>
  );
};
