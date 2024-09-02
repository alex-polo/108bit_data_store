import { useQuery } from '@tanstack/react-query';
import { getNewsParsersAPI } from '../ApiRequest';

export const useGetNewsParsers = () => {
  const { data, isSuccess, isLoading, isError } = useQuery({
    queryKey: ['getNewsParsers'],
    queryFn: getNewsParsersAPI,
    select: (data) => data.data,
  });

  return { parsers: data, isSuccess, isLoading, isError };
};
