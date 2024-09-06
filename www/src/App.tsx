import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from 'react-router-dom';

import { ApplicationRouting } from './components/routes/Routes';

import { RootLayout } from './layouts/RootLayout';
import { AuthLayout } from './layouts/AuthLayout';
import { DashboardLayout } from './layouts/DashboardLayout';
import { DashboardContentLayout } from './layouts/DashboardContentLayout';

import { HomePage, LoginPage, NotFoundPage } from './components/pages';
import { BreadcrumbPage, MetricsPage, ParsersPage, EditParserPage } from './components/AdminPanel';

import { NewsGatheringPage } from './components/AdminPanel/ContentPage';
import { AddNewsEntity } from './components/AdminPanel/ContentPage/NewsGathering/AddNewsEntity';
import { EditNewsEntity } from './components/AdminPanel/ContentPage/NewsGathering';
import {
  CatalogsGathering,
  CreateCatalogsEntity,
  EditCatalogsEntity,
} from './components/AdminPanel/ContentPage/CatalogsGathering';

import './App.css';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path={ApplicationRouting.PUBLIC.home} element={<RootLayout />}>
      <Route index element={<HomePage />} />
      <Route path={`${ApplicationRouting.AUTH.login}`} element={<LoginPage />} />
      <Route path="*" element={<NotFoundPage />} />
      <Route element={<AuthLayout />}>
        <Route
          path={`${ApplicationRouting.USER_PROFILE_ROUTE.home}/*`}
          element={<DashboardLayout />}
          handle={{
            crumb: () => <BreadcrumbPage url="" name={null} emptyUrl={false} />,
          }}
        >
          <Route index element={<HomePage />} />
          <Route
            path={ApplicationRouting.USER_PROFILE_ROUTE.metrics}
            element={<MetricsPage />}
            handle={{
              crumb: () => (
                <BreadcrumbPage url={ApplicationRouting.USER_PROFILE_ROUTE.metrics} name="Метрики" emptyUrl={false} />
              ),
            }}
          />
          <Route element={<DashboardContentLayout />}>
            {/* Схемы парсеров */}
            <Route
              path={ApplicationRouting.USER_PROFILE_ROUTE.parsers}
              element={<ParsersPage />}
              handle={{
                crumb: () => (
                  <BreadcrumbPage
                    url={ApplicationRouting.USER_PROFILE_ROUTE.parsers}
                    name="Схемы парсеров"
                    emptyUrl={false}
                  />
                ),
              }}
            />
            <Route
              path={`${ApplicationRouting.USER_PROFILE_ROUTE.editParser}`}
              element={<EditParserPage />}
              handle={{
                crumb: () => (
                  <BreadcrumbPage
                    url={`${ApplicationRouting.USER_PROFILE_ROUTE.editParser}`}
                    name="Редактирование парсера"
                    emptyUrl={true}
                  />
                ),
              }}
            />
          </Route>
          {/* Новостные ресурсы */}
          <Route element={<DashboardContentLayout />}>
            <Route
              path={ApplicationRouting.USER_PROFILE_ROUTE.newsGathering}
              element={<NewsGatheringPage />}
              handle={{
                crumb: () => (
                  <BreadcrumbPage
                    url={ApplicationRouting.USER_PROFILE_ROUTE.newsGathering}
                    name="Новостные ресурсы"
                    emptyUrl={false}
                  />
                ),
              }}
            />
            <Route
              path={ApplicationRouting.USER_PROFILE_ROUTE.createNewsGathering}
              element={<AddNewsEntity />}
              handle={{
                crumb: () => (
                  <BreadcrumbPage
                    url={ApplicationRouting.USER_PROFILE_ROUTE.createNewsGathering}
                    name="Редактирование новостного ресурса"
                    emptyUrl={true}
                  />
                ),
              }}
            />
            <Route
              path={ApplicationRouting.USER_PROFILE_ROUTE.editNewsGathering}
              element={<EditNewsEntity />}
              handle={{
                crumb: () => (
                  <BreadcrumbPage
                    url={ApplicationRouting.USER_PROFILE_ROUTE.editNewsGathering}
                    name="Редактирование новостного ресурса"
                    emptyUrl={true}
                  />
                ),
              }}
            />
          </Route>
          {/* Парсеры каталогов */}
          <Route element={<DashboardContentLayout />}>
            <Route
              path={ApplicationRouting.USER_PROFILE_ROUTE.catalogsGathering}
              element={<CatalogsGathering />}
              handle={{
                crumb: () => (
                  <BreadcrumbPage
                    url={ApplicationRouting.USER_PROFILE_ROUTE.catalogsGathering}
                    name="Ресурсы каталогов"
                    emptyUrl={false}
                  />
                ),
              }}
            />
            <Route
              path={ApplicationRouting.USER_PROFILE_ROUTE.createCatalogsGathering}
              element={<CreateCatalogsEntity />}
              handle={{
                crumb: () => (
                  <BreadcrumbPage
                    url={ApplicationRouting.USER_PROFILE_ROUTE.createCatalogsGathering}
                    name="Редактирование ресурса каталога"
                    emptyUrl={true}
                  />
                ),
              }}
            />
            <Route
              path={ApplicationRouting.USER_PROFILE_ROUTE.editCatalogsGathering}
              element={<EditCatalogsEntity />}
              handle={{
                crumb: () => (
                  <BreadcrumbPage
                    url={ApplicationRouting.USER_PROFILE_ROUTE.editCatalogsGathering}
                    name="Редактирование ресурса каталога"
                    emptyUrl={true}
                  />
                ),
              }}
            />
          </Route>
        </Route>
      </Route>
    </Route>
  )
);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
