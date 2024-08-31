import { useQuery } from '@tanstack/react-query';
import { getParsersAPI } from '../ApiRequest';

// export const useParser = (parserSystemName: string | undefined): UseQueryResult<IParserData, Error> => {
export const useParser = (parserSystemName: string | undefined) => {
  const { data, isSuccess, isLoading, isError } = useQuery({
    queryKey: ['getParser', parserSystemName],
    queryFn: () => getParsersAPI(parserSystemName ? parserSystemName : ''),
    select: ({ data }) => data,
    enabled: !!parserSystemName,
  });

  return { parser: data, isSuccess, isLoading, isError };
};
