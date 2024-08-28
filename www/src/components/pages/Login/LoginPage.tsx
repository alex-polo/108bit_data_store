import { Button, Form, Spinner } from 'react-bootstrap';
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';

import { useAuth } from '../../context/AuthProvider';
import { toastWarning } from '../../../services/NotifycationService';
import { IUserLoginData } from '../../auth/auth.types';

import styles from './LoginPage.module.css';

type TypeError = {
  email: string | null;
  password: string | null;
};

export const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<TypeError>({ email: null, password: null });
  const { loginUser } = useAuth();
  const loginMutation = useMutation({ mutationFn: loginUser });

  const validateForm = () => {
    const newErrors: TypeError = { email: null, password: null };
    if (!email) newErrors.email = 'Требуется адрес электронной почты';
    else if (!/\S+@\S+\.\S+/.test(email)) newErrors.email = 'Недействительный адрес электронной почты';
    if (!password) newErrors.password = 'Требуется пароль';
    else if (password.length < 8) newErrors.password = 'Пароль должен содержать не менее 8 символов.';
    return newErrors;
  };

  const onSubmitHandler = async (event: React.FormEvent) => {
    event.preventDefault();
    const formErrors = validateForm();
    if (formErrors.email != null || formErrors.password != null) {
      setErrors(formErrors);
    } else {
      setErrors({ email: null, password: null });
      console.log('Login attempted');

      const loginData: IUserLoginData = {
        login: email,
        password: password,
      };

      loginMutation.mutate(loginData);
    }
  };

  if (loginMutation.isError) {
    toastWarning('Не удалось войти. Попробуйте еще раз.');
  }

  return (
    <>
      <div className={styles.login_wrapper}>
        <div className={styles.login_form_container}>
          <h4 className={styles.login_title}>Вход в систему</h4>
          <Form onSubmit={onSubmitHandler} className={styles.login_form}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Электронная почта</Form.Label>
              <Form.Control
                type="email"
                placeholder="Электронная почта"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                isInvalid={!!errors?.email}
              />
              <Form.Control.Feedback type="invalid">{errors?.email}</Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Пароль</Form.Label>
              <Form.Control
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                isInvalid={!!errors?.password}
              />
              <Form.Control.Feedback type="invalid">{errors?.password}</Form.Control.Feedback>
            </Form.Group>

            {!loginMutation.isPending ? (
              <Button className="btn btn-primary" type="submit" variant="primary">
                Войти
              </Button>
            ) : (
              <Button className="btn btn-primary" variant="primary" disabled>
                <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                &nbsp;Вход
              </Button>
            )}
          </Form>
        </div>
      </div>
    </>
  );
};
