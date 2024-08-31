import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { IParserData } from '../service.types';
import { getNewsParsersAPI } from '../ApiRequest';

export const useGetNewsParsers = (): UseQueryResult<IParserData[], Error> => {
  return useQuery({
    queryKey: ['getNewsParsers'],
    queryFn: getNewsParsersAPI,
    select: ({ data }) => data,
  });
};
