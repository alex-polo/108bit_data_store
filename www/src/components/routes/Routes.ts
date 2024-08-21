export const ApplicationRouting = {
  AUTH: {
    login: '/login',
    logout: '/logout',
  },
  USER_PROFILE: {
    home: '/profile',
    createObject: 'create-object',
    createOrganization: 'create-organization',
    managementOrganizations: 'management-organizations',

    managementOrganizationRoute: 'management-organization/:name',

    noObjectsRoute: 'no-objects/:objectName',
    objectSettingsRoute: 'object-settings/:objectName',
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
