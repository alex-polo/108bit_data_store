import { Nav, Navbar } from 'react-bootstrap';

import style from './Sidebar.module.css';
import { ApplicationRouting } from '../../routes/Routes';
import { NavLink } from 'react-router-dom';

export const Sidebar = () => {
  //   if (queryUserOrganizations.isLoading) return <SidebarSpinner />;

  return (
    <>
      <div id="sidebar" className="sidebar">
        <Nav className="flex-column">
          <Navbar.Brand className="text-center navbar-brand" href={ApplicationRouting.USER_PROFILE_ROUTE.home}>
            <span className={style.header_text}>DataBank</span>
          </Navbar.Brand>
          <ul>
            <li className="header_text">Example</li>
            <NavLink className="header_text" to={ApplicationRouting.USER_PROFILE_ROUTE.metrics}>
              Метрики
            </NavLink>

            <NavLink className="header_text" to={ApplicationRouting.USER_PROFILE_ROUTE.parsers}>
              Парсеры
            </NavLink>
            {/* <NavLink className="btn btn-primary btn-sm" to={ApplicationRouting.USER_PROFILE.createObject}>
              + Новый объект
            </NavLink> */}
            {/* <li>Настройки</li> */}
          </ul>

          {/* {queryUserOrganizations.isLoading ? (
            queryUserOrganizations.data?.length ? (<></>) : (<></>)
            if (data?.length === 0) {
              return (
                <>
                  <ul>
                    <li>Ваш аккаунт не подтвержден</li>
                  </ul>
                </>
              );
            }

            Спиннер
            <SidebarSpinner />
          ) : // Проверка на суперпользователя
          props.isSuperUser ? (
            // Отрисовываем меню супепользователя
            <SuperuserMenu organizations={queryUserOrganizations.data} />
          ) : // Отрисовываем меню обычного пользователя
          queryUserOrganizations.data != undefined ? (
            <UserMenu organizations={queryUserOrganizations.data} />
          ) : (
            <span>Error</span>
          )}
          <SidebarSpinner /> */}
        </Nav>
      </div>
    </>
  );
};
