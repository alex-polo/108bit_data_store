export const ApplicationRouting = {
  AUTH: {
    login: '/login',
    logout: '/logout',
  },
  USER_PROFILE_ROUTE: {
    home: '/admin-panel',
    parsers: 'parsers',
    metrics: 'metrics',
    editParser: 'parsers/edit-parser/:parserSystemName',

    managementOrganizationRoute: 'management-organization/:name',

    noObjectsRoute: 'no-objects/:objectName',
    objectSettingsRoute: 'object-settings/:objectName',
  },
  USER_PROFILE_LINK: {
    editParser: (parserSystemName: string) => `edit-parser/${parserSystemName}`,
  },
  PUBLIC: {
    home: '/',
  },
  ADMIN_PROFILE: {
    admin: 'admin',
  },
};

export const detailRoute = (route: string, detail: string): string => {
  return `${route}/${detail}`;
};
