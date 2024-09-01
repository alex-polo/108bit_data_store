export const ApplicationRouting = {
  AUTH: {
    login: '/login',
    logout: '/logout',
  },
  USER_PROFILE_ROUTE: {
    home: '/admin-panel',
    metrics: 'metrics',
    parsers: 'parsers',
    editParser: 'parsers/edit-parser/:parserSystemName',
    editSite: 'parsers/edit-site/:siteName',
    newsGathering: 'news-gathering',
    createNewsGathering: 'news-gathering/create-news-gathering',
    editNewsGathering: 'news-gathering/edit-news-gathering/:siteName',

    catalogsGathering: 'catalogs-gathering',
    createCatalogsGathering: 'catalogs-gathering/create-catalog-gathering',
    editCatalogsGathering: 'catalogs-gathering/edit-catalog-gathering/:siteName',
  },
  USER_PROFILE_LINK: {
    editParser: (parserSystemName: string) => `edit-parser/${parserSystemName}`,
    editNewsGatheringEntity: (siteName: string) => `edit-news-gathering/${siteName}`,
    createNewsGatheringEntity: `create-news-gathering`,

    editCatalogGatheringEntity: (siteName: string) => `edit-catalog-gathering/${siteName}`,
    createCatalogGatheringEntity: `create-catalog-gathering`,
  },
  PUBLIC: {
    home: '/',
  },
};
