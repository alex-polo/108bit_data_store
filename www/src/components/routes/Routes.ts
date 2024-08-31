export const ApplicationRouting = {
  AUTH: {
    login: '/login',
    logout: '/logout',
  },
  USER_PROFILE_ROUTE: {
    home: '/admin-panel',
    parsers: 'parsers',
    editParser: 'parsers/edit-parser/:parserSystemName',
    editSite: 'parsers/edit-site/:siteName',
    newsGathering: 'news-gathering',
    createNewsGathering: 'news-gathering/create-news-gathering',
    catalogGathering: 'catalog-gathering',
    metrics: 'metrics',

    noObjectsRoute: 'no-objects/:objectName',
    objectSettingsRoute: 'object-settings/:objectName',
  },
  USER_PROFILE_LINK: {
    editParser: (parserSystemName: string) => `edit-parser/${parserSystemName}`,
    editSite: (siteName: string) => `edit-site/${siteName}`,
    createNewsGathering: 'create-news-gathering',
  },
  PUBLIC: {
    home: '/',
  },
};
