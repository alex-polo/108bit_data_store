import { Button, Form, Row, Spinner } from 'react-bootstrap';

import { useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

import { ICatalogEntityData, IParserData } from '../../../../services/AdminPanelService/service.types';
import {
  useCatalogEntityByName,
  useGetCatalogParsers,
  useUpdateCatalogEntity,
} from '../../../../services/AdminPanelService/hooks';

type TypeErrorForm = {
  name: string | null;
  url: string | null;
  description: string | null;
  parser_id: string | null;
  isEnable: string | null;
};

export const EditCatalogsEntity = () => {
  const { siteName } = useParams();
  const navigate = useNavigate();

  const [errors, setErrors] = useState<TypeErrorForm>({
    name: null,
    url: null,
    description: null,
    parser_id: null,
    isEnable: null,
  });

  const queryParsers = useGetCatalogParsers();
  const saveMutation = useUpdateCatalogEntity();
  const queryNewsEntity = useCatalogEntityByName(siteName);

  const [id, setId] = useState<number>(-1);
  const [name, setName] = useState<string>('');
  const [url, setUrl] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [parserId, setParserId] = useState<number>(-1);
  const [isEnable, setIsEnable] = useState<string>('Да');

  useEffect(() => {
    if (queryNewsEntity.catalogEntity?.id != undefined) setId(queryNewsEntity.catalogEntity?.id);
    if (queryNewsEntity.catalogEntity?.name != undefined) setName(queryNewsEntity.catalogEntity?.name);
    if (queryNewsEntity.catalogEntity?.url != undefined) setUrl(queryNewsEntity.catalogEntity?.url);
    if (queryNewsEntity.catalogEntity?.description != undefined)
      setDescription(queryNewsEntity.catalogEntity?.description);
    if (queryNewsEntity.catalogEntity?.parser_id != undefined) setParserId(queryNewsEntity.catalogEntity?.parser_id);
    if (queryNewsEntity.catalogEntity?.is_enable != undefined) setIsEnable(queryNewsEntity.catalogEntity?.is_enable);
  }, [queryNewsEntity.isSuccess]);

  const cancelButtonHandler = () => {
    navigate(-1);
  };

  const validateForm = () => {
    const newErrors: TypeErrorForm = {
      name: null,
      url: null,
      description: null,
      parser_id: null,
      isEnable: null,
    };
    if (!name) newErrors.name = 'Поле не может быть пустым';
    else if (name.length > 150) newErrors.name = 'Максимальная длина поля 150 символов';

    if (!url) newErrors.url = 'Поле не может быть пустым';
    else if (url.length > 300) newErrors.name = 'Максимальная длина поля 300 символов';

    if (description.length > 300) newErrors.description = 'Описание не может быть больше 300 символов';

    if (parserId == -1) newErrors.parser_id = 'Выберите парсер';

    return newErrors;
  };

  const onSubmitHandler = async (event: React.FormEvent) => {
    event.preventDefault();
    const formErrors = validateForm();

    if (
      formErrors.name != null ||
      formErrors.url != null ||
      formErrors.description != null ||
      formErrors.parser_id != null
    ) {
      setErrors(formErrors);
    } else {
      setErrors({
        name: null,
        url: null,
        description: null,
        parser_id: null,
        isEnable: null,
      });

      const data: ICatalogEntityData = {
        id: id,
        name: name,
        url: url,
        description: description,
        is_enable: isEnable,
        parser_id: parserId,
      };

      saveMutation.mutate(data);
    }
  };

  if (saveMutation.isSuccess) {
    navigate(-1);
  }

  if (queryParsers.isLoading) <Spinner animation="grow" variant="primary" />;

  if (queryParsers.isError) {
    return (
      <>
        <Row>
          <h1>Редактирование ресурса каталога</h1>
          <p>Произошла ошибка при открытии</p>
        </Row>
      </>
    );
  }

  return (
    <>
      {queryNewsEntity.isSuccess && queryParsers.isSuccess ? (
        <>
          <Row>
            <h1>Редактирование ресурса: {name}</h1>
            <hr />

            <Form onSubmit={onSubmitHandler}>
              <Form.Group className="mb-3">
                <Form.Label>Название</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Название"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  isInvalid={!!errors?.name}
                />
                <Form.Control.Feedback type="invalid">{errors?.name}</Form.Control.Feedback>
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>URL</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Адрес сайта"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  isInvalid={!!errors?.url}
                />
                <Form.Control.Feedback type="invalid">{errors?.url}</Form.Control.Feedback>
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Описание</Form.Label>
                <Form.Control
                  as="textarea"
                  type="text"
                  placeholder="Описание"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  isInvalid={!!errors?.description}
                />

                <Form.Control.Feedback type="invalid">{errors?.description}</Form.Control.Feedback>
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Парсер</Form.Label>
                <Form.Select
                  onChange={(e) => setParserId(parseInt(e.target.value))}
                  isInvalid={!!errors?.parser_id}
                  value={parserId}
                >
                  {queryParsers.parsers.map((parser: IParserData) => (
                    <option key={parser.id} value={parser.id}>
                      {parser.parser_name}
                    </option>
                  ))}
                </Form.Select>
                <Form.Control.Feedback type="invalid">{errors?.parser_id}</Form.Control.Feedback>
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Включить</Form.Label>
                <Form.Select value={isEnable} onChange={(e) => setIsEnable(e.target.value)}>
                  <option value="Да">Да</option>
                  <option value="Нет">Нет</option>
                </Form.Select>
              </Form.Group>

              {!saveMutation.isPending ? (
                <Button className="btn btn-success" type="submit" variant="primary">
                  Сохранить
                </Button>
              ) : (
                <Button className="btn btn-success" variant="primary" disabled>
                  <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                  &nbsp;Сохранение
                </Button>
              )}
              <Button onClick={cancelButtonHandler} className="btn btn-danger">
                Отмена
              </Button>
            </Form>
          </Row>
        </>
      ) : (
        <>
          <Button onClick={cancelButtonHandler} className="btn btn-danger">
            Отмена
          </Button>
        </>
      )}
    </>
  );
};
