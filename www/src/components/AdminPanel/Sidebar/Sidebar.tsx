import { Nav, Navbar } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';

import { ApplicationRouting } from '../../routes/Routes';

import style from './Sidebar.module.css';

export const Sidebar = () => {
  return (
    <>
      <div id="sidebar" className="sidebar">
        <Nav className="flex-column">
          <Navbar.Brand className="text-center navbar-brand" href={ApplicationRouting.USER_PROFILE_ROUTE.home}>
            <span className={style.header_text}>DataBank</span>
          </Navbar.Brand>
          <ul>
            <li className="header_text_menu">Настройки</li>
            <NavLink className="sidebar_link" to={ApplicationRouting.USER_PROFILE_ROUTE.metrics}>
              Метрики
            </NavLink>
            <NavLink className="sidebar_link" to={ApplicationRouting.USER_PROFILE_ROUTE.metrics}>
              Интернет сайты
            </NavLink>
            <NavLink className="sidebar_link" to={ApplicationRouting.USER_PROFILE_ROUTE.parsers}>
              Схемы парсеров
            </NavLink>
            <NavLink className="sidebar_link" to={ApplicationRouting.USER_PROFILE_ROUTE.newsGathering}>
              Новости
            </NavLink>
            <NavLink className="sidebar_link" to={ApplicationRouting.USER_PROFILE_ROUTE.catalogsGathering}>
              Каталог
            </NavLink>
            <NavLink className="sidebar_link" to={ApplicationRouting.USER_PROFILE_ROUTE.catalogsGathering}>
              Просмотр очереди
            </NavLink>
            {/* <NavLink className="btn btn-primary btn-sm" to={ApplicationRouting.USER_PROFILE.createObject}>
              + Новый объект
            </NavLink> */}
            {/* <li>Настройки</li> */}
          </ul>
        </Nav>
      </div>
    </>
  );
};
