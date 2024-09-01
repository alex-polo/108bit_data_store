import { useQuery } from '@tanstack/react-query';
import { getAllCatalogsEntityAPI } from '../ApiRequest';

export const useAllCatalogsEntity = () => {
  const { data, isSuccess, isLoading, isError, refetch } = useQuery({
    queryKey: ['useAllCatalogsEntity'],
    queryFn: () => getAllCatalogsEntityAPI(),
    select: ({ data }) => data,
  });

  return { catalogsEntity: data, isSuccess, isLoading, isError, refetch };
};
