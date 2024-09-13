import { useQuery } from '@tanstack/react-query';
import { getAllInternetSitesAPI } from '../ApiRequest';

export const useGetInternetSites = () => {
  const { data, isSuccess, isLoading, isError, refetch } = useQuery({
    queryKey: ['useNewsEntityByName', name],
    queryFn: () => getAllInternetSitesAPI(),
    select: ({ data }) => data,
  });

  return { internetSites: data, isSuccess, isLoading, isError, refetch };
};
