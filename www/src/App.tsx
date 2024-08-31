import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from 'react-router-dom';

import { ApplicationRouting } from './components/routes/Routes';

import { RootLayout } from './layouts/RootLayout';
import { AuthLayout } from './layouts/AuthLayout';
import { DashboardLayout } from './layouts/DashboardLayout';
import { DashboardContentLayout } from './layouts/DashboardContentLayout';

import { HomePage, LoginPage, NotFoundPage } from './components/pages';
import { BreadcrumbPage, MetricsPage, ParsersPage, EditParserPage } from './components/AdminPanel';

import './App.css';
import { NewsGatheringPage } from './components/AdminPanel/ContentPage';
import { AddNewsEntity } from './components/AdminPanel/ContentPage/NewsGathering/AddNewsEntity';

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
            {/* Вложенные маршруты парсера */}
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
                    name="Создание новостного ресурса"
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
