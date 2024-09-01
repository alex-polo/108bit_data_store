import { useMutation } from '@tanstack/react-query';
import { INewsEntityData } from '../service.types';
import { updateNewsEntityAPI } from '../ApiRequest';

export const useUpdateNewsEntity = () => {
  const mutation = useMutation({
    mutationKey: ['useCreateNewsEntity'],
    mutationFn: async (data: INewsEntityData) => updateNewsEntityAPI(data),
  });

  return mutation;
};
