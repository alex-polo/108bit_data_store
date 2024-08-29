import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { IParserData } from './service.types';
import { getCatalogParsersAPI, getNewsParsersAPI, getParsersAPI } from './api';

export const useGetNewsParsers = (): UseQueryResult<IParserData[], Error> => {
  return useQuery({
    queryKey: ['getNewsParsers'],
    queryFn: getNewsParsersAPI,
    select: ({ data }) => data,
  });
};

export const useGetCatalogParsers = (): UseQueryResult<IParserData[], Error> => {
  return useQuery({
    queryKey: ['getCatalogParsers'],
    queryFn: getCatalogParsersAPI,
    select: ({ data }) => data,
  });
};

export const useGetParser = (parserSystemName: string | undefined): UseQueryResult<IParserData, Error> => {
  if (parserSystemName === undefined) parserSystemName = '';

  return useQuery({
    queryKey: ['getParser', parserSystemName],
    queryFn: () => getParsersAPI(parserSystemName),
    select: ({ data }) => data,
  });
};
