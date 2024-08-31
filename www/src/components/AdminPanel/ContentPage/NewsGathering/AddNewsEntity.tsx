import { Button, Container, Form, Row, Spinner } from 'react-bootstrap';

import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

import { INewsEntityData, IParserData } from '../../../../services/AdminPanelService/service.types';
import { useActiveParsers, useCreateNewsEntity } from '../../../../services/AdminPanelService/hooks';

type TypeErrorForm = {
  parserName: string | null;
  description: string | null;
  vendor: string | null;
  fieldTags: string | null;
  parser_id: string | null;
  isEnable: string | null;
};

export const AddNewsEntity = () => {
  const navigate = useNavigate();

  //   const [errors, setErrors] = useState<TypeErrorForm>({ parserName: null, description: null });

  const queryParsers = useActiveParsers();
  const saveMutation = useCreateNewsEntity();

  const [name, setName] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [vendor, setVendor] = useState<string>('');
  const [fieldTags, setFieldTags] = useState<string>('');
  const [parserId, setParserId] = useState<number>(-1);
  const [isEnable, setIsEnable] = useState<string>('Да');

  const cancelButtonHandler = () => {
    navigate(-1);
  };

  //   const validateForm = () => {
  //     const newErrors: TypeError = { parserName: null, description: null };
  //     if (!parserName) newErrors.parserName = 'Поле не может быть пустым';
  //     else if (parserName.length > 150) newErrors.parserName = 'Максимальная длина поля 150 символов';
  //     if (description.length > 300) newErrors.description = 'Описание не может быть больше 300 символов';
  //     return newErrors;
  //   };

  const onSubmitHandler = async (event: React.FormEvent) => {
    event.preventDefault();
    // const formErrors = validateForm();

    // if (formErrors.parserName != null || formErrors.description != null) {
    //   setErrors(formErrors);
    // } else {
    //   setErrors({ parserName: null, description: null });

    const data: Omit<INewsEntityData, 'id'> = {
      name: name,
      description: description,
      vendor: vendor,
      field_tags: fieldTags,
      is_enable: isEnable,
      parser_id: parserId,
    };

    saveMutation.mutate(data);
    // }
  };

  if (saveMutation.isSuccess) {
    navigate(-1);
  }

  if (queryParsers.isLoading) <Spinner animation="grow" variant="primary" />;

  if (queryParsers.isError) {
    return (
      <>
        <Row>
          <h1>Создание новостного ресурса</h1>
          <p>Произошла ошибка при открытии</p>
        </Row>
      </>
    );
  }

  return (
    <>
      {queryParsers.isSuccess ? (
        <>
          <Row>
            <h1>Создание новостного ресурса</h1>
            <hr />

            <Form onSubmit={onSubmitHandler}>
              <Form.Group className="mb-3">
                <Form.Label>Название</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Название"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  // isInvalid={!!errors?.parserName}
                />
                {/* <Form.Control.Feedback type="invalid">{errors?.parserName}</Form.Control.Feedback> */}
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Описание</Form.Label>
                <Form.Control
                  as="textarea"
                  type="text"
                  placeholder="Описание"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  // isInvalid={!!errors?.description}
                />

                {/* <Form.Control.Feedback type="invalid">{errors?.description}</Form.Control.Feedback> */}
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Название производителя</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Название производителя"
                  value={vendor}
                  onChange={(e) => setVendor(e.target.value)}
                  // isInvalid={!!errors?.parserName}
                />
                {/* <Form.Control.Feedback type="invalid">{errors?.parserName}</Form.Control.Feedback> */}
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Теги (Указываются через запятую, без пробелов)</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Указываются через запятую, без пробелов"
                  value={fieldTags}
                  onChange={(e) => setFieldTags(e.target.value)}
                  // isInvalid={!!errors?.parserName}
                />
                {/* <Form.Control.Feedback type="invalid">{errors?.parserName}</Form.Control.Feedback> */}
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Парсер</Form.Label>
                <Form.Select onChange={(e) => setParserId(parseInt(e.target.value))}>
                  <option value={-1}>Выберите парсер</option>
                  {queryParsers.parsers.map((parser: IParserData) => (
                    <option key={parser.id} value={parser.id}>
                      {parser.parser_name}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Включить</Form.Label>
                <Form.Select
                  value={isEnable}
                  onChange={(e) => setIsEnable(e.target.value)}
                  // isInvalid={!!errors?.parserName}
                >
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
