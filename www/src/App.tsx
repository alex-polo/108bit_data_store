import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from 'react-router-dom';

import { ApplicationRouting } from './components/routes/Routes';

import { RootLayout } from './layouts/RootLayout';
import { AuthLayout } from './layouts/AuthLayout';
import { DashboardLayout } from './layouts/DashboardLayout';

import { HomePage, LoginPage, NotFoundPage } from './components/pages';
import { BreadcrumbPage, MetricsPage, ParsersPage, EditParserPage } from './components/AdminPanel';

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
            crumb: () => <BreadcrumbPage url="" name={null} />,
          }}
        >
          <Route index element={<HomePage />} />
          <Route
            path={ApplicationRouting.USER_PROFILE_ROUTE.metrics}
            element={<MetricsPage />}
            handle={{
              crumb: () => <BreadcrumbPage url={ApplicationRouting.USER_PROFILE_ROUTE.metrics} name="Метрики" />,
            }}
          />
          <Route
            path={ApplicationRouting.USER_PROFILE_ROUTE.parsers + '/'}
            element={<ParsersPage />}
            handle={{
              crumb: () => <BreadcrumbPage url={ApplicationRouting.USER_PROFILE_ROUTE.parsers} name="Парсеры" />,
            }}
          />
          <Route
            path={`${ApplicationRouting.USER_PROFILE_ROUTE.editParser}`}
            // path={'parsers/edit-parser/:parserSystemName'}
            element={<EditParserPage />}
            handle={{
              crumb: () => (
                <BreadcrumbPage
                  url={`${ApplicationRouting.USER_PROFILE_ROUTE.editParser}`}
                  name="Редактирование парсера"
                />
              ),
            }}
          />

          {/*<Route
            path={AppRoutes.USER_PROFILE.appealsRoute}
            element={<ObjectAppeals />}
            handle={{
              crumb: () => <UserAppealsCrumb />,
            }}
          />
          <Route
            path={AppRoutes.USER_PROFILE.objectSettingsRoute}
            element={<ObjectSettings />}
            handle={{
              crumb: () => <UserSettingsCrumb />,
            }}
          /> */}
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
