import { useQuery } from '@tanstack/react-query';
import { getCatalogParsersAPI } from '../ApiRequest';

export const useGetCatalogParsers = () => {
  const { data, isSuccess, isLoading, isError } = useQuery({
    queryKey: ['getCatalogParsers'],
    queryFn: getCatalogParsersAPI,
    select: (data) => data.data,
  });

  return { parsers: data, isSuccess, isLoading, isError };
};
