import { useMutation } from '@tanstack/react-query';
import { INewsEntityData } from '../service.types';
import { createNewsEntityAPI } from '../ApiRequest';

export const useCreateNewsEntity = () => {
  const mutation = useMutation({
    mutationKey: ['useCreateNewsEntity'],
    mutationFn: async (data: Omit<INewsEntityData, 'id'>) => createNewsEntityAPI(data),
  });
  //   const query = useQuery({
  //     queryKey: ['saveParser', parserSystemName],
  //     queryFn: () => getParsersAPI(parserSystemName ? parserSystemName : ''),
  //     select: ({ data }) => data,
  //     enabled: !!parserSystemName,
  //   });

  return mutation;
};
