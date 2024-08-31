import { useQuery } from '@tanstack/react-query';
import { getActiveNewsParsersAPI } from '../ApiRequest';

export const useActiveParsers = () => {
  const { data, isSuccess, isLoading, isError } = useQuery({
    queryKey: ['getActiveParers'],
    queryFn: () => getActiveNewsParsersAPI(),
    select: ({ data }) => data,
  });

  return { parsers: data, isSuccess, isLoading, isError };
};
