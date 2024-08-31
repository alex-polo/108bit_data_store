import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { IParserData } from '../service.types';
import { getCatalogParsersAPI } from '../ApiRequest';

export const useGetCatalogParsers = (): UseQueryResult<IParserData[], Error> => {
  const query = useQuery({
    queryKey: ['getCatalogParsers'],
    queryFn: getCatalogParsersAPI,
    select: (data) => data.data,
  });

  return query;
};
