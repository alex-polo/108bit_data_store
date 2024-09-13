// import { useQuery } from '@tanstack/react-query';
// import { getNewsEntityByNameParsersAPI } from '../ApiRequest';

// export const useInternetSites = (name: string | undefined) => {
//   const { data, isSuccess, isLoading, isError, refetch } = useQuery({
//     queryKey: ['useNewsEntityByName', name],
//     queryFn: () => getNewsEntityByNameParsersAPI(name ? name : ''),
//     select: ({ data }) => data,
//     // enabled: !!name,
//   });

//   return { newsEntity: data, isSuccess, isLoading, isError, refetch };
// };
// getAllInternetSitesAPI
