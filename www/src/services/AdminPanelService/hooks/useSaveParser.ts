import { useMutation } from '@tanstack/react-query';
import { IParserChangeData } from '../service.types';
import { saveChangedParserAPI } from '../ApiRequest';

export const useSaveParser = () => {
  const saveParserMutation = useMutation({
    mutationKey: ['createNewsEntity'],
    mutationFn: async (data: IParserChangeData) => saveChangedParserAPI(data),
  });
  //   const query = useQuery({
  //     queryKey: ['saveParser', parserSystemName],
  //     queryFn: () => getParsersAPI(parserSystemName ? parserSystemName : ''),
  //     select: ({ data }) => data,
  //     enabled: !!parserSystemName,
  //   });

  return saveParserMutation;
};
