import { useQuery } from '@tanstack/react-query';
import { getCatalogEntityByNameAPI } from '../ApiRequest';

export const useCatalogEntityByName = (name: string | undefined) => {
  const { data, isSuccess, isLoading, isError, refetch } = useQuery({
    queryKey: ['useCatalogEntityByName', name],
    queryFn: () => getCatalogEntityByNameAPI(name ? name : ''),
    select: ({ data }) => data,
  });

  return { catalogEntity: data, isSuccess, isLoading, isError, refetch };
};
