import { Button, Container, Form, Row, Spinner } from 'react-bootstrap';

import { useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';

import { IParserChangeData } from '../../../../services/AdminPanelService/service.types';
import { useParser } from '../../../../services/AdminPanelService/hooks/useParser';
import { useSaveParser } from '../../../../services/AdminPanelService/hooks/useSaveParser';

type TypeError = {
  parserName: string | null;
  description: string | null;
};

export const EditParserPage = () => {
  const navigate = useNavigate();
  const { parserSystemName } = useParams();
  const [errors, setErrors] = useState<TypeError>({ parserName: null, description: null });

  const queryClient = useQueryClient();
  queryClient.invalidateQueries({ queryKey: ['getParser', parserSystemName] });
  const queryParser = useParser(parserSystemName);
  const saveMutation = useSaveParser();

  const [parserName, setParserName] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [isEnable, setIsEnable] = useState<string>('');
  const [disabledForm, setDisabledForm] = useState<boolean>(true);

  useEffect(() => {
    if (queryParser.parser?.parser_name != undefined) setParserName(queryParser.parser?.parser_name);

    if (queryParser.parser?.description != undefined) setDescription(queryParser.parser?.description);

    if (queryParser.parser?.is_enable != undefined) setIsEnable(queryParser.parser?.is_enable);

    if (queryParser.parser?.is_parser_scheme_missing == 'Активна') setDisabledForm(false);
  }, [queryParser.isSuccess]);

  const backButtonHandler = () => {
    navigate(-1);
  };

  const validateForm = () => {
    const newErrors: TypeError = { parserName: null, description: null };
    if (!parserName) newErrors.parserName = 'Поле не может быть пустым';
    else if (parserName.length > 150) newErrors.parserName = 'Максимальная длина поля 150 символов';
    if (description.length > 300) newErrors.description = 'Описание не может быть больше 300 символов';
    return newErrors;
  };

  const onSubmitHandler = async (event: React.FormEvent) => {
    event.preventDefault();
    const formErrors = validateForm();

    if (formErrors.parserName != null || formErrors.description != null) {
      setErrors(formErrors);
    } else {
      setErrors({ parserName: null, description: null });

      const data: IParserChangeData = {
        system_name: parserSystemName ? parserSystemName : '',
        parser_name: parserName,
        description: description,
        is_enable: isEnable,
      };

      saveMutation.mutate(data);
    }
  };

  if (saveMutation.isSuccess) {
    navigate(-1);
  }

  if (queryParser.isLoading) <Spinner animation="grow" variant="primary" />;

  if (queryParser.isError) {
    return (
      <>
        <Container fluid>
          <h1>Редактирование парсера</h1>
          <h2>Системное имя: {parserSystemName}</h2>
          <p>Произошла ошибка при открытии</p>
        </Container>
      </>
    );
  }

  return (
    <>
      {queryParser.isSuccess ? (
        <>
          <Container fluid>
            <Row>
              <h1>Редактирование парсера</h1>
              <br />
              <hr />
              <p>Системное имя: {parserSystemName}</p>
              {queryParser.parser?.parser_type == 'news_parser' ? (
                <p>Тип парсера: Новостной парсер</p>
              ) : (
                <p>Тип парсера: Парсер каталога</p>
              )}
              {queryParser.parser?.is_parser_scheme_missing == 'Активна' ? (
                <p>Схема парсера найдена в системе</p>
              ) : (
                <p>Схема парсера не найдена в системе</p>
              )}
              <hr />
              <Form onSubmit={onSubmitHandler}>
                <Form.Group className="mb-3">
                  <Form.Label>Имя парсера</Form.Label>
                  <Form.Control
                    disabled={disabledForm}
                    type="text"
                    placeholder="Имя парсера"
                    value={parserName}
                    onChange={(e) => setParserName(e.target.value)}
                    isInvalid={!!errors?.parserName}
                  />
                  <Form.Control.Feedback type="invalid">{errors?.parserName}</Form.Control.Feedback>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Описание</Form.Label>
                  <Form.Control
                    as="textarea"
                    disabled={disabledForm}
                    type="text"
                    placeholder="Описание"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    isInvalid={!!errors?.description}
                  />
                  <Form.Control.Feedback type="invalid">{errors?.description}</Form.Control.Feedback>
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Парсер включен:</Form.Label>
                  <Form.Select
                    value={isEnable === 'Да' ? isEnable : 'Нет'}
                    disabled={disabledForm}
                    onChange={(e) => setIsEnable(e.target.value)}
                  >
                    <option value="Да">Да</option>
                    <option value="Нет">Нет</option>
                  </Form.Select>
                </Form.Group>

                {!saveMutation.isPending ? (
                  <Button className="btn btn-success" type="submit" variant="primary" disabled={disabledForm}>
                    Сохранить
                  </Button>
                ) : (
                  <Button className="btn btn-success" variant="primary" disabled>
                    <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                    &nbsp;Сохранение
                  </Button>
                )}
                <Button onClick={backButtonHandler} className="btn btn-danger">
                  Назад
                </Button>
              </Form>
            </Row>
          </Container>
        </>
      ) : (
        <>
          <Container fluid>
            <Button onClick={backButtonHandler} className="btn btn-danger">
              Назад
            </Button>
          </Container>
        </>
      )}
    </>
  );
};
