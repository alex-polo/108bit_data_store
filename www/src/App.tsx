import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from 'react-router-dom';

import { ApplicationRouting } from './components/routes/Routes';

import { RootLayout } from './layouts/RootLayout';
import { AuthLayout } from './layouts/AuthLayout';
import { DashboardLayout } from './layouts/DashboardLayout';

import { HomePage, LoginPage, NotFoundPage } from './components/pages';

import { BreadcrumbPage } from './components/Breadcrumbs';

import './App.css';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path={ApplicationRouting.PUBLIC.home} element={<RootLayout />}>
      <Route index element={<HomePage />} />
      <Route path="login" element={<LoginPage />} />
      <Route path="*" element={<NotFoundPage />} />
      <Route element={<AuthLayout />}>
        <Route
          path={`${ApplicationRouting.USER_PROFILE.home}/*`}
          element={<DashboardLayout />}
          handle={{
            crumb: () => <BreadcrumbPage url="" />,
          }}
        >
          {/* <Route index element={<DashboardHome />} />
          <Route
            path={AppRoutes.USER_PROFILE.managementOrganizations}
            element={<ManagementOrganization />}
            handle={{
              crumb: () => <ManagementOrganizationCrumb />,
            }}
          />
          <Route
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
          />

          <Route
            path={AppRoutes.USER_PROFILE.createObject}
            element={<CreateObject />}
            handle={{
              crumb: () => <UserAddObjectCrumb />,
            }}
          />
          <Route
            path={AppRoutes.USER_PROFILE.createOrganization}
            element={<CreateOrganizationForm />}
            handle={{
              crumb: () => <UserAddOrganizationCrumb />,
            }}
          />*/}
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
