import { useQuery } from '@tanstack/react-query';
import { getAllNewsEntityAPI } from '../ApiRequest';

export const useAllNewsEntity = () => {
  const { data, isSuccess, isLoading, isError, refetch, dataUpdatedAt } = useQuery({
    queryKey: ['AllNewsEntity'],
    queryFn: () => getAllNewsEntityAPI(),
    select: ({ data }) => data,
  });

  return { newsEntity: data, isSuccess, isLoading, isError, refetch, dataUpdatedAt };
};
